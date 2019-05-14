from odoo import models, api


class ReportRjcInvoiceCreditNote(models.AbstractModel):
    _name = 'report.rjc_invoice_credit_note_pdf'
    _description = 'report invoice credit notes'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name(
            'rjc_invoice_credit_note_pdf')
        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(docids),
            'report_type': data.get('report_type') if data else '',
        }
