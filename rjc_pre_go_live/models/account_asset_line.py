# Copyright 2009-2018 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountAssetLine(models.Model):
    _inherit = 'account.asset.line'

    line_days = fields.Integer(
        readonly=False
    )
