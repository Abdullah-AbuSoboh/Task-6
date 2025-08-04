from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    is_membership_invoice = fields.Boolean(
        string="Membership Invoice", compute="_compute_is_membership_invoice", store=True,
        help="Set when at least one invoice line is for the library membership product"
    )

    @api.depends('invoice_line_ids.product_id')
    def _compute_is_membership_invoice(self):
        try:
            membership_product = self.env.ref('library_management.membership_product_id')
        except ValueError:
            membership_product = None
        for inv in self:
            inv.is_membership_invoice = bool(
                membership_product and
                any(line.product_id == membership_product for line in inv.invoice_line_ids)
            )

