# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

class MembershipRequest(models.Model):
    _name = 'library.membership.request'
    _description = 'Library Membership Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    member_id = fields.Many2one(
        'res.partner', string='Member', required=True, tracking=True
    )
    registration_date = fields.Date(
        string='Registration Date',
        default=fields.Date.context_today,
        tracking=True
    )
    end_date = fields.Date(string='End Date', tracking=True)
    card_id = fields.Char(string='Card ID', readonly=True)
    payment_term_id = fields.Many2one(
        'account.payment.term', string='Payment Terms', tracking=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('active', 'Active'),
    ], string='Status', default='draft', tracking=True)
    invoice_id = fields.Many2one(
        'account.move', string='Invoice', readonly=True
    )
    line_ids = fields.One2many(
        'library.membership.line', 'membership_request_id',
        string='Membership Lines', copy=True
    )

    def action_confirm(self):
        """Confirm membership and generate invoice."""
        for rec in self:
            if rec.state != 'draft':
                continue
            # تحضير خطوط الفاتورة
            invoice_lines = []
            for line in rec.line_ids:
                invoice_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'quantity': 1,
                    'price_unit': line.amount,
                }))
            inv_vals = {
                'move_type': 'out_invoice',
                'partner_id': rec.member_id.id,
                'invoice_line_ids': invoice_lines,
                'invoice_date': rec.registration_date,
                'invoice_payment_term_id': rec.payment_term_id.id,
                #'membership_request_id':      rec.id,
                'is_membership_invoice':      True,
            }
            inv = self.env['account.move'].create(inv_vals)
            rec.invoice_id = inv.id
            rec.state = 'confirmed'

    def action_mark_paid(self):
        """Register payment, set state to paid, generate card ID and update partner."""
        for rec in self:
            if rec.state != 'confirmed' or not rec.invoice_id:
                continue
            # تأكد من ترحيل الفاتورة
            if rec.invoice_id.state != 'posted':
                rec.invoice_id.action_post()
            # تسجيل الدفعة
            rec.invoice_id.action_register_payment()
            # توليد رقم البطاقة من التسلسل
            seq = self.env['ir.sequence'].next_by_code(
                'library.membership.request.card'
            ) or '/'
            rec.card_id = seq
            rec.member_id.card_id = seq
            rec.state = 'paid'

    def action_activate(self):
        """Activate membership after payment."""
        for rec in self:
            if rec.state != 'paid':
                raise UserError('Only paid memberships can be activated.')
            rec.state = 'active'


class MembershipLine(models.Model):
    _name = 'library.membership.line'
    _description = 'Library Membership Line'

    membership_request_id = fields.Many2one(
        'library.membership.request', string='Membership Request',
        ondelete='cascade'
    )
    product_id = fields.Many2one(
        'product.product', string='Product', required=True
    )
    amount = fields.Float(string='Amount', required=True)

