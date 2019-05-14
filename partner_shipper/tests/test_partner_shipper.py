from odoo.tests import SavepointCase


class TestPartnerShipper(SavepointCase):
    at_install = False
    post_install = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_shipper_model = cls.env['partner.shipper']
        cls.invoice_model = cls.env['account.invoice']
        cls.partner_model = cls.env['res.partner']
        cls.sale_order_model = cls.env['sale.order']
        cls.sale_order_line_model = cls.env['sale.order.line']
        cls.sale_payment_invoice_model = cls.env['sale.advance.payment.inv']
        cls.partner_agrolait = cls.env.ref('base.res_partner_2')
        cls.product = cls.env.ref('product.product_product_4')

        cls.shipper_a = cls.partner_shipper_model.create({
            'name': 'Shipper A',
            'code': '10',
            'route': 'north',
            'active': True,
        })
        cls.shipper_b = cls.partner_shipper_model.create({
            'name': 'Shipper B',
            'code': '11',
            'route': 'south',
            'active': True,
        })
        cls.partner_agrolait.shipper_ids = cls.shipper_a.ids

    def _create_sale(self, product, date, quantity=1.0):
        rslt = self.sale_order_model.create({
            'partner_id': self.partner_agrolait.id,
            'shipper_id': self.shipper_a.id,
            'order_line': [
                (0, 0, {
                    'name': product.name,
                    'product_id': product.id,
                    'product_uom_qty': quantity,
                    'product_uom': product.uom_po_id.id,
                    'price_unit': 10,
                })],
            'date_order': date,
        })
        return rslt

    def test_create_quotation(self):
        sale_order = self._create_sale(self.product, '2108-01-01')
        sale_order.action_confirm()
        sale_order.onchange_partner_id()
        self.assertEqual(
            self.sale_order_model.picking_ids.shipper_id,
            self.partner_model.shipper_ids)

        ctx = {
            'active_model': 'sale.order',
            'active_ids': [sale_order.id],
            'shipper_id': sale_order.shipper_id,
        }

        payment = self.sale_payment_invoice_model.with_context(ctx).create({
            'advance_payment_method': 'fixed',
            'amount': 100,
        })
        payment.create_invoices()

        payment = self.sale_payment_invoice_model.with_context(ctx).create({
            'advance_payment_method': 'all',
        })
        payment.create_invoices()
