from odoo import models, fields


class Inventory(models.Model):
    _name = 'stock.inventory'
    _inherit = ['stock.inventory', 'mail.thread', 'mail.activity.mixin']

    state = fields.Selection(
        track_visibility="onchange")
    name = fields.Char(
        track_visibility="onchange")
    filter = fields.Selection(
        track_visibility="onchange")
    product_id = fields.Many2one(
        track_visibility="onchange")
    
