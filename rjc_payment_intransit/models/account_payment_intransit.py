# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api


class AccountPaymentIntransit(models.Model):
    _inherit = 'account.payment.intransit'

    intransit_line_ids = fields.One2many(
        readonly=True,
    )
    bank_journal_id = fields.Many2one(
        required=False,
    )
    payment_id = fields.Many2one(
        comodel_name='account.payment',
        string='Payment Number',
        readonly=True,
    )
    manual_total_amount = fields.Monetary(
        default=lambda self: self._context.get('total_amount', 0.0)
    )


class AccountPaymentIntransitLine(models.Model):
    _inherit = 'account.payment.intransit.line'

    due_date = fields.Date()
    payment_id = fields.Many2one(
        comodel_name='account.payment',
        string='Payment Reference',
        copy=False,
    )

    @api.onchange('payment_intransit_type')
    def onchange_payment_intransit_type(self):
        payment_id = self._context.get('payment_id', False)
        name = self._context.get('name', False)
        if payment_id:
            self.move_line_id = self.env['account.move.line'].search([
                ('payment_id', '=', payment_id),
                ('reconciled', '=', False),
                ('debit', '>', 0),
                ('name', '=', name)])
