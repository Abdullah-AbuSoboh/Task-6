from odoo import models, fields

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Title')
    author = fields.Char(string='Author')
    description = fields.Text(string='Description')
    published_date = fields.Date(string='Published Date')
    available = fields.Boolean(string='Available', default=True)

