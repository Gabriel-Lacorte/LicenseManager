from app.models import Key, Product, db

from secrets import token_hex
from flask_login import login_required
from datetime import datetime, timedelta
from flask import jsonify, request, Blueprint


key_routes = Blueprint('key', __name__)


# GET /api/keys/<key> -> Get key.
@key_routes.route('/<key>/', methods=['GET'])
def use_key(key):
    key = Key.query.filter_by(key=key).first()
    
    if key:
        now = datetime.utcnow()
        if now > key.expires_at:
            key.is_expired = True
            db.session.commit()

        return jsonify(key.to_dict()), 200
        
    return jsonify({'error': 'Could not find the key.'}), 404


# POST /api/keys -> Create a new key for a product.
@key_routes.route('', methods=['POST'])
@login_required
def create_keys():
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        period = int(data.get('period'))
    except:
        return jsonify({'error': 'The input parameters were incorrect.'}), 400
    
    if not product_id or not period:
        return jsonify({'error': 'The input parameters were incorrect.'}), 400

    if period > 999:
        return jsonify({'error': 'The limit in days is 999.'}), 400
    
    if not Product.query.get(product_id):
        return jsonify({'error': 'Could not find the product.'}), 400
    
    now = datetime.utcnow()
    expires_at = now + timedelta(minutes=period)

    generated_key = token_hex(32)
    while Key.query.filter_by(key=generated_key).first() is not None:
        generated_key = token_hex(32)

    key = Key(key=generated_key, period=period, product_id=product_id, created_at=now, expires_at=expires_at, is_expired=False)
    
    db.session.add(key)
    db.session.commit()
    
    return jsonify(key.to_dict()), 201


# DELETE /api/keys/<key> -> Delete key.
@key_routes.route('/<key>/', methods=['DELETE'])
@login_required
def delete_keys(key):    
    key = Key.query.filter_by(key=key).first()
    
    if key:
        db.session.delete(key)
        db.session.commit()
        return jsonify({'message': 'Key deleted successfully.'}), 200
        
    return jsonify({'error': 'Could not find the key.'}), 404
    

# PUT /api/keys/<key> -> Increases the key period
@key_routes.route('/<key>/', methods=['PUT'])
@login_required
def update_keys(key):
    try:
        data = request.get_json()
        period = data.get('period')
    except:
        return jsonify({'error': 'The input parameters were incorrect.'}), 400
    
    if not period:
        return jsonify({'error': 'The input parameters were incorrect.'}), 400
    
    if period > 999:
        return jsonify({'error': 'The limit in days is 999.'}), 400
    
    key = Key.query.filter_by(key=key).first()
    
    if key:
        now = datetime.utcnow()
        expires_at = now + timedelta(minutes=period)
        
        key.period = period
        key.expires_at = expires_at
        key.is_expired = False
        
        db.session.commit()
        return jsonify(key.to_dict()), 200
    else:
        return jsonify({'error': 'Could not find the key.'}), 404
