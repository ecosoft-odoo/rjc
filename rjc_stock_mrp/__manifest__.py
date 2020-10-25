# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    'name': 'RJC Stock & Mrp',
    'summary': 'Modify field in manufacturing module',
    'version': '12.0.1.0.0',
    'category': 'Manufacturing',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'mrp',
        'rjc_stock',
    ],
    'data': [
        'report/mrp_report_bom_structure.xml',
        'views/product_views.xml',
    ],
}
