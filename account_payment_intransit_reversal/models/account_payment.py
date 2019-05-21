# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import api, models, _
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.multi
    def cancel(self):
        """ If cancel method is to reverse, use document reversal wizard """
        cancel_reversal = all(
            self.mapped('move_line_ids.move_id.journal_id.is_cancel_reversal'))
        states = self.mapped('state')
        move_line = self.env['account.move.line'].search([
            ('payment_id', '=', self.id)])
        intransit = self.env['account.payment.intransit.line'].search([
            ('move_line_id', 'in', move_line.ids)]).mapped('intransit_id')
        intransit_state = intransit.mapped('state')
        if cancel_reversal and 'draft' not in states:
            if not all(st in ('draft', 'cancel') for st in intransit_state):
                raise UserError(
                    _('To cancel this payment, make sure all payment intransit'
                      ' are also cancelled.'))
            return self.reverse_document_wizard()
        return super().cancel()
