from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    number_preprint = fields.Char(
        string='Preprint Number',
        )
