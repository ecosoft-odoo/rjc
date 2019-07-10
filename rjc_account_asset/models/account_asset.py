# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, api, _
from odoo.exceptions import ValidationError


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    @api.one
    @api.constrains('salvage_value')
    def _check_salvage_value(self):
        if self.salvage_value > self.purchase_value or self.salvage_value < 0:
            raise ValidationError(_(
                'Salvage Value can not value %.2f') % self.salvage_value)
