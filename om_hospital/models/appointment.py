from odoo import api,fields,models,_
from odoo.exceptions import ValidationError
import random


class Hospitalappointment(models.Model):

     _name = "hospital.appointment"#table name
     _inherit=['mail.thread','mail.activity.mixin']
     _description = "Hospital appointment"
     _rec_name="active_id"

    #  name=fields.Many2one('hospital.patient',string="Patient")
     patient_id=fields.Many2one('hospital.patient',string="Patient",ondelete="restrict")
     gender=fields.Selection(related='patient_id.gender',readonly=False)
     appointment_time=fields.Datetime(string="Appointment time",default=fields.Datetime.now)
     booking_date=fields.Date(string="Booking date",default=fields.Date.context_today)
     ref=fields.Char(string="Reference",default="Rushita Dodiya",help="Reference of the patient")
     prescription=fields.Html(string="prescription")
     active_id=fields.Char(string="Active Id")
     priority=fields.Selection([
          ('0','normal'),
          ('1','low'),
          ('2','high'),
          ('3','very high')],string="priority")
     state=fields.Selection([
          ('draft','Draft'),
          ('in_consulation','In_consulation'),
          ('done','Done'),
          ('cancel','Canceled')],default="draft",string="status",required=True)
     
     doctor_id=fields.Many2one('res.users',string="Doctor")
     pharmacy_line_ids=fields.One2many('appointment.pharmacy.lines','appointment_id',string="pharmacy lines")
     hide_sales_price=fields.Boolean(string="Hide sales price")
     operation=fields.Many2one('hospital.operation',string="operation")
     progress=fields.Integer(string="progress",compute="_compute_progress")
     duration=fields.Float(string="duration")

     def unlink(self):
          for rec in self:
               print("TEST............................")
               if rec.state != 'draft':
                    raise ValidationError(_('you can only delete records in the draft status'))
          return super(Hospitalappointment,self).unlink()


     @api.model
     def create(self,vals):
          vals['active_id']=self.env['ir.sequence'].next_by_code('hospital.appointment')
          return super(Hospitalappointment,self).create(vals)
     
     @api.onchange('patient_id')
     def _onchange_patient_id(self):
          self.ref=self.patient_id.ref

     def action_test(self):
          print("button clicked...........!")
          return{
               'effect':
               {
                    'fadeout':'slow',
                    'message':'click success',
                    'type':'rainbow_man',
               }
          }

     def action_in_consultation(self):
          for rec in self:
                if rec.state == "draft":
                    rec.state='in_consulation'
     
     def action_done(self):
          for rec in self:
               rec.state='done'
     
     def action_cancel(self):
          action=self.env.ref('om_hospital.action_cancel_appointment').read()[0]
          return action

     def action_draft(self):
          for rec in self:
               rec.state='draft'

     @api.depends('state')
     def _compute_progress(self):
          for rec in self:
               if rec.state=='draft':
                    # progress=25
                     progress=random.randrange(0,25)
               elif rec.state=='in_consulation':
                    # progress=50
                      progress=random.randrange(25,75)
               elif rec.state=='done':
                    progress=100
               else :
                    progress=0
               rec.progress=progress



class HospitalPharmacylines(models.Model):

     _name = "appointment.pharmacy.lines"#table name
     _description="appointment.pharmacy.lines"

     product_id=fields.Many2one('product.product',required=True)
     price_unit=fields.Float(related='product_id.list_price')
     qty=fields.Integer(string="Quantity",default=1)
     appointment_id=fields.Many2one('hospital.appointment',string="appointment")