# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    'name': 'RJC Account',
    'summary': 'Modify field in account module',
    'version': '12.0.1.0.1',
    'category': 'Account',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'installable': True,
    'depends': [
        'account',
        'account_billing',
        'account_payment_netting',
        'account_payment_intransit',
        'l10n_th_withholding_tax_cert',
    ],
    'data': [
        'views/account_invoice_view.xml',
        'views/account_payment_view.xml',
        'views/account_billing.xml',
    ],
}
