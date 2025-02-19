# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Hospital Managements',#module name
    'version': '1.0.0',
    'category': 'Hospital',
    'author':'odoo Rushita',
    'sequence':-200,
    'summary': 'Hospital management system2',#To show the below of module name
    'description': """Hospital management system1""",
    'depends': ['mail','product'],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'data/patient.tag.csv',
        'data/patient_data.xml',
        'data/sequence_data.xml',
        'wizard/cancel_appointment_view.xml',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/male_patient_view.xml',
        'views/appointment_view.xml',
        'views/patient_tag_view.xml',
        'views/res_config_settings_views.xml',
        'views/operation_view.xml',
        'report/patient_details_template.xml',
        'report/patient_card.xml',
        'report/report.xml',
        
       
    ],
    'demo': [],           
    'installable': True,
    'application':True,
    'assets': {},
    'license': 'LGPL-3',
}
