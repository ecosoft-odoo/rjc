# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import fields, models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    payment_ref = fields.Char(
        states={'draft': [('readonly', False)]},
        readonly=True,
        )
    notes = fields.Text(
        string='Internal Notes',
        states={'draft': [('readonly', False)]},
        readonly=True,
        )


class AccountRegisterPayments(models.TransientModel):
    _inherit = 'account.register.payments'

    payment_ref = fields.Char()
    notes = fields.Text(
        string='Internal Notes',
    )

    @api.multi
    def _prepare_payment_vals(self, invoices):
        values = super()._prepare_payment_vals(invoices)
        values['payment_ref'] = self.payment_ref
        values['notes'] = self.notes
        return values
