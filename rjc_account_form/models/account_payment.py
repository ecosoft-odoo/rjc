# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, api
from num2words import num2words

CURRENCY_NAME = {
    'USD': 'ดอลลาร์',
    'EUR': 'ยูโร',
    'JPY': 'เยน',
}


class account_payment(models.Model):
    _inherit = 'account.payment'

    @api.multi
    def amount_text(self, amount):
        if self.currency_id != self.company_id.currency_id:
            amount = num2words(amount, lang='th')
            currency_name = CURRENCY_NAME[self.currency_id.name]
            text_amount_currency = ''.join([amount, currency_name])
            return text_amount_currency
        return num2words(amount, to='currency', lang='th')

    @api.multi
    def _get_move_line_1(self):
        move_line_id = self.env['account.move.line']
        full_reconcile_id = move_line_id.search(
            [('payment_id', '=', self.id)], order="id").filtered(
            'full_reconcile_id').mapped('full_reconcile_id')
        if full_reconcile_id:
            move_reconcile_id = move_line_id.search([
                ('full_reconcile_id', '=', full_reconcile_id[0].id)]).filtered(
                lambda l: not l.payment_id)
            return move_reconcile_id
        return move_line_id

    @api.multi
    def _get_amount_diff(self, move_line, refund):
        payment_move_line_id = self.env['account.move.line'].search([
            ('payment_id', '=', self.id),
            ('reconciled', '=', True)])
        if refund:
            return move_line.balance * -1
        reconcile_id = self.env['account.partial.reconcile'].search([
            ('credit_move_id', '=', move_line.id),
            ('debit_move_id', '=', payment_move_line_id.id)])
        return reconcile_id.amount

    @api.multi
    def _get_move_line(self, type):
        self.ensure_one()
        refund = False
        move_line = self.env['account.move.line']
        payment_move_line_id = move_line.search([
            ('payment_id', '=', self.id),
            ('reconciled', '=', True)])
        if type == 'outbound':
            reconcile_id = payment_move_line_id.matched_credit_ids
            full_reconcile_id = reconcile_id.mapped(
                'credit_move_id').mapped('full_reconcile_id')
            if any(full_reconcile_id):
                move_line_ids = move_line.search([
                    ('full_reconcile_id', 'in', full_reconcile_id.ids)
                ]).filtered(lambda l: not l.payment_id)
                invoice_ids = move_line_ids.mapped('invoice_id')
                # check case refund
                if invoice_ids and \
                    ('in_refund' in invoice_ids.mapped('type') or
                     'out_refund' in invoice_ids.mapped('type')):
                    refund = True
                res = [refund, move_line_ids]
                return res
        if type == 'inbound':
            reconcile_id = payment_move_line_id.matched_debit_ids
        res = [refund, reconcile_id.mapped('credit_move_id')]
        return res

    @api.multi
    def _get_payment_intransit(self):
        payment_ids = self.env['account.move.line'].search(
            [('payment_id', 'in', self.ids)])
        payment_intransit_obj = self.env['account.payment.intransit.line']
        for payment in payment_ids:
            payment_intransit = payment_intransit_obj.search(
                [('move_line_id', '=', payment.id)])
            if payment_intransit:
                return payment_intransit

    @api.multi
    def _get_payment_amount_multi_diff(self):
        multi_deduc = self.env['account.payment.deduction'].search([
            ('payment_id', '=', self.id)])
        return multi_deduc

    @api.multi
    def remove_menu_print(self, res, reports):
        # Remove reports menu
        for report in reports:
            reports = self.env.ref(report, raise_if_not_found=False)
            for rec in res.get('toolbar', {}).get('print', []):
                if rec.get('id', False) in reports.ids:
                    del res['toolbar']['print'][
                        res.get('toolbar', {}).get('print').index(rec)]
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        hide_reports_base = [
            'account.action_report_payment_receipt',
        ]
        hide_reports_vendor = [
            'rjc_account_form.rjc_receipt_pdf_report',
        ]
        type = self._context.get('default_payment_type', False)
        res = super(account_payment, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        if res and view_type in ['tree', 'form']:
            # del menu report customer and vendor
            self.remove_menu_print(res, hide_reports_base)
            # del menu report vendor
            if type and type not in ['inbound']:
                self.remove_menu_print(res, hide_reports_vendor)
        return res

    def _get_payment_amount_diff(self):
        move_line_id = self.env['account.move.line'].search([
            ('account_id', '=', self.writeoff_account_id.id),
            ('payment_id', '=', self.id)])
        balance = move_line_id.balance * -1
        return balance
