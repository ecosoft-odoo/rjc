# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import models, api, _
from odoo.exceptions import ValidationError


class CreateWithholdingTaxCert(models.TransientModel):
    _inherit = 'create.withholding.tax.cert'

    @api.multi
    def create_wt_cert(self):
        self.ensure_one()
        active_id = self._context.get('active_id', [])
        wht_id = self.env['withholding.tax.cert'].search([
            ('payment_id', '=', active_id)])
        if wht_id:
            raise ValidationError(_(
                'Payment create withholding tax cert already!'))
        return super().create_wt_cert()
