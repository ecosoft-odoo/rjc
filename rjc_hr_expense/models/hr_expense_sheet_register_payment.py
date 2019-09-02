# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class HrExpenseSheetRegisterPaymentWizard(models.TransientModel):
    _inherit = 'hr.expense.sheet.register.payment.wizard'

    value_date = fields.Date()
    payment_ref = fields.Char()
    cheque_no = fields.Char(
        string='Cheque No.'
    )
    notes = fields.Text(
        string='Internal Notes',
    )

    def _get_payment_vals(self):
        res = super()._get_payment_vals()
        active_id = self._context.get('active_id', False)
        res.update({
            'value_date': self.value_date,
            'payment_ref': self.payment_ref,
            'cheque_no': self.cheque_no,
            'notes': self.notes,
            'expense_sheet_id': active_id,
        })
        return res
