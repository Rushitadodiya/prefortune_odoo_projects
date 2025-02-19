{
    'name':'Employee Performance Tracker',
    'version': '1.0.0',
    'category': 'Employee Performance',
    'author':'odoo Rushita',
    'sequence':-50,
    'summary': 'Employee Performance ',#To show the below of module name
    'description': """Employee Performance system""",
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/employee.xml',
    ],
    'demo': [],           
    'installable': True,
    'application':True,
    'assets': {},
    'license': 'LGPL-3',
    
}