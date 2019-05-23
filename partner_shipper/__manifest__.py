# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
{
    'name': 'Partner Shipper',
    'summary': 'Set on partners shipper for delivery goods',
    'version': '12.0.1.0.0',
    'development_status': 'Beta',
    'category': 'Delivery',
    'website': 'https://github.com/ecosoft-odoo/addons',
    'author': 'Ecosoft,'
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'sale_stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/partner_shipper_view.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/stock_picking_view.xml',
        'views/report_deliveryslip.xml',
        'views/report_shipping.xml',
        'views/account_invoice_view.xml',
    ],
}
