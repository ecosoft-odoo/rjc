# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models, api
from odoo.addons import decimal_precision as dp


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    secondary_unit_price = fields.Float(
        digits=dp.get_precision('Product Unit of Measure'),
    )

    @api.multi
    def _create_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._create_stock_moves(picking)
        for rec in self:
            res.update({'secondary_uom_id': rec.secondary_uom_id})
        return res
