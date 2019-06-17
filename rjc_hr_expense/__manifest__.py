# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    'name': 'RJC Expense',
    'summary': 'Modify field in expense module',
    'version': '12.0.1.0.0',
    'category': 'Human Resources',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'hr_expense',
    ],
    'data': [
        'views/hr_expense_sheet_register_payment.xml',
    ],
}
