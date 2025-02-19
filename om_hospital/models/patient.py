from odoo import api,fields,models,_
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta



class Hospitalpatient(models.Model):

     _name = "hospital.patient"#table name
     _inherit=['mail.thread','mail.activity.mixin']
     _description = "Hospital patient"
     name=fields.Char(string="name",tracking=True,readonly=True)
     date_of_birth=fields.Date(string="Date of Birth")
     ref=fields.Char(string="Reference",default="Rushita Dodiya")
     age=fields.Integer(string="age",compute="_compute_age", inverse="_inverse_compue_age",search="_search_age",tracking=True)
     gender=fields.Selection([('male','Male'),('female','Female')],string="gender",tracking=True,default="female")#selection is always in tuple of key-value pair
     active=fields.Boolean(string="active",default=True)#archive action 
     image=fields.Image(string="image",attachment=True)
     tag_ids=fields.Many2many('patient.tag',string="Tags")
     appointment_count=fields.Integer(string="Appointment Count",compute="_compute_appointment_count",store=True)
     appointment_ids=fields.One2many('hospital.appointment','patient_id',string="Appointment")
     parent=fields.Char(string="Parent")
     maried_status=fields.Selection([('married','Married'),('single','Single')],string="Marital Status",tracking=True,default="single")
     partner_name=fields.Char(string="Partner Name")
     is_birthday=fields.Boolean(string="Birthday ?",compute="_compute_is_birthday")

     @api.ondelete(at_uninstall=False)
     def check_appointment(self):
          for rec in self:
               if rec.appointment_ids:
                    raise ValidationError(_('You cannot delete a patient with appointment'))
               
     @api.depends('appointment_ids')
     def _compute_appointment_count(self):
          for rec in self:
               rec.appointment_count=self.env['hospital.appointment'].search_count([('patient_id','=',rec.id)])


     def _compute_age(self):
          for rec in self:
               today=date.today()
               if rec.date_of_birth:
                    rec.age=today.year-rec.date_of_birth.year
               else:
                    rec.age=0

     def _inverse_compue_age(self):
          today=date.today()
          for rec in self:
               rec.date_of_birth=today-relativedelta.relativedelta(years=rec.age)

     def _search_age(self,operator,value):
          print("value...............",value)
          date_of_birth=date.today()-relativedelta.relativedelta(years=value)
          print("date_of_birth..........",date_of_birth)
          start_of_year=date_of_birth.replace(day=1,month=1)
          end_of_year=date_of_birth.replace(day=31,month=12)
          print("start_of_year...............",start_of_year)
          print("end_of_year............",end_of_year)
          return [('date_of_birth','>=',start_of_year),('date_of_birth','<=',end_of_year)]
     


     @api.constrains('date_of_birth')
     def check_date_of_birth(self):
          for rec in self:
               if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                    raise ValidationError(_("The entered date of birth is not acceptable"))
               
     def action_test(self):
          print("clicked................")
          return
     

     @api.depends('date_of_birth')
     def _compute_is_birthday(self):
          for rec in self:
               is_birthday=False
               if rec.date_of_birth:
                    today=date.today()
                    if today.day==rec.date_of_birth.day and today.month==rec.date_of_birth.month:
                         is_birthday=True
          rec.is_birthday=is_birthday
                         
          