# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cancellation_days = fields.Integer(string='cancel Day',config_parameter="om_hospital.cancellation_days")
    
