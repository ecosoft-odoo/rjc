# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    'name': 'RJC Account Asset Excel Report',
    'version': '12.0.1.0.0',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'category': 'Report',
    'depends': [
        'excel_import_export',
        'account',
    ],
    'data': [
        'report_asset/xlsx_report_asset.xml',
        'report_asset/templates.xml',
        'data/menu_report.xml',
    ],
    'installable': True,
}
