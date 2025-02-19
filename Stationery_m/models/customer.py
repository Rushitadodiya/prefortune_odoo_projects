from odoo import api,fields,models

class Stationarycustomer(models.Model):
    _name="stationary.customer"#table name
    _description="Stationary Customer"
    name=fields.Char(string="name")
    age=fields.Integer(string="age")
    gender=fields.Selection([('male','Male'),('female','Female')],string="gender")
    