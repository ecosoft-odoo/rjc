# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    shipper_id = fields.Many2one(
        comodel_name='partner.shipper',
        string='Shippers',
        index=True,
    )
    partner_shipper_ids = fields.Many2many(
        comodel_name='partner.shipper',
        string="Partner's Shippers",
        related='partner_id.shipper_ids',
    )

    @api.onchange('partner_id')
    def _onchange_partner_shipper_picking_id(self):
        self.shipper_id = False
        return {'domain': {'shipper_id':
                [('id', 'in', self.partner_shipper_ids.ids)]}}
