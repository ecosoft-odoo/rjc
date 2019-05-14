{
    'name': 'RJC invoice report preprint',
    'version': '12.0.1.0.0',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'website': 'https://github.com/ecosoft-odoo/',
    'category': 'Report',
    'depends': ['account',
                'web',
                ],
    'data': [
        'reports/invoice_layout.xml',
        'reports/invoice_credit_note_layout.xml',
        'data/report_data.xml',
        'data/paper_format.xml',
    ],
    'installable': True,
}
