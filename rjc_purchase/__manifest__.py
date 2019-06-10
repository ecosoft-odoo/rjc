# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    'name': 'RJC Purchase',
    'summary': 'Modify field in purchase module',
    'version': '12.0.1.1.0',
    'category': 'Purchases',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'purchase',
        'purchase_order_secondary_unit',
    ],
    'data': [
        'views/purchase_order_views.xml',
    ],
}
