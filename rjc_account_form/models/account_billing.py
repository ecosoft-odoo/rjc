# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, api
from num2words import num2words


class AccountBilling(models.Model):
    _inherit = 'account.billing'

    @api.multi
    def amount_text(self, amount):
        try:
            return num2words(amount, to='currency', lang='th')
        except NotImplementedError:
            return num2words(amount, to='currency', lang='en')

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
            'account_billing.report_account_billing',
        ]
        res = super(AccountBilling, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        if res and view_type in ['tree', 'form']:
            # del menu report customer and vendor
            self.remove_menu_print(res, hide_reports_base)
        return res
