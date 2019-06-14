# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    payment_intransit_line_ids = fields.One2many(
        comodel_name='account.payment.intransit.line',
        inverse_name='payment_id',
        states={'done': [('readonly', True)]},
    )
    amount_intransit_line_total = fields.Monetary(
        string='Amount Total',
        compute='_compute_amount_intransit_line_total',
        readonly=True
    )
    has_intransit = fields.Boolean(
        compute='_compute_count_payment_intransit_ids',
        help='Technical field used for usability purposes'
    )

    @api.depends('payment_intransit_line_ids.intransit_id')
    def _compute_count_payment_intransit_ids(self):
        for record in self:
            intransit_id = record.payment_intransit_line_ids.mapped(
                'intransit_id').filtered(lambda l: l.state != 'cancel')
            payment_id = record.env['account.payment.intransit.line'].search([
                ('move_line_id.payment_id', '=', record.id),
                ('intransit_id', '!=', False),
                ('intransit_id.state', '!=', 'cancel')])
            if intransit_id or payment_id:
                record.has_intransit = True

    @api.multi
    def payment_intransit_tree_view(self):
        self.ensure_one()
        move_line = self.env['account.payment.intransit.line'].search([
            ('move_line_id.payment_id', '=', self.id)])
        action = self.env.ref(
            'account_payment_intransit.action_payment_intransit_tree')
        result = action.read()[0]
        result.update({'domain': [
            ('id', 'in', move_line.mapped('intransit_id').ids)]})
        return result

    @api.constrains('payment_intransit_line_ids')
    def _check_sum_allocation(self):
        for rec in self:
            allocation = sum(
                rec.payment_intransit_line_ids.mapped('allocation'))
            if allocation != rec.amount:
                raise ValidationError(_(
                    'Amount Total not equal Payment amount'))

    @api.depends('payment_intransit_line_ids.allocation')
    def _compute_amount_intransit_line_total(self):
        self.amount_intransit_line_total = \
            sum(self.payment_intransit_line_ids.mapped('allocation'))
        if self.amount_intransit_line_total > self.amount:
            raise ValidationError(_(
                'Balance allocation must less than %s'
            ) % self.amount)
        return True

    @api.multi
    def action_payment_intransit(self):
        for rec in self:
            if not rec.payment_intransit_line_ids:
                raise ValidationError(_('Line empty!'))
            for line in rec.payment_intransit_line_ids:
                intransit = rec.env['account.payment.intransit'].create({
                    'partner_id': rec.partner_id.id,
                    'payment_date': rec.payment_date,
                    'journal_id': rec.journal_id.id,
                    'currency_id': rec.currency_id.id,
                    'total_amount': line.allocation,
                })
                line.intransit_id = intransit.id
        return True
