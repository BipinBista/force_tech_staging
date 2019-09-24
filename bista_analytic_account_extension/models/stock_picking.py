# © 2015 ABF OSIELL <https://osiell.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Picking(models.Model):
    _inherit = "stock.picking"

    project_tag = fields.Text(
        'Project Tags',
        related="sale_id.project_tag"
    )
