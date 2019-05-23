# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def register_payment(self, payment_line, writeoff_acc_id=False,
                         writeoff_journal_id=False):
        """ Attempt to reconcile netting first,
        and leave the remaining for normal reconcile """
        if not payment_line.payment_id.netting:
            return super().register_payment(
                payment_line, writeoff_acc_id=writeoff_acc_id,
                writeoff_journal_id=writeoff_journal_id)
        # Case netting payment:
        # 1. create netting lines dr/cr
        # 2. do initial reconcile
        line_to_netting = self.env['account.move.line']
        for inv in self:
            line_to_netting += inv.move_id.line_ids.filtered(
                lambda r: not r.reconciled
                and r.account_id.internal_type in ('payable', 'receivable'))
        payment_move = payment_line.move_id
        # Group amounts by account
        account_groups = line_to_netting.read_group(
            [('id', 'in', line_to_netting.ids)],
            ['account_id', 'debit', 'credit'],
            ['account_id'],
        )
        debtors = []
        creditors = []
        total_debtors = 0
        total_creditors = 0
        for account_group in account_groups:
            balance = account_group['debit'] - account_group['credit']
            group_vals = {
                'account_id': account_group['account_id'][0],
                'balance': abs(balance),
            }
            if balance > 0:
                debtors.append(group_vals)
                total_debtors += balance
            else:
                creditors.append(group_vals)
                total_creditors += abs(balance)
        # Create move lines
        netting_amount = min(total_creditors, total_debtors)
        field_map = {1: 'debit', 0: 'credit'}
        move_lines = []
        for i, group in enumerate([debtors, creditors]):
            available_amount = netting_amount
            for account_group in group:
                if account_group['balance'] > available_amount:
                    amount = available_amount
                else:
                    amount = account_group['balance']
                move_line_vals = {
                    field_map[i]: amount,
                    'partner_id': line_to_netting[0].partner_id.id,
                    'name': payment_move.ref,
                    'account_id': account_group['account_id'],
                    'payment_id': payment_line.payment_id.id,
                }
                move_lines.append((0, 0, move_line_vals))
                available_amount -= account_group['balance']
                if available_amount <= 0:
                    break
        if move_lines:
            payment_move.write({'line_ids': move_lines})
        # Make reconciliation
        for move_line in payment_move.line_ids:
            if move_line == payment_line:  # Keep this for super()
                continue
            to_reconcile = move_line + line_to_netting.filtered(
                lambda x: x.account_id == move_line.account_id)
            to_reconcile.filtered(lambda r: not r.reconciled).reconcile()
        return super().register_payment(
            payment_line.filtered(lambda l: not l.reconciled),
            writeoff_acc_id=writeoff_acc_id,
            writeoff_journal_id=writeoff_journal_id)
