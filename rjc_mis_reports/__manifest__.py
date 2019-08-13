# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
{
    'name': 'RJC MIS Builder templates',
    'summary': """
        MIS Builder templates for the RJC P&L and Balance Sheets""",
    'author': 'Ecosoft,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'category': 'Reporting',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'mis_builder',  # OCA/account-financial-reporting
    ],
    'data': [
        'data/mis_report_styles.xml',
        'data/mis_report_pl.xml',
        'data/mis_report_bs.xml',
    ],
    'installable': True,
}
