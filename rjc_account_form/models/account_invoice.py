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


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

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
        for rec in self.invoice_line_ids:
            amount_total += rec.quantity * rec.price_unit
        return amount_total

    @api.multi
    def _get_payments_widget(self, payments_widget, payment_id, value, type):
        if value == 'net_amount':
            net_amount = [x.get('amount') for x in payments_widget
                          if x.get('account_payment_id') < payment_id]
            if self.type == type:
                return self.amount_total - sum(net_amount)
            else:
                return -(self.amount_total - sum(net_amount))
        if value == 'paid':
            payment_paid = [x.get('amount') for x in payments_widget
                            if x.get('account_payment_id') < payment_id]
            if self.type == type:
                return sum(payment_paid)
            else:
                return -sum(payment_paid)
        if value == 'amount':
            payment_amount = [x.get('amount') for x in payments_widget
                              if x.get('account_payment_id') == payment_id]
            if self.type == type:
                return sum(payment_amount)
            else:
                return -sum(payment_amount)

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
        hide_reports_base = [
            'account.account_invoices',
            'account.account_invoices_without_payment',
        ]
        hide_reports_vendor = [
            'rjc_account_form.rjc_invoice_preprint_pdf_report',
            'rjc_account_form.rjc_invoice_credit_note_pdf_report',
            'rjc_account_form.rjc_tax_invoice_pdf_report',
        ]
        hide_reports_customer_invoice = [
            'rjc_account_form.rjc_invoice_credit_note_pdf_report',
        ]
        hide_reports_customer_refund = [
            'rjc_account_form.rjc_invoice_preprint_pdf_report',
            'rjc_account_form.rjc_tax_invoice_pdf_report',
        ]
        type = self._context.get('type')
        res = super(AccountInvoice, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        if res and view_type in ['tree', 'form']:
            # del menu report customer and vendor
            self.remove_menu_print(res, hide_reports_base)
            # del menu report vendor
            if type and type not in ['out_invoice', 'out_refund']:
                self.remove_menu_print(res, hide_reports_vendor)
            # del menu report customer invoice
            if type and type != 'out_refund':
                self.remove_menu_print(res, hide_reports_customer_invoice)
            # del menu report customer refund
            if type and type != 'out_invoice':
                self.remove_menu_print(res, hide_reports_customer_refund)
        return res
