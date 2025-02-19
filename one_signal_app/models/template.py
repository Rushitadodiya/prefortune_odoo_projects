from odoo import models, fields, api
import datetime
import requests
import logging

_logger = logging.getLogger(__name__)



class template(models.Model):
    _name = 'one_signal_app.template'
    _description = 'one_signal_app_template'


    template_id = fields.Char(string="Template ID",index=True,readonly=True)
    name = fields.Char(string="Template Name", required=True)
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
              
    @api.model
    def create(self, vals):
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
                _logger.info("User created successfully in OneSignal.")
                self.setting_id.sync_template()
        else:
                _logger.error(f"Failed to create user: {response.text}")

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
                    "sms_media_urls": self.sms_media_urls,
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





































