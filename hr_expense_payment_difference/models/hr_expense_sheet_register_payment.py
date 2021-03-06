# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api


class HrExpenseSheetRegisterPaymentWizard(models.TransientModel):
    _inherit = 'hr.expense.sheet.register.payment.wizard'

    payment_difference = fields.Monetary(
        compute='_compute_payment_difference',
        readonly=True,
    )
    payment_difference_handling = fields.Selection([
        ('open', 'Keep open'),
        ('reconcile', 'Mark invoice as fully paid')],
        default='open',
        string="Payment Difference Handling",
        copy=False,
    )
    writeoff_account_id = fields.Many2one(
        'account.account',
        string="Difference Account",
        domain=[('deprecated', '=', False)],
        copy=False,
    )
    writeoff_label = fields.Char(
        string='Journal Item Label',
        default='Write-Off',
        help='Change label of the counterpart \
            that will hold the payment difference',
    )

    def _get_payment_vals(self):
        res = super(
            HrExpenseSheetRegisterPaymentWizard, self)._get_payment_vals()
        res.update({
            'payment_difference_handling': self.payment_difference_handling,
            'writeoff_account_id': self.writeoff_account_id.id,
            'writeoff_label': self.writeoff_label,
        })
        return res

    @api.multi
    def _compute_payment_amount(self, invoices=None, currency=None):
        active_id = self._context.get('active_id', False)
        expense_sheet = self.env['hr.expense.sheet'].search([
            ('id', '=', active_id)])
        return expense_sheet.total_amount

    @api.depends('amount', 'payment_date', 'currency_id')
    def _compute_payment_difference(self):
        for pay in self:
            pay.payment_difference = \
                pay._compute_payment_amount() - pay.amount
