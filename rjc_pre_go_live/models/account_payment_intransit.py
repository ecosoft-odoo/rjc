# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class AccountPaymentIntransit(models.Model):
    _inherit = 'account.payment.intransit'

    intransit_line_ids = fields.One2many(
        readonly=False,
    )
