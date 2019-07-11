from odoo.tests.common import TransactionCase
from odoo import fields


class TestReimbursableTax(TransactionCase):
    def setUp(self):
        super().setUp()
        self.currency_eur = self.env.ref('base.EUR')
        self.currency_usd = self.env.ref('base.USD')
        self.main_company = self.env.ref('base.main_company')
        self.env.cr.execute(
            """UPDATE res_company SET currency_id = %s
            WHERE id = %s""",
            (self.main_company.id, self.currency_eur.id),
        )
        self.journal = self.env['account.journal'].create({
            'name': 'Journal',
            'type': 'purchase',
            'code': 'TEST',
        })
        self.partner = self.env['res.partner'].create({
            'supplier': True,
            'name': 'Partner',
        })
        self.reimbursable_partner = self.env['res.partner'].create({
            'supplier': True,
            'name': 'Reimbursable Partner',
        })
        self.product = self.env['product.product'].create({
            'name': 'Product',
        })
        self.reimbursable = self.env['product.product'].create({
            'name': 'Reimbursable',
            'type': 'service',
        })
        self.reimbursable_tax = self.env['account.tax'].search([], limit=1)

    def create_reimbursable(self, amount):
        return (0, 0, {
            'amount': amount,
            'partner_id': self.reimbursable_partner.id,
            'product_id': self.reimbursable.id,
            'name': self.reimbursable.name,
            'account_id': self.product.product_tmpl_id.get_product_accounts(

            )['expense'].id,
            'tax_id': self.reimbursable_tax.id,
        })

    def create_invoice_vals(self, currency_id=None):
        return {
            'partner_id': self.partner.id,
            'account_id': self.partner.property_account_payable_id.id,
            'currency_id': currency_id or self.main_company.currency_id.id,
            'journal_id': self.journal.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'account_id':
                    self.product.product_tmpl_id.get_product_accounts(

                    )['expense'].id,
                'name': self.product.name,
                'price_unit': 100,
            })],
            'reimbursable_ids': [
                self.create_reimbursable(20),
                self.create_reimbursable(60)
            ]
        }

    def test_1_create_reimbursable_with_tax(self):
        invoice = self.complete_check_invoice(100)
        self.assertFalse(invoice.tax_line_ids)
        invoice._onchange_invoice_line_reimbursable_ids()
        self.assertTrue(invoice.tax_line_ids)
        for tax in invoice.tax_line_ids:
            reimburse_id = invoice.reimbursable_ids.filtered(
                lambda l: l.sequence == tax.sequence)
            # sequence between tax line and reimburse are must be 1 only
            self.assertEqual(1, len(reimburse_id))
            self.assertEqual(
                reimburse_id.amount*(tax.tax_id.amount/100), tax.amount)
            self.assertEqual(reimburse_id.amount, tax.base)
        invoice.action_invoice_open()
        move_line_reimburse_tax = invoice.move_id.line_ids.filtered(
            lambda l: l.invoice_tax_line_id.tax_id == self.reimbursable_tax)
        self.assertEqual(2, len(move_line_reimburse_tax))
        for ml in move_line_reimburse_tax:
            # check partner from reimbursable
            self.assertEqual(self.reimbursable_partner, ml.partner_id)

    def test_2_create_reimbursable_currency(self):
        invoice = self.complete_check_invoice(100, self.currency_usd.id)
        self.assertEqual(self.currency_usd, invoice.currency_id)
        currency = invoice.currency_id._convert(
            invoice.amount_total, self.currency_eur,
            invoice.company_id, fields.Date.today())
        self.assertEqual(invoice.amount_total_company_signed, currency)

    def complete_check_invoice(self, amount, currency_id=None):
        invoice = self.env['account.invoice'].with_context(
            default_type='in_invoice', type='in_invoice',
            journal_type='purchase', reimbursable_ids=[
                [0, 0, {'sequence': 1000}], [0, 0, {'sequence': 1001}]]
        ).create(self.create_invoice_vals(currency_id))
        self.assertEqual(invoice.amount_total, 100)
        self.assertEqual(invoice.reimbursable_count, 2)
        self.assertEqual(
            invoice.executable_total,
            amount + sum(invoice.reimbursable_ids.mapped('amount')))
        return invoice
