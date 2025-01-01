from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PropertyHistory(models.Model):
    _name = 'move.product.history'
    _description = 'move history'

    user_id = fields.Many2one('res.users')
    product_id = fields.Many2one('inventory.product')
    quantity = fields.Integer()
    type_operation = fields.Char()
    status = fields.Char()
    responsible_user = fields.Many2one('res.users')
