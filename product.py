# This file is part of the product_pack module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta


__all__ = ['PackagingType', 'ProductPack', 'ProductCode', 'Template']
__metaclass__ = PoolMeta


class PackagingType(ModelSQL, ModelView):
    'Packaging Type'
    __name__ = "product.packaging.type"
    name = fields.Char('Name', select=True, required=True, translate=True)
    type = fields.Selection([
            ('unit', 'Unit'),
            ('pack', 'Pack'),
            ('box', 'Box'),
            ('pallet', 'Pallet')
            ], 'Type', required=True)


class ProductPack(ModelSQL, ModelView):
    'Product Pack'
    __name__ = 'product.pack'
    product = fields.Many2One('product.template', 'Product',
        ondelete='CASCADE')
    sequence = fields.Integer('Sequence',
        help='Gives the sequence order when displaying a list of packaging.')
    codes = fields.One2Many('product.code', 'product_pack', 'Codes')
    qty = fields.Float('Quantity by Package',
        help='The total number of products you can put by box or pallet.')
    packaging_type = fields.Many2One('product.packaging.type',
        'Type of Packaging', required=True)
    packaging_type_weight = fields.Float('Empty Packaging Weight',
        help='The weight of the empty type of packaging.')
    packages_layer = fields.Integer('Packagings by layer',
        help='The number of packages by layer.')
    layers = fields.Integer('Number of Layers', required=True,
        help='The number of layers on a box or pallet.')
    weight = fields.Float('Total Packaging Weight',
        help='The weight of a full package, pallet or box.')
    height = fields.Float('Height', help='The height of the packaging.')
    width = fields.Float('Width', help='The width of the packaging.')
    length = fields.Float('Length', help='The length of the packaging.')
    note = fields.Text('Description')

    @classmethod
    def __setup__(cls):
        super(ProductPack, cls).__setup__()
        cls._order = [('product', 'ASC'), ('sequence', 'ASC')]

    @staticmethod
    def order_sequence(tables):
        table, _ = tables[None]
        return [table.sequence == None, table.sequence]

    @staticmethod
    def default_layers():
        return 3

    @staticmethod
    def default_sequence():
        return 1

    @staticmethod
    def default_packaging_type():
        pool = Pool()
        PackagingType = pool.get('product.packaging.type')
        packaging_types = PackagingType.search([], limit=1)
        return packaging_types[0].id if packaging_types else None

    def get_rec_name(self, name):
        return self.packaging_type.name


class ProductCode:
    __name__ = 'product.code'
    product_pack = fields.Many2One('product.pack', 'Packaging')

    @classmethod
    def __setup__(cls):
        super(ProductCode, cls).__setup__()
        if 'product_pack' not in cls.number.on_change:
            cls.number.on_change.add('product_pack')
            cls.number.on_change.add('_parent_product_pack.product')
        if not cls.product.states.get('invisible', False):
            cls.product.states['invisible'] = True

    @fields.depends('product_pack')
    def on_change_number(self):
        try:
            super(ProductCode, self).on_change_number()
        except AttributeError:
            pass

        self.product = self.product_pack and self.product_pack.product.id or None


class Template:
    __name__ = 'product.template'
    packagings = fields.One2Many('product.pack', 'product', 'Packagings')
