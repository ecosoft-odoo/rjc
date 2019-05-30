# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, api
from num2words import num2words


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def amount_text(self, amount):
        try:
            return num2words(amount, to='currency', lang='th')
        except NotImplementedError:
            return num2words(amount, to='currency', lang='en')

    @api.multi
    def amount_before_discount(self):
        amount_total = 0.0
        for rec in self.invoice_line_ids:
            amount_total += rec.quantity * rec.price_unit
        return amount_total

    @api.multi
    def _get_payments_amount(self, payments_widget, payment_id):
        for inv in payments_widget:
            if inv.get('account_payment_id') == payment_id:
                return inv
