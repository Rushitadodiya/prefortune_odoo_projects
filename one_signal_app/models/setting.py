from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)



class setting(models.Model):
    _name = 'one_signal_app.setting'
    _description = 'one_signal_app_setting'
    _rec_name="name"

    name=fields.Char(string="Name",required=True)
    app_id=fields.Char(string="App ID",required=True)
    rest_api_key =fields.Char(string="Rest Api Key",required=True)
    total_players=fields.Integer(string="Total Players",compute="_total_player")
    connection_status=fields.Selection([('disconnected','Disconnected'),('connected','Connected')],string="Connection Status" ,default="disconnected")


    def test_connection(self):
        url = f"https://api.onesignal.com/apps/{self.app_id}"
        _logger.info(f"url.................................{url}")

        headers = {
            "accept": "text/plain",
            "Content-Type": "application/json",
            "Authorization": f"Key {self.rest_api_key}"
        }
        _logger.info(f"headers.................................{headers}")

        response = requests.get(url, headers=headers)
        _logger.info(f"response............................{response.text}")

        if response.status_code == 200:
            self.connection_status='connected'
            _logger.info(f"connection success....................................")
            # data = response.json()
            # # Default to 0 if 'players' key is missing
            # total_players = data.get('players', 0)  
            # # Create or update the record
            # self.create({'total_players': total_players})
        else:
            self.connection_status='disconnected'

   

    def sync_user(self):
        self.ensure_one()
        self.env['one_signal_app.user'].fetch_users(self.id)
        _logger.info(f"self_id........................{self.id}")
        self._total_player()
        _logger.info(f".................{self._total_player()}")
        return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'User sync successful!',
                    'type': 'rainbow_man',
                }
            }

    def _total_player(self):
        for record in self:
            players = self.env['one_signal_app.user'].search_count([('setting_id','=',record.id)])
            record.total_players=players


    def sync_segment(self):
        self.ensure_one()
        self.env['one_signal_app.segment'].fatch_segment(self.id)
        return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'segment sync successful!',
                    'type': 'rainbow_man',
                }
            }

    def sync_template(self):
       self.ensure_one()
       self.env['one_signal_app.template'].fatch_template(self.id)
       return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Template sync successful!',
                    'type': 'rainbow_man',
                }
            }
       
        


   
        



