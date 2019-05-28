# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, api
from num2words import num2words


class account_payment(models.Model):
    _inherit = 'account.payment'

    @api.multi
    def amount_text(self, amount):
        try:
            return num2words(amount, to='currency', lang='th')
        except NotImplementedError:
            return num2words(amount, to='currency', lang='en')

    @api.multi
    def _get_payment_intransit(self):
        payment_ids = self.env['account.move.line'].search(
            [('payment_id', 'in', self.ids)])
        payment_intransit_obj = self.env['account.payment.intransit.line']
        for payment in payment_ids:
            payment_intransit = payment_intransit_obj.search(
                [('move_line_id', '=', payment.id)])
            if payment_intransit:
                return payment_intransit
