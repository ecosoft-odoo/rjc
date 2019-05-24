# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('state', 'order_line.invoice_status',
                 'order_line.invoice_lines')
    def _get_invoiced(self):
        super(SaleOrder, self)._get_invoiced()
        for rec in self:
            if rec.invoice_status == 'invoiced':
                pickings = rec.picking_ids.filtered(
                    lambda l: l.state in ['done', 'cancel'])
                if rec.state != 'done' and pickings:
                    rec._write({'state': 'done'})
