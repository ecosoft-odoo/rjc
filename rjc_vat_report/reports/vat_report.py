# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import api, fields, models


class VatReportView(models.TransientModel):
    _name = 'vat.report.view'
    _description = 'Vat Report View'
    _inherit = 'account.move.line'
    _order = 'id'

    base_amount = fields.Monetary(
        currency_field='currency_id',
    )
    tax_amount = fields.Monetary(
        currency_field='currency_id',
    )
    tax_date = fields.Char()


class VatReport(models.TransientModel):
    _inherit = 'report.vat.report'

    @api.multi
    def _compute_results(self):
        self.ensure_one()
        self._cr.execute("""
            SELECT aml.id as id, am.company_id, am.name, aml.account_id,
                aml.tax_invoice, aml.partner_id, aml.date, aml.tax_date,
                CASE WHEN ai.type in ('out_refund', 'in_refund')
                then -aml.tax_base_amount
                else aml.tax_base_amount end as base_amount,
                CASE WHEN aa.internal_group = 'asset'
                then aml.balance else -aml.balance end as tax_amount
            FROM account_move_line aml
            JOIN account_move am on aml.move_id = am.id
            JOIN account_account aa on aa.id = aml.account_id
            LEFT JOIN account_invoice ai on ai.id = aml.invoice_id
            WHERE aml.tax_line_id is not null and aml.date >= %s and
                aml.date <= %s and aml.company_id = %s and aml.account_id = %s
            ORDER BY aml.tax_date
        """, (self.date_from, self.date_to, self.company_id.id,
              self.account_id.id))
        vat_report_results = self._cr.dictfetchall()
        ReportLine = self.env['vat.report.view']
        for line in vat_report_results:
            self.results += ReportLine.new(line)
