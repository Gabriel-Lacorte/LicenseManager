from .db import db

from datetime import datetime


class Key(db.Model):
    __tablename__ = 'keys'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    period = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    is_expired = db.Column(db.Boolean, default=False)


    def to_dict(self):
        return {
            'keyID': self.id,
            'key': self.key,
            'period': self.period,
            'productID': self.product_id,
            'createdAt': self.created_at,
            'expiresAt': self.expires_at,
            'isExpired': self.is_expired
        }
