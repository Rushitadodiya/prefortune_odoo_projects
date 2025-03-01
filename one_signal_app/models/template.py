from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime
import requests
import logging
import re

_logger = logging.getLogger(__name__)



class template(models.Model):
    _name = 'one_signal_app.template'
    _description = 'one_signal_app_template'
    _rec_name="name"


    template_id = fields.Char(string="Template ID",index=True,readonly=True)
    name = fields.Char(string="Template Name")
    created_at = fields.Datetime(string="Created At",readonly=True)
    updated_at = fields.Datetime(string="Updated At",readonly=True)
    channel = fields.Selection([
        ('push', 'Push Notification'),
        ('email', 'Email'),
        ('sms', 'SMS')
    ], string="Channel", required=True ,default="push")
    setting_id=fields.Many2one('one_signal_app.setting',string="App Name")
    email_subject = fields.Char(string="Email Subject")
    email_body = fields.Char(string="Email Body")
    email_preheader=fields.Char(string="Email preheader")
    headings = fields.Char(string="Headings")
    subtitle =fields.Char(string="Subtitle")
    contents = fields.Text(string="Contents")
    sms_from=fields.Char(string="Sms From")
    sms_media_urls=fields.Char(string="Sms Media URL")
    global_image = fields.Char(string="Global Image URL")
    is_android = fields.Boolean(string="Android")
    is_ios = fields.Boolean(string="iOS")
    is_macos = fields.Boolean(string="macOS")
    is_adm = fields.Boolean(string="Amazon Device Messaging")
    is_alexa = fields.Boolean(string="Alexa",readonly=True)
    is_wp = fields.Boolean(string="Windows Phone")
    is_wp_wns = fields.Boolean(string="Windows Notification Service")
    is_chrome = fields.Boolean(string="Chrome")
    is_chrome_web = fields.Boolean(string="Chrome Web")
    is_safari = fields.Boolean(string="Safari")
    is_firefox = fields.Boolean(string="Firefox")
    is_edge = fields.Boolean(string="Edge")


    


    @api.model
    def fatch_template(self,app_id):
        setting = self.env['one_signal_app.setting'].search([("id", "=",app_id)],limit=1)
        if not setting:
            _logger.error(f"No settings found for app_id: {app_id}")
            raise ValidationError(f"No settings found for app_id: {app_id}")
            return
        url = f"https://api.onesignal.com/templates?limit=49&offset=offset&app_id={setting.app_id}"
        headers = {
                    "accept": "application/json",
                    "Authorization": f"Key {setting.rest_api_key}",
                    "Content-Type": "application/json; charset=utf-8"
                }

        response = requests.get(url, headers=headers)
        _logger.info(f"response of fetch users.................{response.text}")
        if response.status_code == 200:
                data = response.json()
                templates = data.get('templates', [])

                for template in templates:
                    template_id = template.get('id', '')

                    detail_url = f"https://api.onesignal.com/templates/{template_id}?app_id={setting.app_id}"

                    detail_response = requests.get(detail_url, headers=headers)

                    if detail_response.status_code == 200:
                            
                            details = detail_response.json()

                            headings = details.get('content', {}).get('headings', {}).get('en', '')
                            # subtitle = details.get('content', {}).get('subtitle', {}).get('en', 'null')
                            contents = details.get('content', {}).get('contents', {}).get('en', '')
                            global_image = details.get('content', {}).get('global_image', '')
                            content = details.get('content', {})


                            values ={
                                'template_id': template_id,
                                'name': template.get('name', ''),
                                'created_at': fields.Datetime.to_string(
                                    datetime.datetime.strptime(template.get('created_at', ''), "%Y-%m-%dT%H:%M:%S.%fZ")
                                ) if template.get('created_at') else False,
                                'updated_at': fields.Datetime.to_string(
                                    datetime.datetime.strptime(template .get('updated_at', ''), "%Y-%m-%dT%H:%M:%S.%fZ")
                                ) if template.get('updated_at') else False,
                                'channel': template.get('channel', ''),
                                'setting_id':setting.id,
                                'headings': headings,
                                # 'subtitle':subtitle,
                                'contents': contents,
                                'global_image': global_image,
                                'is_android': content.get('isAndroid', False),
                                'is_ios': content.get('isIos', False),
                                'is_macos': content.get('isMacOSX', False),
                                'is_adm': content.get('isAdm', False),
                                'is_alexa': content.get('isAlexa', False),
                                'is_wp': content.get('isWP', False),
                                'is_wp_wns': content.get('isWP_WNS', False),
                                'is_chrome': content.get('isChrome', False),
                                'is_chrome_web': content.get('isChromeWeb', False),
                                'is_safari': content.get('isSafari', False),
                                'is_firefox': content.get('isFirefox', False),
                                'is_edge': content.get('isEdge', False),
                                'email_subject':content.get('email_subject', ''),
                                'email_body':content.get('email_body', ''),
                                'email_preheader':content.get('email_preheader',''),

                            }
                            existing_template = self.search([('template_id', '=', template_id)], limit=1)
                            if existing_template:
                                existing_template.write(values)
                            else:
                                self.with_context(sync_template=True).create(values)




    @staticmethod
    def is_valid_phone(phone):
        """Function to validate a phone number format."""
        phone_regex = r"^\+?[1-9]\d{1,14}$"  # Supports E.164 format
        return bool(phone and re.match(phone_regex, phone))
             
    @api.model
    def create(self, vals):
        # if not vals.get("name"):
        #      raise ValidationError("Template Name is required. Please enter valid Template Name")
        # elif not vals.get("setting_id"):
        #      raise ValidationError("App Name is required. Please select valid App Name")
        
        # if vals.get("channel")=='push':
        #     if not vals.get("headings"):
        #         raise ValidationError("Heading is required. Please enter valid Heading")
        #     elif not vals.get("subtitle"):
        #         raise ValidationError("subtitle is required. Please enter valid subtitle")
        #     elif not vals.get("contents"):
        #         raise ValidationError("contents is required. Please enter valid contents")
            
        # if vals.get("channel")=='email':
        #     if not vals.get("email_subject"):
        #         raise ValidationError("Email subject is required. Please enter valid Email subject")
        #     elif not vals.get("email_body"):
        #         raise ValidationError("Email body is required. Please enter valid Email body")
            
        if vals.get("channel")=='sms':
            phone = vals.get("sms_from")
            if not self.is_valid_phone(phone):
                raise ValidationError("Invalid phone Number. Please enter a valid Phone Number.")
        
        sync_template = self.env.context.get('sync_template', False)
        if not sync_template:
                record = super(template, self).create(vals)   
                record.create_template()
                return record 
        else:
             return super(template, self).create(vals)  
    
    def create_template(self):
    
        url = "https://api.onesignal.com/templates"
        _logger.info(f"##################################################{self.setting_id.app_id}")
        _logger.info(f"---------------------------------------------------------{self.setting_id.rest_api_key}")
        if self.channel == "email":
             payload = {
                    "app_id":self.setting_id.app_id,
                    "name":self.name,
                    "isEmail":True,
                    "email_subject":self.email_subject,
                    "email_body":self.email_body,
                    "email_preheader":self.email_preheader,
                    }
        elif self.channel == "sms":
              payload = {
                    "app_id":self.setting_id.app_id,
                    "name":self.name,
                    "isSMS": True,
                    "sms_from":self.sms_from,
                    "contents": {"en": self.contents},
                    "sms_media_urls": self.sms_media_urls,
                }
             
        else:
             payload = {
                    "app_id":self.setting_id.app_id,
                    "name":self.name,
                    "contents":{"en": self.contents},
                    "headings":{"en": self.headings },
                    "subtitle":{"en": self.subtitle },
                    "isAndroid":self.is_android or False,
                    "isIos": self.is_ios or False,
                    "isMacOSX":self.is_macos or False,
                    "isAdm": self.is_adm or False,
                    # "isAlexa":self.is_alexa or False,
                    "isWP": self.is_wp or False,
                    "isWP_WNS":self.is_wp_wns or False,
                    "isChrome": self.is_chrome or False,
                    "isChromeWeb":self.is_chrome_web or False,
                    "isSafari": self.is_safari or False,
                    "isFirefox": self.is_firefox or False,
                    "isEdge": self.is_edge or False,  
                  }
       
             
        
        headers = {
            "accept": "application/json",
            "Authorization": f"Key {self.setting_id.rest_api_key} ",
            "Content-Type": "application/json; charset=utf-8"
        }

        response = requests.post(url, json=payload, headers=headers)
        _logger.info(f"response_text...................{response.status_code}")
        if response.status_code == 200:
                _logger.info("Template created successfully in OneSignal.")
                self.setting_id.sync_template()
        else:
                _logger.error(f"Failed to create Template: {response.text}")
                raise ValidationError(f"Failed to create Template: {response.text}")

        _logger.info(f"response_text......................{response.text}")


    @api.model
    def write(self, vals):
        res = super(template, self).write(vals)
        if res:  # Ensure write() succeeded before calling update_user()
            self.update_template()
        return res
    

    def update_template(self):
        url = f"https://api.onesignal.com/templates/{self.template_id}?app_id={self.setting_id.app_id}"

        _logger.info(f"##################################################{url}")

        _logger.info(f"---------------------------------------------------------{self.setting_id.rest_api_key}")
        if self.channel == "email":
             payload = {
                    "app_id":self.setting_id.app_id,
                    "name":self.name,
                    "isEmail":True,
                    "email_subject":self.email_subject,
                    "email_body":self.email_body,
                    "email_preheader":self.email_preheader,
                   
                    }
        elif self.channel == "sms":
              payload = {
                    "app_id":self.setting_id.app_id,
                    "name":self.name,
                    "isSMS": True,
                    "sms_from":self.sms_from,
                    "contents": { "en": self.contents},
                    "sms_media_urls": self.sms_media_urls or " ",
                }
             
        else:
             payload = {
                    "app_id":self.setting_id.app_id,
                    "name":self.name,
                    "contents":{"en": self.contents},
                    "headings":{ "en": self.headings },
                    "subtitle":{ "en": self.subtitle },
                    "isAndroid":self.is_android or False,
                    "isIos": self.is_ios or False,
                    "isMacOSX":self.is_macos or False,
                    "isAdm": self.is_adm or False,
                    # "isAlexa":self.is_alexa or False,
                    "isWP": self.is_wp or False,
                    "isWP_WNS":self.is_wp_wns or False,
                    "isChrome": self.is_chrome or False,
                    "isChromeWeb":self.is_chrome_web or False,
                    "isSafari": self.is_safari or False,
                    "isFirefox": self.is_firefox or False,
                    "isEdge": self.is_edge or False,  
                  }
             _logger.info(f"push.............................{payload}")
       
             
        
        headers = {
            "accept": "application/json",
            "Authorization": f"Key {self.setting_id.rest_api_key} ",
            "Content-Type": "application/json; charset=utf-8"
        }

        response = requests.patch(url, json=payload, headers=headers)
        _logger.info(f"response_text...................{response.status_code}")
        if response.status_code == 200:
                _logger.info("User updated successfully in OneSignal.")
        else:
                _logger.error(f"Failed to update user: {response.text}")

    def unlink(self):
        for record in self:
            record.delete_template() 
        return super(template, self).unlink()
    
    def delete_template(self):
        setting = self.env['one_signal_app.setting'].search([],limit=1)

        url = f"https://api.onesignal.com/templates/{self.template_id}?app_id={setting.app_id}"

        headers = {
            "Authorization":  f"Key {setting.rest_api_key}"
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
                _logger.info("Template deleted successfully!")
                self.unlink()# that delete the records in tree view
        else:
                _logger.info(f"Failed to delete Template: {response.text}")        



    def sync_template_delete(self):
        setting = self.env['one_signal_app.setting'].search([])

        for signal_record in setting:
            _logger.info(f"signal_record_app_id....................................{signal_record.app_id}")
            url = f"https://onesignal.com/api/v1/templates?app_id={signal_record.app_id}"
            _logger.info(f"Fetching users from URL: {url}")

            headers = {
                "accept": "text/plain",
                "Content-Type": "application/json",
                "Authorization": f"Key {signal_record.rest_api_key}"
            }
            response = requests.get(url, headers=headers)
            _logger.info(f"response........................................{response.text}")
            if response.status_code == 200:
                templates=response.json().get('templates',[])
                template_ids = [template.get('id') for template in templates]
                _logger.info(f"template_id...............................................{template_ids}")
                _logger.info(f"setting_id....................{self.setting_id}")
                _logger.info(f"signal_record_id....................{signal_record.id}")
                odoo_templates=self.search([('setting_id', '=', signal_record.id)])
                _logger.info(f"odoo_templates...................{odoo_templates}")
                for odoo_template in odoo_templates:
                            if odoo_template.template_id not in template_ids:
                                _logger.info(f"User {odoo_template.template_id} no longer exists in OneSignal. Deleting in Odoo.")
                                odoo_template.unlink()
            
            else:
                 _logger.error(f"Failed to fetch templates from OneSignal: {response.status_code}, {response.text}")
                 
        




































