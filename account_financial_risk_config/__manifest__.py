# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    'name': 'Account Financial Risk Config',
    'summary': 'config customer risk',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'author': 'Ecosoft, Odoo Community Association (OCA)',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'depends': [
        'account_financial_risk',
        'account',
        'stock',
    ],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
}
