# © 2015 ABF OSIELL <https://osiell.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_tag = fields.Text(
        'Project Tags',
        related='analytic_account_id.project_tag'
    )
    count_move_lines = fields.Integer(
        'Move Lines',
        compute='_compute_move_lines'
    )

    @api.depends('picking_ids')
    def _compute_move_lines(self):
        for order in self:
            for picking in order.picking_ids:
                for move_lines in picking.move_line_ids:
                    order.count_move_lines = len(picking.move_line_ids)

    @api.multi
    def action_view_move_lines(self):
        move_lines = self.mapped('picking_ids').mapped('move_line_ids')
        action = self.env.ref('stock.stock_move_line_action').read()[0]
        domain = [('project_tag_sale_ref', '=', self.project_tag)]
        if len(move_lines) > 1:
            action['domain'] = [('id', 'in', move_lines.ids)]
        elif len(move_lines) == 1:
            action['views'] = \
            [(self.env.ref('stock.view_move_line_form').id, 'form')]
            action['res_id'] = move_lines.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.multi
    def _create_analytic_account(self, prefix=None):
        """
        Method override to added new fields values form sale \
        order to analytic account
        """
        for order in self:
            name = order.name
            if prefix:
                name = order.name + ": " + prefix
            if self.x_studio_field_J0IMG != 'Change Order' \
                and order.name and order.short_description:
                name = order.name + ": " + order.short_description or ''
            analytic_transaction_value = \
            self.analytic_account_id._fields['x_studio_field_pidtP'].selection
            analytic_dict = dict(analytic_transaction_value)
            partner_id = self.env['res.partner']\
            .search([('id', 'parent_of', self.partner_id.parent_id.id)],\
                     limit=1)
            analytic = self.env['account.analytic.account'].create({
                'name': name,
                'code': order.client_order_ref,
                'company_id': order.company_id.id,
                'partner_id': partner_id.id,
                'user_id': order.user_id.id,
                'sale_ref_id': order.id,
                'x_studio_field_pidtP': \
                analytic_dict.get(self.x_studio_field_J0IMG, False),
            })
            order.analytic_account_id = analytic


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _timesheet_create_task_prepare_values(self, project):
        """
        Prepare values to create project task
        """
        name = ''
        self.ensure_one()
        planned_hours = self._convert_qty_company_hours()
        sale_line_name_parts = self.name.split('\n')
        title = sale_line_name_parts[0] or self.product_id.name
        description = '<br/>'.join(sale_line_name_parts[1:])

        #added custom code to add sale order name while creating Project task
        if project.sale_line_id and \
            self.order_id.x_studio_field_J0IMG != 'Change Order' and \
            self.order_id.short_description:
            name = self.order_id.name + ": " + self.order_id.short_description
        else:
            name = title
        return {
            'name': name,
            'planned_hours': planned_hours,
            'partner_id': self.order_id.partner_id.id,
            'email_from': self.order_id.partner_id.email,
            'description': description,
            'project_id': project.id,
            'sale_line_id': self.id,
            'company_id': self.company_id.id,
            'user_id': False,  # force non assigned task, as created as sudo()
        }

    @api.multi
    def _timesheet_create_project(self):
        """ Generate project for the given so line, and link it.
            :param project: record of project.project \
             in which the task should be created
            :return task: record of the created task
        """
        self.ensure_one()
        name = ''
        account = self.order_id.analytic_account_id
        if not account:
            self.order_id._create_analytic_account \
             (prefix=self.product_id.default_code or None)
            account = self.order_id.analytic_account_id

        # create the project or duplicate one
        #added custom code to add sale order name while creating Project
        if self.order_id.client_order_ref and \
            self.order_id.x_studio_field_J0IMG != 'Change Order' and \
            self.order_id.short_description:
            name = self.order_id.client_order_ref
        else:
            name = self.order_id.client_order_ref
        if self.order_id.name and \
            self.order_id.x_studio_field_J0IMG != 'Change Order' and \
            self.order_id.short_description:
            name = \
             self.order_id.name + ": " + self.order_id.short_description or ''
        else:
            name = self.order_id.name
        values = {
            'name': name,
            'allow_timesheets': True,
            'analytic_account_id': account.id,
            'partner_id': self.order_id.partner_id.id,
            'sale_line_id': self.id,
            'sale_order_id': self.order_id.id,
            'active': True,
        }
        if self.product_id.project_template_id:
            values['name'] = "%s - %s" % (values['name'], \
                           self.product_id.project_template_id.name)
            project = self.product_id.project_template_id.copy(values)
            project.tasks.write({
                'sale_line_id': self.id,
                'partner_id': self.order_id.partner_id.id,
                'email_from': self.order_id.partner_id.email,
            })
            # duplicating a project doesn't set the SO on sub-tasks
            project.tasks.filtered \
                (lambda task: task.parent_id != False).write({
                'sale_line_id': self.id,
            })
        else:
            project = self.env['project.project'].create(values)
        # link project as generated by current so line
        self.write({'project_id': project.id})
        return project
