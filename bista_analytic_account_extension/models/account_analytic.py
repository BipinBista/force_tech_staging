# © 2015 ABF OSIELL <https://osiell.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    project_tag = fields.Text(
        'Project Tag',
         compute="compute_analytic_name",
         store=True
    )
    sale_ref_id = fields.Many2one(
        'sale.order', 'Sale Ref'
    )
    user_id = fields.Many2one(
        'res.users',
        'Sales Person'
    )

    @api.depends('name')
    def compute_analytic_name(self):
        """"
        Method to compute analytic name in project tag field.
        """
        for analytic in self:
            if analytic.name:
                anaytic_name = analytic.name.split(':')[0]
                analytic.project_tag = anaytic_name
