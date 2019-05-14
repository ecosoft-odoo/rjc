from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    shipper_id = fields.Many2one(
        comodel_name='partner.shipper',
        string='Shippers',
        ondelete='restrict',
        index=True,
    )
    partner_ids = fields.Many2many(
        related='partner_id.shipper_ids',
    )

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.shipper_id = False
        return {'domain': {'shipper_id':
                [('id', 'in', self.partner_id.shipper_ids.ids)]}}

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals.update({'shipper_id': self.shipper_id.id})
        return invoice_vals
