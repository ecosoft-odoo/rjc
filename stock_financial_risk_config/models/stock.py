# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import _, api, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_confirm(self):
        stock_block = self.env['ir.config_parameter'].sudo()\
            .get_param('stock.stock_block')
        if self.partner_id.risk_exception and stock_block:
            raise ValidationError(_('Financial risk exceeded.'))
        return super(StockPicking, self).action_confirm()

    @api.multi
    def action_assign(self):
        stock_block = self.env['ir.config_parameter'].sudo()\
            .get_param('stock.stock_block')
        if self.partner_id.risk_exception and stock_block:
            raise ValidationError(_('Financial risk exceeded.'))
        return super(StockPicking, self).action_assign()

    @api.multi
    def button_validate(self):
        stock_block = self.env['ir.config_parameter'].sudo()\
            .get_param('stock.stock_block')
        if self.partner_id.risk_exception and stock_block:
            raise ValidationError(_('Financial risk exceeded.'))
        return super(StockPicking, self).button_validate()
