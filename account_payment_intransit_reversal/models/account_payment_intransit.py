# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import api, models, _
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _name = 'account.payment.intransit'
    _inherit = ['account.payment.intransit', 'account.document.reversal']

    @api.multi
    def action_intransit_cancel(self):
        """ If cancel method is to reverse, use document reversal wizard
        * Draft invoice, fall back to standard invoice cancel
        * Non draft, must be fully open (not even partial reconciled) to cancel
        """
        cancel_reversal = all(self.mapped('journal_id.is_cancel_reversal'))
        states = self.mapped('state')
        if cancel_reversal and 'draft' not in states:
            return self.reverse_document_wizard()
        return super().action_intransit_cancel()

    @api.multi
    def action_document_reversal(self, date=None, journal_id=None):
        """ Reverse all moves related to this invoice + set state to cancel """
        # Check document state
        if 'cancel' in self.mapped('state'):
            raise ValidationError(
                _('You are trying to cancel the cancelled document'))

        # Set all moves to unreconciled
        if self.move_id:
            self.move_id.button_cancel()
            self.move_id.line_ids.filtered(
                lambda x: x.account_id.reconcile).remove_move_reconcile()
            # Create reverse entries
            self.move_id.reverse_moves(date, journal_id)

        # Set state cancelled and unlink with account.move
        self.write({'move_id': False, 'state': 'cancel'})
        return True
