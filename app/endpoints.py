from flask import Blueprint, request, jsonify
from app.models import db, Order, User, Product, Address, OrderProduct, UserRoles
from flask_security import roles_required, login_required


api_bp = Blueprint('api', __name__)


@api_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and user.verify_password(data['password']):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Unauthorized access'}), 401


@api_bp.route('/order/<int:order_id>', methods=['POST'])
@login_required
def get_order(order_id):
    order = Order.query.get(order_id)
    if order:
        return jsonify(order_id=order.id, status=order.status)
    return jsonify(error="Order not found"), 404


@api_bp.route('/products/<int:product_id>', methods=['GET'])
@login_required
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({'id': product.id, 'color': product.color, 'weight': product.weight, 'price': product.price}), 200


@api_bp.route('/products/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json
    product.color = data.get('color', product.color)
    product.weight = data.get('weight', product.weight)
    product.price = data.get('price', product.price)
    db.session.commit()
    return jsonify({'message': 'Product updated', 'product_id': product.id}), 200


@api_bp.route('/products/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200


@api_bp.route('/addresses', methods=['POST'])
@login_required
def create_address():
    data = request.json
    address = Address(country=data['country'], city=data['city'], street=data['street'])
    db.session.add(address)
    db.session.commit()
    return jsonify({'message': 'Address created', 'address_id': address.id}), 201


@api_bp.route('/addresses/<int:address_id>', methods=['GET'])
@login_required
def get_address(address_id):
    address = Address.query.get_or_404(address_id)
    return jsonify({'id': address.id, 'country': address.country, 'city': address.city, 'street': address.street}), 200


@api_bp.route('/addresses/<int:address_id>', methods=['PUT'])
@login_required
def update_address(address_id):
    address = Address.query.get_or_404(address_id)
    data = request.json
    address.country = data.get('country', address.country)
    address.city = data.get('city', address.city)
    address.street = data.get('street', address.street)
    db.session.commit()
    return jsonify({'message': 'Address updated', 'address_id': address.id}), 200


@api_bp.route('/addresses/<int:address_id>', methods=['DELETE'])
@login_required
def delete_address(address_id):
    address = Address.query.get_or_404(address_id)
    db.session.delete(address)
    db.session.commit()
    return jsonify({'message': 'Address deleted'}), 200


@api_bp.route('/orders', methods=['POST'])
@login_required
def create_order():
    data = request.json
    order = Order(status=data['status'], address_id=data['address_id'])
    db.session.add(order)

    for item in data['products']:
        order_product = OrderProduct(order_id=order.id, product_id=item['product_id'], quantity=item['quantity'])
        db.session.add(order_product)

    db.session.commit()
    return jsonify({'message': 'Order created', 'order_id': order.id}), 201


@api_bp.route('/orders/<int:order_id>', methods=['GET'])
@login_required
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    order_products = [{'product_id': op.product_id, 'quantity': op.quantity} for op in order.products]
    return jsonify(
        {'id': order.id, 'status': order.status, 'address_id': order.address_id, 'products': order_products}), 200


@api_bp.route('/orders/<int:order_id>', methods=['PUT'])
@login_required
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.json
    order.status = data.get('status', order.status)
    db.session.commit()
    return jsonify({'message': 'Order updated', 'order_id': order.id}), 200


@api_bp.route('/orders/<int:order_id>', methods=['DELETE'])
@login_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted'}), 200


@api_bp.route('/users', methods=['POST'])
@login_required
def create_user():
    data = request.json
    user = User(email=data['email'], password=data['password'])
    roles = UserRoles.query.filter(UserRoles.name.in_(data['roles'])).all()
    user.roles.extend(roles)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created', 'user_id': user.id}), 201


@api_bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    user_roles = [role.name for role in user.roles]
    return jsonify({'id': user.id, 'email': user.email, 'roles': user_roles}), 200


@api_bp.route('/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)
    roles = UserRoles.query.filter(UserRoles.name.in_(data['roles'])).all()
    user.roles = roles
    db.session.commit()
    return jsonify({'message': 'User updated', 'user_id': user.id}), 200


@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
@roles_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200


@api_bp.route('/roles', methods=['POST'])
@login_required
@roles_required('admin')
def create_role():
    data = request.json
    role = UserRoles(name=data['name'])
    db.session.add(role)
    db.session.commit()
    return jsonify({'message': 'Role created', 'role_id': role.id}), 201


@api_bp.route('/roles/<int:role_id>', methods=['GET'])
@login_required
def get_role(role_id):
    role = UserRoles.query.get_or_404(role_id)
    return jsonify({'id': role.id, 'name': role.name}), 200


@api_bp.route('/roles/<int:role_id>', methods=['PUT'])
@login_required
@roles_required('admin')
def update_role(role_id):
    role = UserRoles.query.get_or_404(role_id)
    data = request.json
    role.name = data.get('name', role.name)
    db.session.commit()
    return jsonify({'message': 'Role updated', 'role_id': role.id}), 200


@api_bp.route('/roles/<int:role_id>', methods=['DELETE'])
@login_required
@roles_required('admin')
def delete_role(role_id):
    role = UserRoles.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
    return jsonify({'message': 'Role deleted'}), 200


@api_bp.route('/json-rpc', methods=['POST'])
@login_required
def json_rpc():
    data = request.json
    if 'method' in data:
        method = data['method']
        if method == 'get_order_info':
            if 'params' in data and 'order_id' in data['params']:
                order_id = data['params']['order_id']
                order = Order.query.get(order_id)
                if order:
                    return jsonify({'result': {'order_id': order.id, 'status': order.status, 'products': [{'product_id': op.product_id, 'quantity': op.quantity} for op in order.products]}}), 200
                else:
                    return jsonify({'error': {'code': 404, 'message': 'Order not found'}}), 404
        else:
            return jsonify({'error': {'code': 400, 'message': 'Invalid method'}}), 400
    else:
        return jsonify({'error': {'code': 400, 'message': 'Method not specified'}}), 400
