# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import SavepointCase
from odoo.exceptions import ValidationError


class TestHrExpensePaymentDifference(SavepointCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.expense_model = self.env['hr.expense']
        self.expense_sheet_model = self.env['hr.expense.sheet']
        # self.register_payments_model = self.env['account.register.payments']

        self.product = self.env.ref("product.product_product_4")

        self.employee_1 = self.env['hr.employee'].create({
            'name': 'Employee 1',
        })

        self.expense_1 = self.create_expense(self, 'Expense Test1')
        self.expense_2 = self.create_expense(self, 'Expense Test2')
        self.sheet = self.expense_sheet_model.create({
            'name': 'Report Expense 1',
            'employee_id': self.employee_1.id,
        })

    def create_expense(self, name):
        """ Returns an open expense """
        expense = self.expense_model.create({
            'name': name,
            'employee_id': self.employee_1.id,
            'product_id': self.product.id,
            'unit_amount': self.product.standard_price,
            'quantity': 1,
        })
        expense.action_submit_expenses()
        return expense

    # def create_payment(self, ctx):
    #     register_payments = \
    #         self.register_payments_model.with_context(ctx).create({
    #             'journal_id': self.journal_bank.id,
    #             'payment_method_id': self.payment_method_manual_in.id
    #         })
    #     return register_payments.create_payments()

    def test_1_create_payment_expense(self):
        self.sheet.expense_line_ids = [
            (6, 0, [self.expense_1.id])]
        print("=====11111==========")
        self.sheet.action_submit_sheet()
        print("=====2222==========")
        self.sheet.approve_expense_sheets()
        print(self.sheet.state)
        print("=====333==========")
        self.sheet.action_sheet_move_create()
        print("=====444==========")
        print(self.sheet.state)
        print("===============")
        x=1/0

    # def test_2_invoice_currency(self):
    #     ctx1 = {'active_model': 'account.invoice',
    #             'active_ids': [self.inv_1.id, self.inv_3.id],
    #             'bill_type': 'out_invoice'}
    #     with self.assertRaises(ValidationError):
    #         self.billing_model.with_context(ctx1).create({})
    #     # create billing directly
    #     self.billing_model.create({'partner_id': self.partner_agrolait.id})
    #
    # def test_3_validate_billing_state_not_open(self):
    #     ctx = {'active_model': 'account.invoice',
    #            'active_ids': [self.inv_1.id]}
    #     self.create_payment(ctx)
    #     customer_billing = self.billing_model.with_context(ctx).create({})
    #     with self.assertRaises(ValidationError):
    #         customer_billing.validate_billing()
    #
    # def test_4_billing_fields_view_get(self):
    #     ctx = {'active_model': 'account.invoice',
    #            'active_ids': [self.inv_1.id]}
    #     customer_billing = self.billing_model.with_context(ctx).create({})
    #     # check invoice is billed
    #     with self.assertRaises(ValidationError):
    #         customer_billing.fields_view_get()
    #
    #     self.create_payment(ctx)
    #     # check invoice is state paid
    #     customer_billing = self.billing_model.with_context(ctx).create({})
    #     with self.assertRaises(ValidationError):
    #         customer_billing.fields_view_get()
    #
    # def test_5_create_billing_from_selected_invoices(self):
    #     """ Create two invoices, post it and send context to Billing """
    #     ctx = {'active_model': 'account.invoice',
    #            'active_ids': [self.inv_1.id, self.inv_2.id],
    #            'bill_type': 'out_invoice'}
    #     customer_billing1 = self.billing_model.with_context(ctx).create({})
    #     customer_billing1._onchange_bill_type()
    #     self.assertEqual(customer_billing1.state, 'draft')
    #     customer_billing1.validate_billing()
    #     self.assertEqual(customer_billing1.state, 'billed')
    #     self.assertEqual(customer_billing1.invoice_related_count, 2)
    #     customer_billing1.invoice_relate_billing_tree_view()
    #     customer_billing1.action_cancel()
    #     customer_billing1.action_cancel_draft()
    #
    #     customer_billing2 = self.billing_model.with_context(ctx).create({})
    #     customer_billing2.validate_billing()
    #     self.create_payment(ctx)
    #     with self.assertRaises(ValidationError):
    #         customer_billing2.action_cancel()
