from odoo import models, api
from num2words import num2words


class ReportRjcPo(models.AbstractModel):
    _name = 'report.rjc_purchase_order_pdf'
    _description = 'report PO'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name(
            'rjc_purchase_order_pdf')
        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(docids),
            'report_type': data.get('report_type') if data else '',
        }


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
        return (amount_total)

    @api.multi
    def amount_discount(self):
        amount_total = 0.0
        amount_discount_sum = 0.0
        for rec in self.order_line:
            amount_total += rec.product_qty * rec.price_unit
            amount_discount_sum = amount_total - (self.amount_untaxed)
        return (amount_discount_sum)
