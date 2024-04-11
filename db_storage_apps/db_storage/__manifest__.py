# -*- coding: utf-8 -*-
{
    'name': 'File Storage',
    'version': '1.0.0',
    'sequence': -100,
    'summary': """For storing files""",
    'category': 'Storage',
    'license': 'AGPL-3',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/storage_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': True,
}
