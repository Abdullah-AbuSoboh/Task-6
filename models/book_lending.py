from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class BookLending(models.Model):
    _name = 'library.book.lending'
    _description = 'Book Lending'

    book_id = fields.Many2one('library.book', string='Book', required=True)
    borrower_id = fields.Many2one(
        'res.partner', string='Member', required=True,
        help="Select the member who borrows the book.")
    card_id = fields.Char(
        related='borrower_id.card_id', string='Card ID', readonly=True)
    lend_date = fields.Date(string='Lend Date', required=True)
    return_date = fields.Date(string='Return Date')
    state = fields.Selection([
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('late', 'Late'),
    ], string='Status', default='borrowed')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        return res

    def mark_as_returned(self):
        for rec in self:
            if rec.state == 'returned':
                raise ValidationError("This book is already returned.")
            rec.state = 'returned'

    @api.onchange('lend_date')
    def _onchange_lend_date(self):
        if self.lend_date:
            self.return_date = self.lend_date + timedelta(days=7)
        if self.lend_date and self.return_date and self.lend_date > self.return_date:
            raise ValidationError("Lend date cannot be after return date.")

    @api.constrains('borrower_id', 'lend_date')
    def _check_membership_active(self):
        for rec in self:
            active = self.env['library.membership.request'].search([
                ('member_id', '=', rec.borrower_id.id),
                ('state', '=', 'active'),
                ('registration_date', '<=', rec.lend_date),
                ('end_date', '>=', rec.lend_date),
            ], limit=1)
            if not active:
                raise ValidationError(
                    "You cannot borrow this book because your membership is invalid or expired.")

