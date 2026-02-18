# -*- coding: utf-8 -*-
{
    'name': "Sales - Blue Sale Extension",
    'category': 'Sale',
    'version': '16.0.0.0',
    'summary': """Module extension to add improved insurance number status authorization.""",
    'description': """
        Module extension to add improved insurance number status authorization.
    """,
    'author': "Edwin Pérez",
    'website': "https://www.linkedin.com/in/edwin-pérez-7ab456229",
    'depends': ['sale', 'product'],
    'data': [
        'security/sale_groups.xml',
        'views/sale_order_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
