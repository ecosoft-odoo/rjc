# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    'name': 'RJC Account Report',
    'version': '12.0.1.2.0',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'category': 'Report',
    'depends': [
        'web',
        'account',
        'l10n_th_withholding_tax_cert_form',
    ],
    'data': [
        'data/paper_format.xml',
        'data/report_data.xml',
        'reports/account_style.xml',
        'reports/invoice_preprint_layout.xml',
        'reports/invoice_credit_note_layout.xml',
        'reports/invoice_tax_layout.xml',
        'reports/voucher_layout.xml',
        'reports/payment_voucher_layout.xml',
        'reports/receipt_layout.xml',
        'reports/receipt_voucher_layout.xml',
        'reports/wht_cert_layout.xml',
        'reports/billing_layout.xml',
    ],
    'installable': True,
}
