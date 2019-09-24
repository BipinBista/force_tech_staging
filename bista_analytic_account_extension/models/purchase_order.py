# © 2015 ABF OSIELL <https://osiell.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models, fields


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    project_tag = fields.Text(
        'Project Tags',
        related="account_analytic_id.project_tag"
    )
