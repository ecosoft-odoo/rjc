# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
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
        cls.partner_1 = cls.env.ref('base.res_partner_2')  # with shipper
        cls.partner_2 = cls.env.ref('base.res_partner_12')
        cls.product = cls.env.ref('product.product_product_4')
        cls.shipper_a = cls.partner_shipper_model.create({
            'name': 'Shipper A',
            'code': '10',
            'route': 'north',
        })
        cls.shipper_b = cls.partner_shipper_model.create({
            'name': 'Shipper B',
            'code': '11',
            'route': 'south',
        })
        cls.shipper_c = cls.partner_shipper_model.create({
            'name': 'Shipper C',
            'code': '11',
            'route': 'northeast',
        })
        cls.partner_1.write({
            'shipper_ids': [(6, 0, [cls.shipper_a.id,
                                    cls.shipper_b.id])]})

    def _create_sale(self, parnter, product, quantity=1.0):
        rslt = self.sale_order_model.create({
            'partner_id': parnter.id,
            'order_line': [
                (0, 0, {
                    'name': product.name,
                    'product_id': product.id,
                    'product_uom_qty': quantity,
                    'product_uom': product.uom_po_id.id,
                    'price_unit': 10,
                })],
        })
        return rslt

    def test_partner_shipper(self):
        """
        SO -> Picking, SO -> Invoice, shipper must pass from doc to doc
        """
        # Create SO with partner 2, and test that are no shippers
        sale_order = self._create_sale(self.partner_2, self.product, 10)
        self.assertFalse(sale_order.partner_shipper_ids)
        sale_order.write({'partner_id': self.partner_1.id,
                          'partner_invoice_id': self.partner_1.id,
                          'partner_shipping_id': self.partner_1.id, })
        valid_shipper_ids = [self.shipper_a.id, self.shipper_b.id]
        res = sale_order._onchange_partner_shipper_id()
        # Test onchange result in valid shipper_ids domain
        self.assertEqual(res['domain']['shipper_id'][0][2], valid_shipper_ids)
        self.assertEqual(sale_order.partner_shipper_ids.ids, valid_shipper_ids)
        sale_order.shipper_id = self.shipper_a  # Assign shipper
        # Confirm SO, new DO is created
        sale_order.action_confirm()
        self.assertEqual(len(sale_order.picking_ids), 1)
        picking = sale_order.picking_ids[0]
        self.assertEqual(picking.partner_shipper_ids.ids, valid_shipper_ids)
        self.assertEqual(picking.shipper_id, self.shipper_a)  # Test shipper
        res = picking._onchange_partner_shipper_picking_id()
        self.assertEqual(res['domain']['shipper_id'][0][2], valid_shipper_ids)
        picking.shipper_id = self.shipper_a  # Assign shipper after cleared
        picking.move_ids_without_package[0].write({'quantity_done': 10.0})
        picking.button_validate()
        # Create Invoice from SO
        ctx = {
            'active_model': 'sale.order',
            'active_ids': [sale_order.id],
            'active_id': sale_order.id,
        }
        wizard = self.sale_payment_invoice_model.with_context(ctx).create({
            'advance_payment_method': 'delivered',
        })
        wizard.with_context(ctx).create_invoices()
        self.assertEqual(len(sale_order.invoice_ids), 1)
        invoice = sale_order.invoice_ids[0]
        self.assertEqual(invoice.shipper_id, self.shipper_a)  # Test shipper
        # Test domain, incase partner is changed
        res = invoice._onchange_partner_invoice_shipper_id()
        self.assertEqual(res['domain']['shipper_id'][0][2], valid_shipper_ids)
        self.assertEqual(invoice.partner_shipper_ids.ids, valid_shipper_ids)

    def test_down_payment(self):
        # Create SO with partner 2, and test that are no shippers
        sale_order = self._create_sale(self.partner_1, self.product, 10)
        sale_order.shipper_id = self.shipper_a  # assign shipper

        ctx = {
            'active_model': 'sale.order',
            'active_ids': [sale_order.id],
            'active_id': sale_order.id,
        }
        wizard = self.sale_payment_invoice_model.with_context(ctx).create({
            'advance_payment_method': 'percentage',
            'amount': 10.0,
        })
        wizard.with_context(ctx).create_invoices()
        self.assertEqual(len(sale_order.invoice_ids), 1)
        invoice = sale_order.invoice_ids[0]
        self.assertEqual(invoice.invoice_line_ids[0].price_unit, 10.0)
        self.assertEqual(invoice.shipper_id, self.shipper_a)
