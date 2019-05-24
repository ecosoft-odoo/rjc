# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, models
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        for invoice in self.filtered(lambda x: x.type in (
                'out_invoice', 'out_refund') and x.amount_total_signed > 0.0):
            exception_msg = invoice.risk_exception_msg()
            if self.company_id.invoice_block and exception_msg:
                raise ValidationError(exception_msg)
        return super(AccountInvoice, self).action_invoice_open()
