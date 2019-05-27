# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, api
from num2words import num2words


class ReportRjcInvoice(models.AbstractModel):
    _name = 'report.rjc_invoice_pdf'
    _description = 'report invoice preprint'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name(
            'rjc_invoice_pdf')
        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(docids),
            'report_type': data.get('report_type') if data else '',
        }


class ReportRjcTaxInvoice(models.AbstractModel):
    _name = 'report.rjc_tax_invoice_pdf'
    _description = 'report tax invoice preprint'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name(
            'rjc_tax_invoice_pdf')
        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(docids),
            'report_type': data.get('report_type') if data else '',
        }


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
