from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    pre_print_no = fields.Char(
        string='Pre-Print Number',
        )
