# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import api, models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    invoice_tax_line_id = fields.Many2one(
        comodel_name='account.invoice.tax',
        copy=True,
        ondelete='restrict',
    )

    @api.depends('move_id.line_ids', 'move_id.line_ids.tax_line_id',
                 'move_id.line_ids.debit', 'move_id.line_ids.credit')
    def _compute_tax_base_amount(self):
        res = super()._compute_tax_base_amount()
        for move_line in self:
            if move_line.tax_line_id:
                reimburse_sequence = \
                    [x.sequence for x in move_line.invoice_id.tax_line_ids
                     if x.sequence >= 1000]
                for seq in reimburse_sequence:
                    tax_reimburse_id = \
                        move_line.invoice_id.tax_line_ids.filtered(
                            lambda l: l.sequence == seq)
                    if move_line.invoice_tax_line_id == tax_reimburse_id:
                        move_line.tax_base_amount = abs(tax_reimburse_id.base)
        return res
