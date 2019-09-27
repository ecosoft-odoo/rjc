# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    number_preprint = fields.Char(
        string='Preprint Number',
        )
    comment = fields.Text(
        readonly=False,
    )
    reference = fields.Char(
        readonly=False,
    )

    @api.model
    def default_get(self, default_fields):
        """ Override partner_bank_id in refund for invoice netting
            Create directly
        """
        res = super().default_get(default_fields)
        res['partner_bank_id'] = False
        return res

    @api.model
    def create(self, vals):
        """ Override partner_bank_id in refund for invoice netting
            Create from Vendor Bills
        """
        res = super().create(vals)
        if res.partner_bank_id:
            res.partner_bank_id = False
        return res

    @api.multi
    def action_invoice_open(self):
        """ If invoice line has account_id in Fixed asset,
            user must fill in account asset profile.
        """
        fixed_asset = self.invoice_line_ids.filtered(
            lambda l: l.account_id.asset_profile_id)
        if fixed_asset.filtered(lambda l: not l.asset_profile_id):
            raise UserError(_("Please fill in asset profile"))
        return super().action_invoice_open()
