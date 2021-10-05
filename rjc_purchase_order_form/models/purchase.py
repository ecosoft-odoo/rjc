# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, api
from num2words import num2words

CURRENCY_NAME = {
    'USD': 'ดอลลาร์',
    'EUR': 'ยูโร',
    'JPY': 'เยน',
    'CNY': 'หยวน',
}


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def amount_text(self, amount):
        if self.currency_id != self.company_id.currency_id:
            amount = num2words(amount, lang='th')
            currency_name = CURRENCY_NAME[self.currency_id.name]
            text_amount_currency = ''.join([amount, currency_name])
            return text_amount_currency
        return num2words(amount, to='currency', lang='th')

    @api.multi
    def amount_before_discount(self):
        amount_total = 0.0
        for rec in self.order_line:
            amount_total += rec.product_qty * rec.price_unit
        return amount_total

    @api.multi
    def remove_menu_print(self, res, reports):
        # Remove reports menu
        for report in reports:
            reports = self.env.ref(report, raise_if_not_found=False)
            for rec in res.get('toolbar', {}).get('print', []):
                if rec.get('id', False) in reports.ids:
                    del res['toolbar']['print'][
                        res.get('toolbar', {}).get('print').index(rec)]
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        hide_reports_purchase = [
            'purchase.action_report_purchase_order',
            'purchase.report_purchase_quotation',
        ]
        res = super(PurchaseOrder, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        if res and view_type in ['tree', 'form']:
            # del menu report customer and vendor
            self.remove_menu_print(res, hide_reports_purchase)
        return res
