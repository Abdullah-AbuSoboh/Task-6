# models/product.py
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_membership = fields.Boolean(string='Membership Product', default=False)

