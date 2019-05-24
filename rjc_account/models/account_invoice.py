# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    number_preprint = fields.Char(
        string='Preprint Number',
        )
