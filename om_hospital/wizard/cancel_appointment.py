from odoo import api,fields,models,_
import datetime
from odoo.exceptions import ValidationError
class HospitalAppointmentWizard(models.TransientModel):
    _name="cancel.appointment.wizard"
    _discription="cancel appointment wizard"


    @api.model
    def default_get(self,fields):
        print('....................................',fields)
        res=super(HospitalAppointmentWizard,self).default_get(fields)
        res['cancellation_date']=datetime.date.today()
        print('.......................11111',self.env.context.get('active_id'))
        res['appointment_id']=self.env.context.get('active_id')
        return res





    appointment_id=fields.Many2one('hospital.appointment',string="Appoinment",domain="[('state','=','draft'),('priority','in',('0','1',False))]")
    reason=fields.Text(string="Reason")
    cancellation_date=fields.Date(string="Cancellation Date")

    
    def action_cancel(self):
        if self.appointment_id.booking_date == fields.Date.today():
            raise ValidationError(_('Sorry,cancellation is not allowed on the same day of booking'))
        self.appointment_id.state="cancel"
        return{
            'type':'ir.actions.client',
            'tag':'reload',
        }