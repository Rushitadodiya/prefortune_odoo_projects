from odoo import api,fields,models

class Employeeemployeeper(models.Model):
    _name = "employee.employee_per"#table name
    _description = "Hospital patient"
    name=fields.Char(string="name")
    Department=fields.Char(string="Department")
    Role=fields.Char(string="Role")
    Performance_Score=fields.Float(string="Performance Score")
    Review_Date=fields.Date(string="Review Date")
    Comments=fields.Char(string="Comments")
    
