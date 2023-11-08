from .db import db
from .key import Key


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256), nullable=False)

    def to_dict(self):
        return {
            'productID': self.id,
            'name': self.name,
            'description': self.description,
        }
    
    def to_dict_keys(self):
        return {
            'productID': self.id,
            'name': self.name,
            'description': self.description,
            'keys': [key.to_dict() for key in Key.query.filter_by(product_id=self.id).all()]
        }
    
