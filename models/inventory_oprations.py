from odoo import models, fields, api

class InventoryOperation(models.Model):
    _name = 'inventory.operation'
    _description = 'Inventory Operation'

    product_id = fields.Many2one('inventory.product', string='Product', required=True)
    operation_type = fields.Selection([
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
        ('internal', 'Internal Transfer')
    ], string='Operation Type', required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    date = fields.Datetime(string='Operation Date', default=fields.Datetime.now)
    current_location = fields.Many2one('location.inventory', related='product_id.location_id', readonly=0,
                                       string='Current Location')
    to_location_id = fields.Many2one('location.inventory', string='Update Location')

    responsible_user = fields.Many2one('res.users', string='Responsible User', default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancel')
    ], string='Status', default='draft')
    is_late = fields.Boolean()

    # for internal transfer
    # source_location_id = fields.Many2one('stock.location', string='Source Location', required=False)
    # destination_location_id = fields.Many2one('stock.location', string='Destination Location', required=False)

    # @api.model
    # def create(self, vals):
    #     product = self.env['inventory.product'].browse(vals['product_id'])
    #     if vals['operation_type'] == 'incoming':
    #         product.quantity += vals['quantity']
    #     elif vals['operation_type'] == 'outgoing':
    #         if product.quantity < vals['quantity']:
    #             raise ValueError("Not enough stock to complete the operation")
    #         product.quantity -= vals['quantity']
    #     return super().create(vals)

    # compute cost total value
    @api.depends('quantity', 'product_id', 'operation_type')
    def _compute_value(self):
        for record in self:
            if record.operation_type == 'incoming':
                record.value = record.quantity * record.product_id.price
            elif record.operation_type == 'outgoing':
                record.value = -(record.quantity * record.product_id.price)

    def check_end_date_for_operation(self):
        product_ids = self.search([])
        for rec in product_ids:
            if rec.state == 'in_progress' and rec.date and rec.date < fields.Date.today():
                rec.is_late = True
            else:
                rec.is_late = False

    def create_move_product_history(self, quantity, type_operation, status, vendor):
        for rec in self:
            rec.env['move.product.history'].create({
                'user_id': rec.env.uid,
                'product_id': rec.product_id.id,
                'quantity': quantity,
                'type_operation': type_operation,
                'status': status,
                'responsible_user': rec.responsible_user.id,
            })
    # def action_draft(self):
    #     for rec in self:
    #         rec.state = 'draft'
    #
    # def action_in_progress(self):
    #     for rec in self:
    #         rec.state = 'in_progress'
    #
    # def action_done(self):
    #     for rec in self:
    #         rec.state = 'done'
    #
    # def action_cancelled(self):
    #     for rec in self:
    #         rec.state = 'cancelled'

    @api.model
    def create(self, vals):
        vals['state'] = 'draft'
        return super().create(vals)

    def action_in_progress(self):
        for record in self:
            if record.state == 'draft':
                record.write({'state': 'in_progress'})

    def action_done(self):
        for record in self:
            if record.state == 'in_progress':
                product = record.product_id
                if record.operation_type == 'incoming':
                    record.create_move_product_history(record.quantity, record.operation_type,
                                                       'done', record.responsible_user)
                    product.quantity += record.quantity
                elif record.operation_type == 'outgoing':
                    record.create_move_product_history(record.quantity, record.operation_type,
                                                       'done', record.responsible_user)
                    if product.quantity < record.quantity:
                        raise ValueError("Not enough stock to complete the operation")
                    product.quantity -= record.quantity
                elif record.operation_type == 'internal':
                    product.location_id = record.to_location_id
                    record.create_move_product_history(record.quantity, record.operation_type,
                                                       'done', record.responsible_user)
                record.write({'state': 'done'})

    def action_cancel(self):
        for record in self:
            if record.state != 'done':
                if record.operation_type == 'incoming':
                    record.create_move_product_history(record.quantity, record.operation_type,
                                                       'cancel', record.responsible_user)

                elif record.operation_type == 'outgoing':
                    record.create_move_product_history(record.quantity, record.operation_type,
                                                       'cancel', record.responsible_user)

                elif record.operation_type == 'internal':

                    record.create_move_product_history(record.quantity, record.operation_type,
                                                       'cancel', record.responsible_user)
                record.write({'state': 'cancelled'})
