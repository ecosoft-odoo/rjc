{
    'name': 'RJC Purchase Order form',
    'version': '12.0.1.0.0',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'category': 'Report',
    'depends': [
        'purchase',
        'partner_fax',
        'web',
    ],
    'data': [
        'reports/purchase_order_layout.xml',
        'data/report_data.xml',
        'data/paper_format.xml',
    ],
    'installable': True,
}
