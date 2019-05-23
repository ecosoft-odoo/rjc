# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    shipper_id = fields.Many2one(
        comodel_name='partner.shipper',
        string='Shippers',
        ondelete='restrict',
        index=True,
    )
    partner_shipper_ids = fields.Many2many(
        comodel_name='partner.shipper',
        string="Partner's Shippers",
        related='partner_id.shipper_ids',
    )

    @api.onchange('partner_id')
    def _onchange_partner_shipper_id(self):
        self.shipper_id = False
        return {'domain': {'shipper_id':
                [('id', 'in', self.partner_shipper_ids.ids)]}}

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals.update({'shipper_id': self.shipper_id.id})
        return invoice_vals
