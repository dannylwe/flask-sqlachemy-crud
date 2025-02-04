from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
# import database

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#databse
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db init
db = SQLAlchemy(app)
#init marshmallow
ma = Marshmallow(app)

#product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

#product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty') 

#Init schema
product_schema = ProductSchema() 
products_schema = ProductSchema(many=True) 


@app.route('/health', methods=['GET'])
def healthCheck():
    return jsonify({"mesaage": "server is running"})

@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

@app.route('/products', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

@app.route('/product/<int:num>', methods=['GET'])
def get_single_product(num):
    product = Product.query.get(num)
    if product is not None:
        return product_schema.jsonify(product)
    else:
        return jsonify({"Error": "product with that key can not be found"})

@app.route('/product/<int:num>', methods=['PATCH'])
def update_product(num):
    update_product = Product.query.get(num)
    print(update_product)

    if update_product is not None:
        description = request.json['description']
        price = request.json['price']
        qty = request.json['qty']

        # update product
        update_product.description = description
        update_product.price = price
        update_product.qty = qty

        db.session.commit()

        return product_schema.jsonify(update_product)
    else:
        return jsonify({"Error": "product with that key can not be found"})

@app.route('/product/<int:num>', methods=['DELETE'])
def delete_single_product(num):
    product = Product.query.get(num)
    if product is not None:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"deletion": "product has been deleted"})
    else:
        return jsonify({"Error": "product with that key can not be found"})