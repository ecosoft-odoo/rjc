# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    'name': 'Reimbursables with Tax',
    'version': '12.0.1.0.0',
    'author': 'Ecosoft, Odoo Community Association (OCA)',
    'category': 'Accounting & Finance',
    'website': 'https://github.com/ecosoft-odoo/addons',
    'license': 'AGPL-3',
    'depends': [
        'account_invoice_reimbursable',
    ],
    'data': [
        'views/account_invoice_view.xml',
    ],
    'installable': True,
}
