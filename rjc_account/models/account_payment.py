# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import fields, models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    value_date = fields.Date(
        required=True,
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    payment_ref = fields.Char(
        states={'draft': [('readonly', False)]},
        readonly=True,
        )
    cheque_no = fields.Char(
        string='Cheque No.',
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    validate_by = fields.Many2one(
        comodel_name='res.users',
        readonly=True,
    )
    notes = fields.Text(
        string='Internal Notes',
        states={'draft': [('readonly', False)]},
        readonly=True,
        )

    @api.multi
    def post(self):
        for payment in self:
            payment.validate_by = self.env.user.id
        return super(AccountPayment, self).post()


class AccountRegisterPayments(models.TransientModel):
    _inherit = 'account.register.payments'

    payment_ref = fields.Char()
    notes = fields.Text(
        string='Internal Notes',
    )
    value_date = fields.Date(
        required=True,
    )
    cheque_no = fields.Char(
        string='Cheque No.',
    )

    @api.multi
    def _prepare_payment_vals(self, invoices):
        values = super()._prepare_payment_vals(invoices)
        values['payment_ref'] = self.payment_ref
        values['notes'] = self.notes
        values['cheque_no'] = self.cheque_no
        values['value_date'] = self.value_date
        return values
