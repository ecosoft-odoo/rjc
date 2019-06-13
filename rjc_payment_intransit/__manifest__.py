# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    'name': 'RJC Account Payment Intransit',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'summary': 'Manage deposit to the bank',
    'description': 'This module based on account_check_deposit',
    'author': 'Ecosoft, Odoo Community Association (OCA)',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'depends': [
        'account',
        'account_payment_intransit',
    ],
    'data': [
        'views/account_payment_intransit_view.xml',
        'views/account_payment_view.xml',
    ],
    'installable': True,
    'development_status': 'alpha',
    'maintainers': ['Saran440'],
}
