# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def line_get_convert(self, line, part):
        res = super().line_get_convert(line, part)
        for record in self.tax_line_ids:
            if line['type'] == 'tax' and record.sequence >= 1000 and \
                    line['invoice_tax_line_id'] == record.id:
                reimburse_tax = self.reimbursable_ids.filtered(
                    lambda l: l.sequence == record.sequence)
                reimburse_tax.ensure_one()
                part = self.env['res.partner']._find_accounting_partner(
                    reimburse_tax.partner_id)
                res['partner_id'] = part.id
        return res

    @api.multi
    def compute_invoice_totals(self, company_currency, invoice_move_lines):
        total = 0
        total_currency = 0
        for line in invoice_move_lines:
            if self.currency_id != company_currency:
                currency = self.currency_id
                date = self._get_currency_rate_date() or \
                    fields.Date.context_today(self)
                if not (line.get('currency_id') and
                        line.get('amount_currency')):
                    line['currency_id'] = currency.id
                    line['amount_currency'] = currency.round(line['price'])
                    line['price'] = currency._convert(
                        line['price'], company_currency, self.company_id, date)
            else:
                line['currency_id'] = False
                line['amount_currency'] = False
                line['price'] = self.currency_id.round(line['price'])
            if self.type in ('out_invoice', 'in_refund'):
                total += line['price']
                total_currency += line['amount_currency'] or line['price']
                line['price'] = - line['price']
            else:
                total -= line['price']
                total_currency -= line['amount_currency'] or line['price']
        return total, total_currency, invoice_move_lines

    @api.multi
    def finalize_invoice_move_lines(self, move_lines):
        res = super().finalize_invoice_move_lines(move_lines)
        for reimbursable in self.reimbursable_ids.filtered(
            lambda r: r.amount != 0
        ):
            res.append((0, 0, self.line_get_convert(
                reimbursable._invoice_reimbursable_credit_move_line_get(),
                reimbursable.partner_id.id
            )))
        return res

    @api.onchange('invoice_line_ids', 'reimbursable_ids')
    def _onchange_invoice_line_reimbursable_ids(self):
        taxes_grouped = self.get_taxes_values()
        tax_lines = self.tax_line_ids.filtered('manual')
        # check invoice line
        for tax in taxes_grouped.values():
            tax_lines += tax_lines.new(tax)
        # check reimbursable
        reimbursable_ids = self._context.get('reimbursable_ids', False)
        sequence = False
        if reimbursable_ids:
            sequence = max(list(map(
                lambda x: x[0] == 0 and x[2] and x[2]['sequence'],
                reimbursable_ids)))
        elif self.reimbursable_ids:
            self.reimbursable_ids = False
        for line in self.reimbursable_ids:
            if line.tax_id and sequence:
                sequence += 1
                amount_tax = line.amount * (line.tax_id.amount/100)
                val = {
                    'invoice_id': self.id,
                    'name': line.tax_id.name,
                    'tax_id': line.tax_id.id,
                    'amount': amount_tax,
                    'account_id': line.tax_id.account_id.id,
                    'sequence': sequence,
                }
                tax_lines += tax_lines.new(val)
                line.sequence = sequence
        self.tax_line_ids = tax_lines
        return


class AccountInvoiceReimbursable(models.Model):
    _inherit = 'account.invoice.reimbursable'

    tax_id = fields.Many2one(
        comodel_name='account.tax',
        domain=[
            ('type_tax_use', '=', 'purchase'),
            ('tax_exigibility', '=', 'on_invoice')
        ],
        ondelete='restrict',
    )
    sequence = fields.Integer(
        default=1000,
        help="This sequence start with 1000, to ensure it is specially used \
        to keep relation with account.invoice.tax",
    )

    @api.multi
    def _invoice_reimbursable_move_line_get(self):
        res = super()._invoice_reimbursable_move_line_get()
        if self.tax_id:
            res['tax_ids'] = [(4, self.tax_id.id)]
        return res

    @api.multi
    def _invoice_reimbursable_credit_move_line_get(self):
        self.ensure_one()
        amount = False
        currency_id = False
        amount_currency = False
        if self.currency_id != self.company_id.currency_id:
            amount = self.currency_id._convert(
                self.amount, self.company_id.currency_id,
                self.company_id, fields.Date.today())
            currency_id = self.currency_id.id
            amount_currency = self.amount
        return {
            'reimbursable_id': self.id,
            'type': 'reimbursable',
            'partner_id': self.partner_id.id,
            'name': self.name.split('\n')[0][:64],
            'price_unit': self.amount,
            'quantity': 1,
            'price': -amount or -self.amount,
            'currency_id': currency_id or False,
            'amount_currency': amount_currency or False,
            'account_id': self.account_id.id,
            'product_id': self.product_id.id,
            'uom_id': self.product_id.uom_id.id,
            'account_analytic_id': self.account_analytic_id.id,
            'invoice_id': self.invoice_id.id,
            'analytic_tag_ids': [(4, analytic_tag.id, None)
                                 for analytic_tag in self.analytic_tag_ids]
        }


class AccountInvoiceTax(models.Model):
    _inherit = 'account.invoice.tax'

    @api.depends('invoice_id.invoice_line_ids', 'invoice_id.reimbursable_ids')
    def _compute_base_amount(self):
        res = super()._compute_base_amount()
        for tax in self:
            tax_reimburse = tax.invoice_id.reimbursable_ids.filtered(
                lambda l: l.sequence == tax.sequence)
            if tax_reimburse:
                tax_reimburse.ensure_one()
                tax.base = tax_reimburse.amount
        return res
