from odoo import api, fields, models, _
import logging
import requests
from datetime import datetime
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)
class butttom(models.TransientModel):
    _name = 'contact.wizard'
    _description = 'contact Wizard'

    connector_ids=fields.Many2one('one_signal_app.setting',string="App Name")
   
   

    def _default_contact(self):
        return self.env.context.get('active_id')
    
    def _default_email(self):
        contact = self.env['res.partner'].browse(self.env.context.get('active_id'))
        return contact.email
    
    def _default_phone(self):
        contact = self.env['res.partner'].browse(self.env.context.get('active_id'))
        return contact.phone
    
    def _default_tags(self):
            contact = self.env['res.partner'].browse(self.env.context.get('active_id'))
            return ', '.join(contact.category_id.mapped('name'))
    
    def _default_country(self):
            contact = self.env['res.partner'].browse(self.env.context.get('active_id'))
            return contact.city

        

    contact_id = fields.Many2one('res.partner', string='Contact', default=_default_contact,readonly=True)
    notification_type=fields.Selection([
        ('email', 'Email'),
        ('sms', 'SMS')
        ],string="Notification Type")
    email = fields.Char(string='Email', default=_default_email)
    phone = fields.Char(string='Phone', default=_default_phone)
    category_id = fields.Char(string='tags', default=_default_tags)
    country=fields.Char(string='country',default=_default_country)
    
    def _is_already_subscribed(self, identifier):
        onesignal_app_id = self.connector_ids.app_id
        onesignal_rest_api_key = self.connector_ids.rest_api_key
        if self.notification_type == 'email':
            onesignal_url = f"https://api.onesignal.com/apps/{onesignal_app_id}/users/by/external_id/{identifier}"
        else:
            onesignal_url = f"https://api.onesignal.com/apps/{onesignal_app_id}/users/by/external_id/+{identifier}"
        _logger.info(f"onesignal_url..............{onesignal_url}")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {onesignal_rest_api_key}",
        }
        response = requests.get(onesignal_url, headers=headers)
        _logger.info(f"response alredy........................{response.status_code}")
        if response.status_code == 200:
                return True
        return False
    
    def subscribe_to_onesignal(self):
        if self.email and self.notification_type == 'email':
            if self._is_already_subscribed(self.email):
                _logger.info("______________________________________________________")
                raise ValidationError("This email is already subscribed to OneSignal.")
            else:
                self._subscribe_to_onesignal(self.email)
        elif self.phone and self.notification_type == 'sms':
            if self._is_already_subscribed(self.phone):
                raise ValidationError("This phone number is already subscribed to OneSignal.")
            else:
                self._subscribe_to_onesignal(self.phone)
        else:
            raise ValidationError("You Dont have Email and Phone number")
    def _subscribe_to_onesignal(self, identifier):
        _logger.info(f"----------------------------------------------------------------{identifier}")
        onesignal_app_id = self.connector_ids.app_id
        onesignal_rest_api_key = self.connector_ids.rest_api_key

        url=f"https://api.onesignal.com/apps/{onesignal_app_id}/users"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {onesignal_rest_api_key}",
        }
        types=''
        if identifier == self.email:
            types='Email'
        else:
            identifier=f"+{identifier}" if not identifier.startswith("+") else self.identifier
            types='SMS'

        payload = {"properties": {
                    "country":self.country,
                    "tags": {
                            "subscription_status": self.category_id
                            
                            },
                    },
                    "subscriptions":[
                        {"type":types,
                         "token":identifier,
                         "enabled":True
                         } ],
                    "identity":{"external_id" : f"{identifier}" },
                    }
        
        response = requests.post(url, json=payload, headers=headers)
        _logger.info(f"-----------------------------------------------------{response.status_code}")
        if response.status_code == 201:
            self.connector_ids.sync_user()
            _logger.info(f"--------------------------success=================================--===============")
            return True
        else:
            return False
