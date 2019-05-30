# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, api
from num2words import num2words


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def amount_text(self, amount):
        try:
            return num2words(amount, to='currency', lang='th')
        except NotImplementedError:
            return num2words(amount, to='currency', lang='en')

    @api.multi
    def amount_before_discount(self):
        amount_total = 0.0
        for rec in self.order_line:
            amount_total += rec.product_qty * rec.price_unit
        return amount_total
