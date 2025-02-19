{
    'name': 'Simple Contact List',#module name
    'version': '1.0.0',
    'category': 'Simple Contact',
    'author':'odoo Rushita',
    'sequence':-100,
    'summary': 'Simple Contact List',#To show the below of module name
    'description': """To store and view detailed contact information.""",
    'depends': ['mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/contact_view.xml',
        'views/add_new_contact_view.xml',
        'views/personal_contact_view.xml',
        'views/business_contact_view.xml',
        'views/contact_activity_view.xml'
    ],
    'demo': [],           
    'installable': True,
    'application':True,
    'assets': {},
    'license': 'LGPL-3',
}