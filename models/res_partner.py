from odoo import api, models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    card_id = fields.Char(string='Card ID', readonly=True)
    membership_ids = fields.One2many(
        'library.membership.request', 'member_id', string='Memberships'
    )

    def action_view_memberships(self):
        self.ensure_one()
        return {
            'name': 'Memberships',
            'type': 'ir.actions.act_window',
            'res_model': 'library.membership.request',
            'view_mode': 'tree,form',
            'domain': [('member_id', '=', self.id)],
        }

