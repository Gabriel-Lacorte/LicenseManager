from .db import db

import secrets
from datetime import datetime


class Key(db.Model):
    __tablename__ = 'keys'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    period = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    usage_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    is_expired = db.Column(db.Boolean, default=False)


    def generate_key():
        while True:
            generated_key = '-'.join(secrets.token_hex(2).upper() for _ in range(4))
            if not Key.query.filter_by(key=generated_key).first():
                return generated_key.upper()


    def check_expired(self):
        now = datetime.utcnow()
        if now > self.expires_at:
            self.is_expired = True
            db.session.commit()


    def to_dict(self):
        self.check_expired()
        return {
            'keyID': self.id,
            'key': self.key,
            'period': self.period,
            'productID': self.product_id,
            'usageCount': self.usage_count,
            'createdAt': self.created_at,
            'expiresAt': self.expires_at,
            'isExpired': self.is_expired
        }
    