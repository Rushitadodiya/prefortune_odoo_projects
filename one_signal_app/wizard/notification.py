from odoo import api, fields, models, _
import logging
import requests
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)





class butttom(models.TransientModel):
    _name = 'onesignal.butttom.wizard'
    _description = 'OneSignal butttom Wizard'

    noti_id=fields.Many2one('onesignal.push.notification.wizard',string="Notify")
    btn_id=fields.Char(string="Button Id")
    btn_name=fields.Char(string="Button Name")
    btn_url=fields.Char(string="Button URL")


class OneSignalPushNotification(models.TransientModel):
    _name = 'onesignal.push.notification.wizard'
    _description = 'OneSignal Push Notification Wizard'

    name = fields.Many2one('one_signal_app.setting', string="OneSignal Account Name")
    template = fields.Many2one('one_signal_app.template', string="Templates", domain=[])
    segment_id = fields.Many2one('one_signal_app.segment', string="segment",domain=[])
    button_ids = fields.One2many('onesignal.butttom.wizard','noti_id',string="Action Button")
    subscription_id = fields.Many2many('one_signal_app.user', string="Subecription Id",domain=[])
    notification_type = fields.Selection([
         ('push','push'),('email','email'),('sms','sms')
    ], string="Notification Type", required=True,default="push")

    using_template = fields.Boolean(string="Using Template", default=False)
    heading = fields.Char(string="Heading")
    content = fields.Text(string="Content")
    email_subject = fields.Char(string="Email Subject")
    email_body = fields.Char(string="Email Body")
    cover_url = fields.Char(string="Cover URL")
    redirect_url = fields.Char(string="Redirect URL")
    action_btn = fields.Boolean(string="Action Button")
    
    send_to = fields.Selection([
        ('all', 'All'),
        ('subscription_id', 'Subscription ID'),
        ('segment', 'By segment'),
    ], string="Send To", required=True,default="all")

    template_domain = fields.Binary(compute="_compute_template_domain")
    segment_domain = fields.Binary(compute="_compute_segment")
    subcription_domain=fields.Binary(compute="_compute_sub_id")





    @api.depends('notification_type', 'name')
    def _compute_template_domain(self):
        """Compute domain for template selection based on OneSignal account and notification type"""
        for rec in self:
            if rec.name and rec.notification_type:
                rec.template_domain = [('setting_id', '=', rec.name.id), ('channel', '=', rec.notification_type)]
            else:
                rec.template_domain = [('id', '=', False)]
    
    @api.depends('name')
    def _compute_segment(self):
        for rec in self:
            if rec.name:
                rec.segment_domain = [('setting_id', '=', rec.name.id)]
            else:
                rec.segment_domain = [('id', '=', False)]
   
    @api.depends('name', 'notification_type')
    def _compute_sub_id(self):
            for rec in self:
                if rec.name and rec.notification_type:
                    domain = [('setting_id', '=', rec.name.id)]

                    # Mapping notification types to corresponding device_type values
                    notification_mapping = {
                        'push': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '13'],
                        'email': ['11'],
                        'sms': ['14'],
                    }

                    if rec.notification_type in notification_mapping:
                        domain.append(('device_type', 'in', notification_mapping[rec.notification_type]))

                    rec.subcription_domain = domain
                else:
                    rec.subcription_domain = [('id', '=', False)]

    @api.model  
    def one_signal_msg(self):

        setting = self.env['one_signal_app.setting'].search([], limit=1)

        if not setting:
            _logger.error("No OneSignal account selected.")
            return

        if setting.connection_status != 'connected':
            _logger.error(f"OneSignal account {setting.name} is not connected.")
            return

        url = f"https://api.onesignal.com/notifications?c=push"
        _logger.info("push..................................")
        payload = {
                    "app_id": setting.app_id,
                    "included_segments": ["Total Subscriptions"],  # Target audience
                    "contents": {"en": "Hii.. How are you.? I hope you are fine.......!"},
                    "headings": {"en": "Good Morning..!"},
                    "url": "https://www.prefortune.com/",  # Optional link
                    # "big_picture": "https://cdn.pixabay.com/photo/2022/09/29/11/45/dawn-7487173_640.jpg",  # Chrome web push image
                    "chrome_web_image": "https://cdn.pixabay.com/photo/2022/09/29/11/45/dawn-7487173_640.jpg",  # Web push image
                    "chrome_web_icon": "https://www.prefortune.com/wp-content/uploads/2023/08/PSS_new_final_logo-03.png",
                    "web_buttons":[
                                        {
                                            "id": "btn_1",
                                            "text": "Click Me",
                                            "url": "https://www.prefortune.com/"
                                        }
                                ],
                }
        headers = {
            "accept": "application/json",
            "Authorization": f"Key {setting.rest_api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()

            if response.status_code == 200:
                _logger.info(f"Push notification sent successfully: {response_data}")
            else:
                _logger.error(f"Failed to send notification: {response_data}")
        except Exception as e:
            _logger.error(f"Error sending push notification: {str(e)}")

      
       
    def fire_notification(self):
        """Send notification via OneSignal API"""
        # if not self.name:
        #    raise ValidationError("No OneSignal account selected.")
        # if self.send_to == 'subscription_id':
        #         if not self.subscription_id:
        #                 raise ValidationError(" Subecription Id is required. Please select valid Subecription Id") 
        # if self.send_to == 'segment':
        #         if not self.subscription_id:
        #                 raise ValidationError("segment is required. Please select valid segment") 
        # if self.using_template:  
        #         if not self.template:
        #                   raise ValidationError("Template is required. Please select valid Template")
            
        

        # if self.notification_type == 'push':
        #     if not self.heading :
        #         raise ValidationError("Heading is required. Please enter valid Heading")
        #     elif not self.content :
        #         raise ValidationError("content is required. Please enter valid content")
            

        # if self.notification_type == 'email':
        #     if not self.email_subject :
        #         raise ValidationError("Email subject is required. Please enter valid Email subject")
        #     elif not self.email_body :
        #         raise ValidationError("Email body is required. Please enter valid Email body")  


        # if self.notification_type == 'sms':
        #     if not self.heading :
        #         raise ValidationError("Heading is required. Please enter valid Heading")
        #     elif not self.content :
        #         raise ValidationError("content is required. Please enter valid content") 
            
        

        setting = self.name  # Selected OneSignal setting

        if setting.connection_status != 'connected':
            _logger.error(f"OneSignal account {setting.name} is not connected.")
            return

        url = f"https://api.onesignal.com/notifications?c={self.notification_type}"
        _logger.info("push..................................")
        payload = {
                    "app_id": setting.app_id,
                }

        # PUSH NOTIFICATION
        if self.notification_type == 'push':
            _logger.info("Sending Push Notification...")

            if self.send_to == 'all':   
                payload["included_segments"] = ["Total Subscriptions"]

            elif self.send_to == 'segment':
                if self.segment_id.name == 'Total Subscriptions':
                    payload["included_segments"] = ["Total Subscriptions"]
                elif self.segment_id.name == 'Active Subscriptions':
                    payload["included_segments"] = ["Active Subscriptions"]
                elif self.segment_id.name == 'Inactive Subscriptions':
                    payload["included_segments"] = ["Inactive Subscriptions"]
                elif self.segment_id.name == 'Engaged Subscriptions':
                    payload["included_segments"] = ["Engaged Subscriptions"]
                elif self.segment_id.name == 'All SMS Subscriptions':
                    payload["included_segments"] = ["All SMS Subscriptions"]
                else:
                    payload["included_segments"] = ["All Email Subscriptions"]
            elif self.send_to == 'subscription_id':
                    payload["include_player_ids"]=self.subscription_id.mapped('onesignal_id')
            else :
                return
           

            if self.content:
                payload["contents"] = {"en": self.content}

            if self.heading:
                payload["headings"] = {"en": self.heading}

            if self.redirect_url:
                payload["url"] = self.redirect_url

            if self.cover_url:
                payload["big_picture"] = self.cover_url

            if self.using_template and self.template:
                payload["template_id"] = self.template.template_id
                _logger.info(f"Using template ID: {self.template.template_id}")

            if self.action_btn and self.button_ids:
                    _logger.info(f"Action Buttons: {[{'id': btn.btn_id, 'name': btn.btn_name, 'url': btn.btn_url} for btn in self.button_ids]}")

                    payload["web_buttons"] = [
                        {
                            "id": button.btn_id,
                            "text": button.btn_name,
                            "url": button.btn_url or "",
                        }
                        for button in self.button_ids
                    ]

        # EMAIL NOTIFICATION
        elif self.notification_type == 'email':
            _logger.info("Sending Email Notification...")
            _logger.info("email..................................")
            payload.update({
                "email_subject": self.email_subject or "No Subject",
                "email_body": self.email_body or "",
            })
            if self.send_to == 'all':
                payload["included_segments"] = ["Total Subscriptions"]
            elif self.send_to == 'segment':
                if self.segment_id.name == 'Total Subscriptions':
                    payload["included_segments"] = ["Total Subscriptions"]
                elif self.segment_id.name == 'Active Subscriptions':
                    payload["included_segments"] = ["Active Subscriptions"]
                elif self.segment_id.name == 'Inactive Subscriptions':
                    payload["included_segments"] = ["Inactive Subscriptions"]
                elif self.segment_id.name == 'Engaged Subscriptions':
                    payload["included_segments"] = ["Engaged Subscriptions"]
                elif self.segment_id.name == 'All SMS Subscriptions':
                    payload["included_segments"] = ["All SMS Subscriptions"]
                else:
                    payload["included_segments"] = ["All Email Subscriptions"]
            elif self.send_to == 'subscription_id':
                    payload["include_player_ids"]=self.subscription_id.mapped('onesignal_id')
            else :
                return

            if self.using_template :
                payload["template_id"] = self.template.template_id
            


        # SMS NOTIFICATION
        elif self.notification_type == 'sms':
            _logger.info("Sending SMS Notification...")
            _logger.info("sms..................................")
            payload.update({
                # "contents": {"en": self.content or ""},
                "sms_from":"+15414066946",
                "name":setting.name,
            })
            _logger.info(f"payload.....................{payload}")
            if self.content:
                payload["contents"] = {"en": self.content}
            if self.send_to == 'all':
                payload["included_segments"] = ["Total Subscriptions"]
            elif self.send_to == 'segment':
                if self.segment_id.name == 'Total Subscriptions':
                    payload["included_segments"] = ["Total Subscriptions"]
                elif self.segment_id.name == 'Active Subscriptions':
                    payload["included_segments"] = ["Active Subscriptions"]
                elif self.segment_id.name == 'Inactive Subscriptions':
                    payload["included_segments"] = ["Inactive Subscriptions"]
                elif self.segment_id.name == 'Engaged Subscriptions':
                    payload["included_segments"] = ["Engaged Subscriptions"]
                elif self.segment_id.name == 'All SMS Subscriptions':
                    payload["included_segments"] = ["All SMS Subscriptions"]
                else:
                    payload["included_segments"] = ["All Email Subscriptions"]
            elif self.send_to == 'subscription_id':
                    payload["include_player_ids"]=self.subscription_id.mapped('onesignal_id')
            else :
                return

            if self.using_template and self.template:
                payload["template_id"] = self.template.template_id
                _logger.info(f"Using template ID: {self.template.template_id}")


        #HEADERS
        headers = {
            "accept": "application/json",
            "Authorization": f"Key {setting.rest_api_key}",
            "Content-Type": "application/json"
        }

        # SEND REQUEST
        response = requests.post(url, json=payload, headers=headers)
        _logger.info(f"Response from OneSignal: {response.text}")

        if response.status_code == 200:
            _logger.info("Notification sent successfully!")
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Notification sent successfully!',
                    'type': 'rainbow_man',
                }
            }
        else:
            _logger.error(f"Failed to send notification: {response.text}")


        return response
    



