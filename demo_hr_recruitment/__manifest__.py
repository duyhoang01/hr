# -*- coding: utf-8 -*-
{
    'name': "Hr Recruitment",
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
    'depends': ['base', 'hr', 'hr_recruitment', 'mail'],
    'data': [
        # 'security/ir.model.access.csv',
        'security/data_group.xml',
        'views/template.xml',
        'views/hr_job_view.xml',
        'views/hr_recruitment_stage_views.xml',
        'views/hr_applicant_views.xml',
        # 'views/hr_recruitment_request.xml',
    ],
    'demo': [],
    'qweb': [],
    'auto_install': False,
    'application': True,
    'installable': True,
}
