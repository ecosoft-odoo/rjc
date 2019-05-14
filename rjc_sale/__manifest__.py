{
    'name': 'RJC Sale',
    'summary': 'Add condition to hidding lock button and autolock sale order',
    'version': '12.0.1.0.0',
    'development_status': 'Beta',
    'category': 'Sale',
    'website': 'https://github.com/ecosoft-odoo/rjc',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'sale',
    ],
    'data': [
        'views/sale_order_view.xml',
    ],
}
