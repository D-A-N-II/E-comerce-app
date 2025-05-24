from flask import Flask, render_template, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pesticides.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'your-secret-key-here'

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

# Define all products
products_data = [
    {
        'name': 'BugAway Pro Max',
        'description': 'Professional grade insecticide for complete crop protection with long-lasting effect',
        'price': '₹1,299.00',
        'category': 'Insecticide',
        'image_url': 'static/images/product (1).webp'
    },
    {
        'name': 'WeedClear Ultra',
        'description': 'Advanced herbicide formula for effective and quick weed control',
        'price': '₹899.00',
        'category': 'Herbicide',
        'image_url': 'static/images/product (2).webp'
    },
    {
        'name': 'FungusGuard Premium',
        'description': 'Superior fungicide protection for all types of plant diseases',
        'price': '₹1,499.00',
        'category': 'Fungicide',
        'image_url': 'static/images/product (3).webp'
    },
    {
        'name': 'CropShield Complete',
        'description': 'All-in-one pesticide solution for comprehensive crop protection',
        'price': '₹1,999.00',
        'category': 'Multi-purpose',
        'image_url': 'static/images/product (4).webp'
    },
    {
        'name': 'InsectKill Power',
        'description': 'Fast-acting insecticide for immediate pest control',
        'price': '₹799.00',
        'category': 'Insecticide',
        'image_url': 'static/images/product (5).webp'
    },
    {
        'name': 'WeedMaster Pro',
        'description': 'Professional strength herbicide for tough weeds',
        'price': '₹1,099.00',
        'category': 'Herbicide',
        'image_url': 'static/images/product (6).webp'
    },
    {
        'name': 'K Othorine Flow 25',
        'description': 'Powerful synthetic pyrethroid insecticide with broad spectrum control for various crops',
        'price': '₹675.00',
        'category': 'Herbicide',
        'image_url': 'static/images/product (8).webp'
    },
    {
        'name': 'Shri Shritaf (75 SP)',
        'description': 'Powerful multi-purpose pesticide for comprehensive pest control and plant protection',
        'price': '₹959.00',
        'category': 'Multi-purpose',
        'image_url': 'static/images/product (7).webp'
    }
]

with app.app_context():
    db.create_all()
    
    # Clear existing products and add all products again
    Product.query.delete()
    for product_data in products_data:
        product = Product(**product_data)
        db.session.add(product)
    db.session.commit()

@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = []
        session.modified = True

@app.route('/')
def home():
    if 'cart' not in session:
        session['cart'] = []
        session.modified = True
    return render_template('index.html')

@app.route('/api/products')
def get_products():
    try:
        category = request.args.get('category')
        if category and category != 'all':
            products = Product.query.filter_by(category=category).all()
        else:
            products = Product.query.all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'category': p.category,
            'image_url': p.image_url
        } for p in products])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cart', methods=['GET', 'POST'])
def cart():
    if 'cart' not in session:
        session['cart'] = []
        session.modified = True
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Invalid request data'}), 400
            
            product_id = data.get('product_id')
            action = data.get('action', 'add')
            
            if not product_id:
                return jsonify({'error': 'Product ID is required'}), 400
            
            # Convert product_id to integer for comparison
            product_id = int(product_id)
            
            if action == 'add':
                if product_id not in session['cart']:
                    # Verify product exists before adding to cart
                    product = Product.query.get(product_id)
                    if product:
                        session['cart'].append(product_id)
                        session.modified = True
                    else:
                        return jsonify({'error': 'Product not found'}), 404
            elif action == 'remove':
                if product_id in session['cart']:
                    session['cart'].remove(product_id)
                    session.modified = True
            
            return jsonify({'success': True, 'cart': session['cart']})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    try:
        cart_items = []
        for product_id in session['cart']:
            product = Product.query.get(product_id)
            if product:
                cart_items.append({
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image_url': product.image_url
                })
        return jsonify(cart_items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.after_request
def after_request(response):
    # Ensure the session is saved after each request
    session.modified = True
    return response

if __name__ == '__main__':
    app.run(debug=True) 