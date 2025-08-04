from odoo import models, fields

class Author(models.Model):
    _name = 'library.author'
    _description = 'Author'

    name = fields.Char(string="Name", required=True)
    biography = fields.Text(string="Biography")

