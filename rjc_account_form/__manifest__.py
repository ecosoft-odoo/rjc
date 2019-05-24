{
    'name': 'RJC account report and preprint',
    'version': '12.0.1.0.0',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'category': 'Report',
    'depends': [
        'web',
        'account',
                ],
    'data': [
        'data/paper_format.xml',
        'data/paper_format_tax_invoice.xml',
        'data/report_data.xml',
        'reports/invoice_layout.xml',
        'reports/invoice_credit_note_layout.xml',
        'reports/invoice_tax_layout.xml',
    ],
    'installable': True,
}
