# © 2015 ABF OSIELL <https://osiell.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': "Bista Account Analytic Extension",
    'version': "12.0.1.0.0",
    'author': "Bista Solutions",
    'license': "AGPL-3",
    'website': "http://www.bistasolutions.com",
    'category': "Tools",
    'depends': [
        'analytic', 'sale_management', 'sale_timesheet', 'purchase',
    ],
    'data': [
        'data/paperformats.xml',
        'views/account_analytic_view.xml',
        'views/purchase_order_view.xml',
        'views/sale_view.xml',
        'views/stock_move_view.xml',
        'views/stock_picking_view.xml',
        'views/lot_serial_label_report.xml',
    ],
    'application': True,
    'installable': True,
}
