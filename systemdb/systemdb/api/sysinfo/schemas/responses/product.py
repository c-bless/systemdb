from ....ma import ma
from .....models.sysinfo import Product


class ProductSchema(ma.SQLAlchemyAutoSchema):
    """
    Installed Product

    """
    class Meta:
        model = Product
        include_fk = True