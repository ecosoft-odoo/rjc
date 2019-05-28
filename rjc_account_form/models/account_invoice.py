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

    @api.multi
    def remove_menu_print(self, res, reports):
        # Remove reports if its not Customer
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
            if type not in ['out_invoice', 'out_refund']:
                self.remove_menu_print(res, hide_reports_vendor)
            # del menu report customer invoice
            if type != 'out_refund':
                self.remove_menu_print(res, hide_reports_customer_invoice)
            # del menu report customer refund
            if type != 'out_invoice':
                self.remove_menu_print(res, hide_reports_customer_refund)
        return res
