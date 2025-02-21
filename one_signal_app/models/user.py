
from odoo import models, fields, api
from odoo.exceptions import ValidationError
# import datetime
from datetime import datetime
import requests
import logging
import re

_logger = logging.getLogger(__name__)

DEVICE_TYPE_MAPPING = {
    '0': 'iOSPush',                      # iOS
    '1': 'AndroidPush',                   # Android
    '2': 'AmazonPush',                    # Amazon
    '3': 'WindowsPhonePush',              # Windows Phone (MPNS)
    '4': 'ChromeAppPush',                 # Chrome Apps / Extensions
    '5': 'ChromePush',                    # Chrome Web Push
    '6': 'WindowsPush',                   # Windows (WNS)
    '7': 'SafariPush',                    # Safari
    '8': 'FirefoxPush',                   # Firefox
    '9': 'MacOSPush',                      # MacOS
    '10': 'AlexaPush',                     # Alexa
    '11': 'Email',                         # Email
    '13': 'HuaweiPush',                    # Huawei App Gallery Builds
    '14': 'SMS'                            # SMS
}

class user(models.Model):
    _name = 'one_signal_app.user'
    _description = 'one_signal_app_user'
    _rec_name="onesignal_id"

    external_user_id = fields.Char(string="External User ID")
    identifier = fields.Char(string="FCM Identifier" ,readonly=True)
    session_count = fields.Integer(string="Session Count")
    last_active = fields.Datetime(string="Last Active")
    device_os = fields.Char(string="Device OS",readonly=True)
    device_model = fields.Char(string="Device Model",readonly=True)
    ip = fields.Char(string="IP Address",readonly=True)
    onesignal_id=fields.Char(string="onesignal id",readonly=True)
    setting_id=fields.Many2one('one_signal_app.setting',string="App Name")
    token=fields.Char(string="Token")
    language=fields.Char(string="Language",readonly=True)
    tags=fields.Char(string="Tags")
    country=fields.Char(string="Country")
    device_type = fields.Selection([
    ('0', 'iOSPush '),
    ('1', 'AndroidPush'),
    ('2', 'AmazonPush'),
    ('3', 'WindowsPhonePush'),
    ('4', 'ChromeAppPush'),
    ('5', 'ChromePush'),
    ('6', 'WindowsPush'),
    ('7', 'SafariPush'),
    ('8', 'FirefoxPush'),
    ('9', 'MacOSPush'),
    ('10', 'AlexaPush'),
    ('11', 'Email'),
    ('13', 'HuaweiPush'),
    ('14', 'SMS'),], string="Device Type",default="0")
    sub_id=fields.Char(string="Subscription id",readonly=True)
    current_timestamp = datetime.utcnow().strftime('%Y-%m-%d%H:%M:%S')
    type=fields.Char(string="subscription type",readonly=True)
   
    






    @api.model
    def fetch_users(self, app_id):
        setting = self.env['one_signal_app.setting'].search([("id", "=", app_id)], limit=1)

        if not setting:
            _logger.error(f"No settings found for app_id: {app_id}")
            return
        
        url = f"https://onesignal.com/api/v1/players?app_id={setting.app_id}"
        _logger.info(f"Fetching users from URL: {url}")

        headers = {
            "accept": "text/plain",
            "Content-Type": "application/json",
            "Authorization": f"Key {setting.rest_api_key}"
        }

        response = requests.get(url, headers=headers)
        _logger.info(f"Response from OneSignal: {response.text}")

        if response.status_code == 200:
            data = response.json().get('players', [])
            for player in data:
                onesignal_id = player.get('id', '')
                external_user_id = player.get('external_user_id', '')

                detail_url = f"https://api.onesignal.com/apps/{setting.app_id}/users/by/external_id/{external_user_id}"
                
                detail_response = requests.get(detail_url, headers=headers)
                _logger.info(f"detail_url....................{detail_url}")
                _logger.info(f"detail_response....................{detail_response}")
               
                if detail_response.status_code == 200:
                            details = detail_response.json()
                            properties=details.get("properties",{})
                            sub_id=details.get("identity", {}).get("onesignal_id", None)
                            _logger.info(f"sub_id.....................{sub_id}")
                            subscriptions = details.get("subscriptions", [])

                            if subscriptions:
                                subscription_type = subscriptions[0].get("type")
                            else:
                                subscription_type = None  # or some default value l
                            _logger.info(f"subscription_type.........................{subscription_type}")

                           
                
                
                
                            existing_user=self.search([('onesignal_id', '=', onesignal_id)], limit=1)
                            values={
                                            'onesignal_id': onesignal_id,
                                            'external_user_id': player.get('external_user_id', ''),
                                            'identifier': player.get('identifier', ''),
                                            'session_count': player.get('session_count', 0),
                                            'last_active': fields.Datetime.to_string(datetime.utcfromtimestamp(player.get('last_active', 0))),
                                            'device_os': player.get('device_os', ''),
                                            'device_model': player.get('device_model', ''),
                                            'ip': player.get('ip',''),
                                            'setting_id': setting.id,
                                            'device_type': str(player.get('device_type', '')),
                                            'language': player.get('language', ''),
                                            'tags': ', '.join(player.get('tags', {}).values()),
                                            'token': player.get('identifier', ''),
                                            'sub_id':sub_id,
                                            "country":properties.get('country',''),
                                            "type":subscription_type
                                            

                                        }
                            if existing_user:
                                        existing_user.write(values)
                                        
                            else:
                                    self.with_context(sync_user=True).create(values)        
        else:
            _logger.error(f"Failed to fetch users: {response.text}")
 
                   


    @staticmethod
    def is_valid_email(email):
        """Function to validate an email address format."""
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(email and re.match(email_regex, email))
    
    @staticmethod
    def is_valid_phone(phone):
        """Function to validate a phone number format."""
        phone_regex = r"^\+?[1-9]\d{1,14}$"  # Supports E.164 format
        return bool(phone and re.match(phone_regex, phone))
    
    @api.model
    def create(self, vals):
        if not vals.get("device_type"):
             raise ValidationError("Device type is required. Please select valid device type")
          
        elif vals.get("device_type") == "11":
             email = vals.get("token")
             if not self.is_valid_email(email):
                raise ValidationError("Invalid email format. Please enter a valid email address.")

        elif vals.get("device_type") == "14":
             phone = vals.get("token")
             if not self.is_valid_phone(phone):
                raise ValidationError("Invalid phone Number. Please enter a valid Phone Number.")
             
        elif not vals.get("setting_id"):
             raise ValidationError("App name is required. Please select valid App name")
        
        else:
             if not vals.get("device_type") == "14":
                token = vals.get("token")
                if not token:
                    raise ValidationError("Token is required. Please enter a valid Token")

             
        sync_user = self.env.context.get('sync_user', False)
        if not sync_user:
                record = super(user, self).create(vals)   
                record.create_user()
                return record 
        else:
             return super(user, self).create(vals)
                       
    def create_user(self):
            subscriptions_type = DEVICE_TYPE_MAPPING.get(self.device_type, None)

            if not subscriptions_type:
                _logger.error(f"Invalid device type: {self.device_type}")
                return  # Stop execution if the device type is invalid
           
            url = f"https://api.onesignal.com/apps/{self.setting_id.app_id}/users"
            _logger.info(f"url..........................{self.token}")
            
            payload = {
                "properties": {
                    "country":self.country or None,
                    "tags": {
                            "key": self.tags or None,
                            
                            },
                    },
                "identity": { "external_id":f"{self.token}_{self.current_timestamp}" if self.external_user_id 
                   else f"{self.token}_{self.current_timestamp}"},
                "subscriptions": [
                                    {
                                        "type": subscriptions_type,
                                        "token": self.token,
                                    }
                                ]
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }

            response = requests.post(url, json=payload, headers=headers)
            _logger.info(f"response_text...................{response.status_code}")

            if response.status_code == 201:
                self.setting_id.sync_user()
                _logger.info("User created successfully in OneSignal.")
               
                return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'User Created successful!',
                    'type': 'rainbow_man',
                }
            }
            else:
                _logger.error(f"Failed to create user: {response.text}")
            
            




    def unlink(self):
        for record in self:
            record.delete_user() 
        return super(user, self).unlink()


    def delete_user(self):
            setting = self.env['one_signal_app.setting'].search([],limit=1)
            url = f"https://onesignal.com/api/v1/players/{self.onesignal_id}?app_id={setting.app_id}"

            headers = {
                "Authorization": f"Basic {setting.rest_api_key}",
            }

            response = requests.delete(url, headers=headers)

            if response.status_code == 200:
                _logger.info("User deleted successfully!")
                self.unlink()# that delete the records in tree view
            else:
                _logger.info(f"Failed to delete user: {response.text}")




                   
    @api.model
    def write(self, vals):
        res = super(user, self).write(vals)
        if res:  # Ensure write() succeeded before calling update_user()
            self.update_user()
        return res
       
    
    def update_user(self):
            subscriptions_type = DEVICE_TYPE_MAPPING.get(self.device_type, None)

            if not subscriptions_type:
                _logger.error(f"Invalid device type: {self.device_type}")
                return  # Stop execution if the device type is invalid
        
            url = f"https://api.onesignal.com/apps/{self.setting_id.app_id}/users/by/external_id/{self.external_user_id}"
            _logger.info(f"url..........................{url}")
            
            
            payload = {
                "properties": {
                    "language": self.language or None,
                    "country": self.country or None,
                    "tags": {"key": self.tags or None},
                },
                "identity": {
                    "external_id": f"{self.token}_{self.current_timestamp}"if self.external_user_id 
                   else f"{self.token}_{self.current_timestamp}"
                },
                "subscriptions": [
                    {
                        "type": subscriptions_type or None,
                        "token": self.token or None,
                    }
                ]
            }

            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"Key {self.setting_id.rest_api_key}"
            }

            response = requests.patch(url, json=payload, headers=headers)
       
            _logger.info(f"response_text...................{response.status_code}")
            if response.status_code == 202:
                _logger.info("User updated successfully in OneSignal.")
            else:
                _logger.error(f"Failed to update user: {response.text}")


    def sync_user_delete(self):
        setting = self.env['one_signal_app.setting'].search([])

        for signal_record in setting:
            
            url = f"https://onesignal.com/api/v1/players?app_id={setting.app_id}"
            _logger.info(f"Fetching users from URL: {url}")

            headers = {
                "accept": "text/plain",
                "Content-Type": "application/json",
                "Authorization": f"Key {setting.rest_api_key}"
            }
            try:
                    response = requests.get(url, headers=headers)
                    _logger.info(f"Response from OneSignal: {response.text}")

                    if response.status_code == 200:
                        onesignal_users = response.json().get('players', [])
                        onesignal_player_ids = [player.get('id') for player in onesignal_users]
                        odoo_users = self.search([('setting_id', '=', signal_record.id)])
                        for odoo_user in odoo_users:
                            if odoo_user.onesignal_id not in onesignal_player_ids:
                                _logger.info(f"User {odoo_user.onesignal_id} no longer exists in OneSignal. Deleting in Odoo.")
                                odoo_user.unlink()
                    else:
                        _logger.error(f"Failed to fetch users from OneSignal: {response.status_code}, {response.text}")
            except requests.exceptions.RequestException as e:
                    _logger.error(f"Error while syncing users from OneSignal: {str(e)}")               

               











        
            
           

      




































































































 