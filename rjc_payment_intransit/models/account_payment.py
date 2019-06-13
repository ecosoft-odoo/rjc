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
            intransit_id = \
                record.payment_intransit_line_ids.mapped('intransit_id')
            if intransit_id:
                record.has_intransit = \
                    bool(intransit_id.filtered(lambda l: l.state != 'cancel'))

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

    @api.depends('payment_intransit_line_ids.allocation')
    def _compute_amount_intransit_line_total(self):
        self.amount_intransit_line_total = \
            sum(self.payment_intransit_line_ids.mapped('allocation'))
        if self.amount_intransit_line_total > self.amount:
            raise ValidationError(_(
                'Can not payment balance allocation more than %s'
            ) % self.amount)
        return True

    @api.multi
    def action_payment_intransit(self):
        for rec in self:
            if not rec.payment_intransit_line_ids:
                raise ValidationError(_('Line empty!'))
            intransit = self.env['account.payment.intransit'].create({
                'partner_id': rec.partner_id.id,
                'receipt_date': rec.payment_date,
                'journal_id': rec.journal_id.id,
                'currency_id': rec.currency_id.id,
                'total_amount': rec.amount_intransit_line_total
            })
            intransit_line = self.env['account.payment.intransit.line'].search(
                [('payment_id', '=', rec.id)])
            intransit_line.update({'intransit_id': intransit.id})
        return True
