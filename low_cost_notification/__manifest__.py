{
    'name': 'Low Cost Notification',
    'version': '1.0.0',
    'category': 'Low Cost',
    'author':'odoo mates',
    'sequence':-300,
    'summary': 'Low Cost Notification',
    'description': """Low Cost Notification""",
    'depends':['base','product'],
    'data': ['security/ir.model.access.csv',
            'data/cron.xml',
            'views/menu.xml',
             'views/low_cost_view.xml',
             'views/res_config_settings_views.xml'],
    'demo': [],           
    'installable': True,
    'application':True,
    'assets': {},
    'license': 'LGPL-3',
}