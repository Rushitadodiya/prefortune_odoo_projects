from odoo import models, fields, api
import datetime
import requests
import logging

_logger = logging.getLogger(__name__)



class segment(models.Model):
    _name = 'one_signal_app.segment'
    _description = 'one_signal_app_segment'

    segment_id = fields.Char(string="Segment ID", required=True, index=True)
    name = fields.Char(string="Segment Name", required=True)
    app_id = fields.Char(string="App ID", readonly=True)
    created_at = fields.Datetime(string="Created At")
    updated_at = fields.Datetime(string="Updated At")
    is_active = fields.Boolean(string="Is Active", default=True)
    source = fields.Char(string="Source")
    setting_id=fields.Many2one('one_signal_app.setting',string="App Name")


    @api.model
    def fatch_segment(self,app_id):
        setting = self.env['one_signal_app.setting'].search([("id", "=",app_id)],limit=1)
        for setting_data in setting:
            _logger.info(f"setting_id......................{setting_data.app_id}")
        
            if setting_data.connection_status =='connected':
                data_id=setting_data.id
                _logger.info(f"setting_data_app_id_success...........{data_id}")
                url = f"https://api.onesignal.com/apps/{setting_data.app_id}/segments?offset=0&limit=300"

                headers = {
                    "accept": "application/json",
                    "Authorization": f"Key {setting_data.rest_api_key}",
                    "Content-Type": "application/json; charset=utf-8"
                }

                response = requests.get(url, headers=headers)
                _logger.info(f"response of fetch users.................{response.text}")


        if response.status_code == 200:
                data = response.json()
                segments = data.get('segments', [])
                for segment in segments:
                
                    existing_segment = self.env['one_signal_app.segment'].search([('segment_id', '=', segment.get('id'))], limit=1)
                    if existing_segment:
                        continue  

                    self.create({
                        'segment_id':segment.get('id', ''),
                        'name': segment.get('name', ''),
                        'app_id': segment.get('app_id', ''),
                        'created_at': fields.Datetime.to_string(
                            datetime.datetime.strptime(segment.get('created_at', ''), "%Y-%m-%dT%H:%M:%S.%fZ")
                        ) if segment.get('created_at') else False,
                        'updated_at': fields.Datetime.to_string(
                            datetime.datetime.strptime(segment.get('updated_at', ''), "%Y-%m-%dT%H:%M:%S.%fZ")
                        ) if segment.get('updated_at') else False,
                        'is_active': segment.get('is_active', False),
                        'source': segment.get('source', ''),
                        'setting_id':data_id
                    })
    

    # @api.model
    # def create(self, vals):
    #     record = super(segment, self).create(vals)   
    #     record.create_segment()
    #     return record 
    
    # def create_segment(self):
    #     setting = self.env['one_signal_app.setting'].search([("id", "=", self.setting_id.id)], limit=1)
    #     if not setting or setting.connection_status != 'connected':
    #         _logger.error("OneSignal connection is not established.")
    #         return False

    #     url = f"https://api.onesignal.com/apps/{setting.app_id}/segments"
    #     _logger.info(f"URL..........................{url}")

    #     headers = {
    #         "accept": "application/json",
    #         "Authorization": f"Key {setting.rest_api_key}",
    #         "Content-Type": "application/json; charset=utf-8"
    #     }
      
    #     payload = {
    #         "name":self.name,
    #         "filters": [
    #             { "field": "tag", "key": "user_type", "relation": "=", "value": "premium" }
    #         ]
    #         }
    #     _logger.info(f"payload..............................{payload}")

    #     response = requests.post(url, json=payload, headers=headers)
    #     _logger.info(f"Response from OneSignal (create segment): {response.text}")
    #     return response

    def delete_segment(self):
        
            setting = self.env['one_signal_app.setting'].search([("id", "=", self.setting_id.id)], limit=1)
            url = f"https://api.onesignal.com/apps/{setting.app_id}/segments/{self.segment_id}"

            headers = {
                "accept": "application/json",
                "Authorization": f"Key {setting.rest_api_key}"
            }

            response = requests.delete(url, headers=headers)

            
            if response.status_code == 200:
                _logger.info("segment deleted successfully!")
                self.unlink()# that delete the records in tree view
            else:
                _logger.info(f"Failed to delete segment: {response.text}")    
                    
          
        
        