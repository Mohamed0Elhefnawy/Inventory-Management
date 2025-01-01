from odoo import models, fields, api

class ProductCategory(models.Model):
    _name = 'category'
    _description = 'Product Category'
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char(string='Category Name', required=True)
    description = fields.Text(string='Description')
    parent_id = fields.Many2one('category', string='Parent Category', ondelete='cascade')
    child_ids = fields.One2many('category', 'parent_id', string='Subcategories')
    complete_name = fields.Char(string='Complete Name', compute='_compute_complete_name', store=True)
    active = fields.Boolean(default=True)

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for record in self:
            if record.parent_id:
                record.complete_name = f"{record.parent_id.complete_name}/{record.name}"
            else:
                record.complete_name = record.name

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.complete_name))
        return result

    # @api.model
    # def action_open_new_location(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Create New Location',
    #         'res_model': 'inventory.location',
    #         'view_mode': 'form',
    #         'target': 'new',
    #     }
    # < button
    # name = "action_open_new_location"
    # type = "object"
    # string = "Click to New Location"
    #
    # class ="btn-primary" / >



