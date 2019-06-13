# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    'name': 'RJC Stock Report',
    'version': '12.0.1.0.0',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'category': 'Report',
    'depends': [
        'web',
        'stock',
    ],
    'data': [
        'data/stock_report_views.xml',
        'reports/deliveryslip_layout.xml',
    ],
    'installable': True,
    'maintainers': ['Saran440'],
}
