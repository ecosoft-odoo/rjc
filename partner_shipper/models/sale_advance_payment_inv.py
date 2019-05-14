from odoo import api, models


class SaleAdvancePayment(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        invoice = super()._create_invoice(order, so_line, amount)
        invoice.write({'shipper_id': order.shipper_id.id})
        return invoice
