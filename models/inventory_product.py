from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InventoryProduct(models.Model):
    _name = 'inventory.product'
    _description = 'Inventory Product'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Product Name', required=True)
    description = fields.Text(string='Description')
    quantity = fields.Integer(string='Quantity', default=0, tracking=1)
    location_id = fields.Many2one('location.inventory')
    price = fields.Float(string='Price', tracking=1)
    sale_price = fields.Float(string='Sale Price', help="Price at which the product is sold")
    total_value = fields.Float(string='Total Value', compute='_compute_total_value', store=True)
    vendor = fields.Many2one('res.partner', string='Vendor', tracking=1)
    category = fields.Many2one('category', string='Category')
    sku = fields.Char(string='SKU', required=True, help="Stock Keeping Unit - Unique Product Identifier")
    barcode = fields.Char(string='Barcode', tracking=1)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', help="Unit of measurement for the product")
    reorder_level = fields.Integer(string='Reorder Level', help="Minimum stock before reordering", tracking=1)
    active = fields.Boolean(string='Active', default=True)
    # stock_moves = fields.One2many('stock.move', 'product_id', string='Stock Moves')
    # field for reports current_date
    current_date = fields.Date(default=fields.Date.today)

    # check_reorder_level for quantity
    def check_reorder_level(self):
        for rec in self:
            if rec.quantity <= rec.reorder_level:
                message = f"Product '{rec.name}' is below reorder level!"
                self.env.user.notify_info(message)

    # compute_total_value
    @api.depends('quantity', 'price')
    def _compute_total_value(self):
        for rec in self:
            rec.total_value = rec.quantity * rec.price

    @api.constrains('quantity')
    def _check_quantity(self):
        for rec in self:
            if rec.quantity < 0:
                raise ValidationError("Quantity cannot be negative!")

    _sql_constraints = [
        ('unique_sku', 'unique(sku)', 'SKU must be unique!')
    ]







