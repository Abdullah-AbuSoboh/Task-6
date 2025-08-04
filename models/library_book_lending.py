# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date

class BookLending(models.Model):
    _inherit = 'library.book.lending'

    card_id = fields.Char(
        string="Card ID",
        related='member_id.card_id',
        readonly=True,
        store=False,
    )

    @api.constrains('member_id')
    def _check_membership_active(self):
        today = date.today()
        for rec in self:
            membership = self.env['library.membership.request'].search([
                ('member_id', '=', rec.member_id.id),
                ('state', '=', 'active'),
                ('registration_date', '<=', today),
                ('end_date', '>=', today),
            ], limit=1, order='registration_date desc')
            if not membership:
                raise UserError(_(
                    "This partner has no active membership valid today.\n"
                    "You cannot borrow books without an active membership."
                ))

