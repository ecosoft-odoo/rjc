# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    'name': 'RJC Purchase Order Form',
    'version': '12.0.1.0.0',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'category': 'Report',
    'depends': [
        'purchase',
        'partner_fax',
        'web',
    ],
    'data': [
        'data/paper_format.xml',
        'data/report_data.xml',
        'reports/purchase_style.xml',
        'reports/purchase_order_layout.xml',
    ],
    'installable': True,
}
