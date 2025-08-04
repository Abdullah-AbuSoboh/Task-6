from odoo import models, fields

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Book'

    name = fields.Char(string="Title", required=True)
    author = fields.Char(string="Author")
    published_date = fields.Date(string="Published Date")

from odoo import models, fields

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Author'

    name = fields.Char(string="Author Name", required=True)
    biography = fields.Text(string="Biography")

