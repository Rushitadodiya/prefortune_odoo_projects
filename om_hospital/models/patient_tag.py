from odoo import api,fields,models,_

class Hospitalpatienttag(models.Model):

     _name = "patient.tag"#table name
     _description = "patient tag"
     # p_id=fields.Many2one('hospital.patient',string="Name")
     name=fields.Char(string="Tags",required=True)
     active=fields.Boolean(string="Active",default=True,copy=False)
     color=fields.Integer(string="Color")
     color2=fields.Char(string="color2")
     sequnce=fields.Integer(string="Sequence")

     @api.returns('self',lambda value:value.id)
     def copy(self,default=None):
          if default is None:
               default={}
          if not default.get('name'):
               default['name']=_("%s (copy)",self.name)
          default['sequnce']=10
          return super(Hospitalpatienttag,self).copy(default)

     _sql_constraints=[
          ('unique_tag_name','unique(name)','Name must be unique'),
          ('check_sequence','check(sequnce>0)','sequence must be non zero positive number')
          ]
   