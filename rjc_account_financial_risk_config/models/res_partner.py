# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, models

GROUP_SECURITY = [
    'account.group_account_manager',
    'rjc_account_financial_risk_config.group_account_financial_risk'
]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _compute_risk_allow_edit(self):
        is_editable = self.env.user.has_group(GROUP_SECURITY[0]) or \
            self.env.user.has_group(GROUP_SECURITY[1])
        for partner in self.filtered('customer'):
            partner.risk_allow_edit = is_editable
