from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    shipper_id = fields.Many2one(
        comodel_name='partner.shipper',
        string='Shippers',
        index=True,
    )
    partner_ids = fields.Many2many(
        related='partner_id.shipper_ids',
    )

    @api.onchange('partner_id')
    def _onchange_partner_shipper_picking_id(self):
        self.shipper_id = False
        return {'domain': {'shipper_id':
                [('id', 'in', self.partner_id.shipper_ids.ids)]}}
