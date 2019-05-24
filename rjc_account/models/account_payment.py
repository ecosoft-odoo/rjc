# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import fields, models


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
