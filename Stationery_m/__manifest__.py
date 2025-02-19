{
    'name':'Stationary Management',
    'version':'1.0.0',
    'category': 'Stationary',
    'author':'odoo Rushita',
    'sequence':-99,
    'summary': 'Stationary management system',
    'description': """Stationary management system""",
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/customer_view.xml',
        'views/male_customer_view.xml',
        'views/female_customer_view.xml'
    ],
    'demo': [],           
    'installable': True,
    'application':True,
    'assets': {},
    'license': 'LGPL-3',
}