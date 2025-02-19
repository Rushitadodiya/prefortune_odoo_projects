from odoo import api,fields,models

class simplecontact(models.Model):
    _name="simple.contact"
    _inherit=['mail.thread','mail.activity.mixin']
    _description="To store and view detailed contact information"
    _rec_name="contact_name"
    
    contact_name=fields.Char(string="Contact Name",tracking=True)
    phone=fields.Char(string="phone Number",tracking=True)
    email=fields.Char(string="Email Address",tracking=True)
    address=fields.Text(string="Physical Address",tracking=True)
    company_name=fields.Char(string="Company_Name",tracking=True)
    birthday=fields.Date(string="Birthday")
    notes=fields.Html(string="Notes")
    contact_type=fields.Selection([
        ('personal','Personal'),
        ('business','Business')],string="contact_type",tracking=True)
    active=fields.Boolean(string="Active",default=True)

