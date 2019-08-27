from odoo import models, api, fields


class PNDReportView(models.TransientModel):
    _name = 'pnd.report.view'
    _description = 'Pnd Report View'
    _inherit = 'withholding.tax.cert.line'

    date = fields.Date()


class ReportPND(models.TransientModel):
    _inherit = 'report.pnd'

    results = fields.Many2many(
        comodel_name='pnd.report.view',
        compute='_compute_results',
    )

    @api.multi
    def _compute_results(self):
        self.ensure_one()
        self._cr.execute("""
            SELECT wht_line.*
            FROM withholding_tax_cert_line wht_line
            JOIN withholding_tax_cert wht ON wht.id = wht_line.cert_id
            WHERE wht.income_tax_form = %s
                AND wht.date >= %s AND wht.date <= %s
            ORDER BY wht.date
        """, (self.income_tax_form, self.date_from, self.date_to))
        Results = self._cr.dictfetchall()
        ReportLine = self.env['pnd.report.view']
        for line in Results:
            self.results += ReportLine.new(line)
