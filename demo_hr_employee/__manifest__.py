# -*- coding: utf-8 -*-
{
    'name': "Hr Employee",
    'version': '0.1',
    'author': 'GiangNC',
    'maintainer': '',
    'website': "http://entrustlab.com",
    'license': '',
    'category': 'Uncategorized',
    'sequence': 1,
    'description': """
            
    """,
    'summary': """""",
    'depends': ['base', 'mail', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        # 'views/mail_channel_views.xml',
        'views/res_partner_views.xml',
        'views/time_sheet_views.xml',
        'views/hr_employee_views.xml',
     ],
    'demo': [],
    'qweb': [],
    'auto_install': False,
    'application': True,
    'installable': True,
}
