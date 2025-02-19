# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    minimum_quantity=fields.Integer(string='Quantity',config_parameter="low_cost_notification.minimum_quantity")
    

        