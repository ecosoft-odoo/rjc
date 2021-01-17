from odoo import models


class MrpUnbuild(models.Model):
    _inherit = 'mrp.unbuild'

    def _generate_produce_moves(self):
        moves = super(MrpUnbuild, self)._generate_produce_moves()
        mrp_operation = self.env["stock.picking.type"].search(
            [("code", "=", "mrp_operation")], limit=1)
        for move in moves:
            move.picking_type_id = mrp_operation
        return moves._action_confirm()
