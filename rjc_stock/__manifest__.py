# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    'name': 'RJC Stock',
    'summary': 'Modify field in stock module',
    'version': '12.0.1.1.1',
    'category': 'Warehouse',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'stock',
        'stock_secondary_unit',
    ],
    'data': [
        'views/stock_picking_views.xml',
        'views/stock_move_views.xml',
    ],
}
