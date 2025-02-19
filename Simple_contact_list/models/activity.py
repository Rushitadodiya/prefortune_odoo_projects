from odoo import api,fields,models

class simpleactivity(models.Model):
    _name="simple.activity"
    _inherit=['mail.thread','mail.activity.mixin']
    _description="To create and view activity of contact"
    _rec_name="customer_id"

    customer_id=fields.Many2one('simple.contact',string="Contact Name")
    phone=fields.Char(related="customer_id.phone",string="phone Number",tracking=True)
    email=fields.Char(related="customer_id.email",string="Email Address",tracking=True)
    address=fields.Text(related="customer_id.address",string="Physical Address",tracking=True)
    company_name=fields.Char(related="customer_id.company_name",string="Company_Name",tracking=True)
    contact_type=fields.Selection([
        ('personal','Personal'),
        ('business','Business')],related="customer_id.contact_type",string="contact_type",tracking=True)
    priority=fields.Selection([('0','Normal'),('1','Low'),('2','High'),('3','Very high')],string="Priority")
    activity_datetime=fields.Datetime(string="Activity Datetime",default=fields.Datetime.now)
    notes=fields.Html(string="Notes")