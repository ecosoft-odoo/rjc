# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
{
    'name': 'RJC VAT Reports',
    'version': '12.0.1.0.0',
    'author': 'Ecosoft, Odoo Community Association (OCA)',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'license': 'AGPL-3',
    'category': 'Accounting',
    'depends': [
        'base',
        'l10n_th_vat_report',
        'l10n_th_account_report'
    ],
    'data': [
        'wizard/vat_report_wizard_view.xml'
    ],
    'installable': True,
}
