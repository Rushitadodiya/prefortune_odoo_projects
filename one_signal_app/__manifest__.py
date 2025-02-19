
{
    'name': "one_signal_app",
    'summary': "one_signal_app",

    'description': """
        Create the users and Push the Notifications in multiple divices
    """,

    'author': "My Company",
    'sequence':-500,
    'website': "https://www.yourcompany.com",
    'category': 'One_signal',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/cron.xml',
        'wizard/pushnotification.xml',
        'wizard/contact_view.xml',
        'views/menu_view.xml',
        'views/settings_view.xml',
        'views/segment_view.xml',
        'views/user_view.xml',
        'views/template_view.xml',
        # 'views/subscription_view.xml'
    ],
    'demo': [],
    'installable': True,
    'application':True,
    'assets': {},
    'license': 'LGPL-3',
}

