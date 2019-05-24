# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
{
    'name': 'RJC Partner Stock Risk Config',
    'summary': 'Config partner risk in stock moves',
    'version': '12.0.1.0.0',
    'category': 'Sales Management',
    'license': 'AGPL-3',
    'author': 'Ecosoft, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'depends': [
        'stock',
        'account_financial_risk'
    ],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
}
