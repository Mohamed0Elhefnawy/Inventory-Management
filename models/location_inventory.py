from odoo import models, fields, api

class InventoryLocation(models.Model):
    _name = 'location.inventory'
    _description = 'Location Inventory'
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char(string='Location Name', required=True)
    code = fields.Char(string='Location Code', required=True)
    parent_id = fields.Many2one('location.inventory', string='Parent Location', ondelete='cascade')
    child_ids = fields.One2many('location.inventory', 'parent_id', string='Sub Locations')
    type = fields.Selection([
        ('internal', 'Internal'),
        ('vendor', 'Vendor Location'),
        ('customer', 'Customer Location'),
        ('other', 'Other')
    ], string='Location Type', required=True, default='internal')
    active = fields.Boolean(string='Active', default=True)
    description = fields.Text(string='Description')
    complete_name = fields.Char(string='Complete Name', compute='_compute_complete_name', store=True)

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for record in self:
            if record.parent_id:
                record.complete_name = f"{record.parent_id.complete_name}/{record.name}"
            else:
                record.complete_name = record.name

    @api.model
    def name_get(self):
        result = []
        for record in self:
            names = []
            current = record
            while current:
                names.append(current.name)
                current = current.parent_id
            result.append((record.id, " / ".join(reversed(names))))
        return result
