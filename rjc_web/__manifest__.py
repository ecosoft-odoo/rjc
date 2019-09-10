# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    'name': 'RJC web',
    'summary': 'Show Database Name',
    'version': '12.0.1.0.0',
    'category': 'Warehouse',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'web',
    ],
    'data': [
        'views/webclient_templates.xml',
    ],
}
