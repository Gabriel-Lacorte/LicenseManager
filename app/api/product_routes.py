from app.models import Product, Key, db

from flask_login import login_required
from flask import jsonify, request, Blueprint


product_routes = Blueprint('product', __name__)


# GET /api/products -> List All Products.
@product_routes.route('', methods=['GET'])
@login_required
def get_products():
    all_products = Product.query.all()

    return jsonify([product.to_dict() for product in all_products]), 200


# POST /api/products -> Create a new product
@product_routes.route('', methods=['POST'])
@login_required
def create_product():
    try:
        data = request.get_json()
        name = data.get('name').strip()
        description = data.get('description').strip()
    except:
        return jsonify({'error': 'The input parameters were incorrect.'}), 400
    
    if not name or not description:
        return jsonify({'error': 'The input parameters were incorrect.'}), 400
    
    if len(description) > 500:
        return jsonify({'error': 'The description cannot be more than 500 characters.'}), 400
    
    if len(name) > 100:
        return jsonify({'error': 'The product name cannot be more than 100 characters.'}), 400
    
    product = Product(name=name.strip(), description=description.strip())
    db.session.add(product)
    db.session.commit()
    
    return jsonify(product.to_dict()), 201


# GET /api/products/<int:id> -> Get product by id.
@product_routes.route('/<int:id>/', methods=['GET'])
@login_required
def get_product_id(id):
    if len(str(id)) >= 19:
        return jsonify({'error': 'The product id cannot be more than 100.'}), 400

    product = Product.query.get(id)
    if product:
        return jsonify(product.to_dict_keys()), 200

    return jsonify({'error': 'Could not find the product.'}), 404
    

# DELETE /api/products/<int:id> -> Delete product by id
@product_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_product(id):
    if len(str(id)) >= 19:
        return jsonify({'error': 'The product id cannot be more than 100.'}), 400
    product = Product.query.get(id)
    product_keys = Key.query.filter_by(product_id=id).all()
    
    if product:
        db.session.delete(product)
        for key in product_keys:
            db.session.delete(key)
        db.session.commit()
        return jsonify({'message': 'Product deleted.'}), 200

    return jsonify({'error': 'Could not find the product.'}), 404