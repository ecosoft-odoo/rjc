# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def line_get_convert(self, line, part):
        val = self.env['product.product']._convert_prepared_anglosaxon_line(
            line, part)
        for record in self.tax_line_ids:
            if line['type'] == 'tax' and record.sequence != 1 and \
                    line['invoice_tax_line_id'] == record.id:
                reimburs_tax = self.reimbursable_ids.filtered(
                    lambda l: l.sequence == record.sequence)
                part = self.env['res.partner']._find_accounting_partner(
                    reimburs_tax.partner_id)
                val['partner_id'] = part.id
        return val

    @api.onchange('invoice_line_ids', 'reimbursable_ids')
    def _onchange_invoice_line_reimbursable_ids(self):
        taxes_grouped = self.get_taxes_values()
        tax_lines = self.tax_line_ids.filtered('manual')
        # check invoice line
        for tax in taxes_grouped.values():
            tax_lines += tax_lines.new(tax)
        # check reimbursable
        sequence = 10
        for line in self.reimbursable_ids:
            for tax in line.mapped('account_line_tax_ids'):
                amount_tax = line.amount * (tax.amount/100)
                val = {
                    'invoice_id': self.id,
                    'name': line.name,
                    'tax_id': tax.id,
                    'amount': amount_tax,
                    'base': line.amount,
                    'account_id': tax.account_id.id,
                    'sequence': sequence
                }
                line.sequence = sequence
                tax_lines += tax_lines.new(val)
                sequence += 1
        self.tax_line_ids = tax_lines
        return


class AccountInvoiceReimbursable(models.Model):
    _inherit = 'account.invoice.reimbursable'

    account_line_tax_ids = fields.Many2one(
        'account.tax',
        string='Tax',
        copy=False,
    )
    sequence = fields.Integer(
        help='For relationship with account.invoice.tax',
    )
