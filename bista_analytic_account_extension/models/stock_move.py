# © 2015 ABF OSIELL <https://osiell.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class StockMove(models.Model):
    _inherit = "stock.move"

    project_tag = fields.Text(
        'Project Tags',
        related="purchase_line_id.project_tag"
    )
    project_tag_sale_ref = fields.Text(
        'Project Tags',
        related="picking_id.project_tag"
    )


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    project_tag = fields.Text(
        'Project Tags',
        related="move_id.project_tag"
    )
    project_tag_sale_ref = fields.Text(
        'Project Tags',
        related="move_id.project_tag_sale_ref"
    )
    picking_code = fields.Selection(
        related='move_id.picking_code',
        readonly=True
    )
