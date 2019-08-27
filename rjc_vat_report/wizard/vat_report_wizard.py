# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import models, fields


class VatReportWizard(models.TransientModel):
    _inherit = 'vat.report.wizard'

    tax_id = fields.Many2one(
        domain=[('tax_exigibility', '=', 'on_invoice'),
                ('type_tax_use', 'in', ['sale', 'purchase']),
                ('include_base_amount', '=', False)],
    )
