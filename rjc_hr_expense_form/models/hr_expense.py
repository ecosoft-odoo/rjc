# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, api


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

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
            'hr_expense.action_report_hr_expense_sheet',
        ]
        res = super(HrExpenseSheet, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        if res and view_type in ['tree', 'form']:
            # del menu report customer and vendor
            self.remove_menu_print(res, hide_reports_base)
        return res
