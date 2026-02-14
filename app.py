import pymongo
import flask
import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from vector_organizer import find_relevant
import vector_organizer
import requests
import logging
import os

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = flask.Flask(__name__)
app.secret_key = 'proudsureshite'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    user = users_collection.find_one({"username": user_id})
    if user:
        return User(user_id)
    return None

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['VadaPavFashion']
col1 = mydb['fashion_items']
users_collection = mydb['users']

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    logger.info("Search page accessed")
    results = []
    if request.method == 'POST':
        logger.debug("Search POST request")
        query = request.form.get('query')
        logger.debug(f"Search query: {query}")
        if query:
            try:
                # Construct final query similar to searchapi
                ip = request.remote_addr
                logger.info(f"User IP for search: {ip}")
                if ip == '127.0.0.1' or ip.startswith('192.168.') or ip.startswith('10.'):
                    ip = '202.43.122.205'  # Use a public IP for testing local requests
                    logger.debug(f"Using public IP: {ip}")
                try:
                    logger.debug(f"Fetching geolocation for search")
                    response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
                    data = response.json()
                    country = data.get('country')
                    state = data.get('regionName')
                    logger.info(f"Search geolocation: Country={country}, State={state}")
                except Exception as e:
                    logger.error(f"Error in geolocation for search: {e}")
                    country = 'Unknown'
                    state = 'Unknown'
                finalquery = f"{query} from {country} {state}"
                logger.info(f"Final query constructed: {finalquery}")
                api_results = find_relevant(finalquery)
                logger.info(f"Search returned {len(api_results)} results")
                item_ids = [item[0] for item in api_results]
                if item_ids:
                    items = list(col1.find({"id": {"$in": item_ids}}))
                    logger.debug(f"Fetched {len(items)} items from DB")
                    id_to_item = {item['id']: {k: v for k, v in item.items() if k != '_id'} for item in items}
                    results = [id_to_item.get(id, {}) for id, sim in api_results]
                    logger.info(f"Final results: {len(results)} items")
                else:
                    results = []
            except Exception as e:
                logger.error(f"Search error: {e}")
                results = []
        else:
            logger.warning("No query provided")
    else:
        logger.debug("Search GET request")
    return render_template('search.html', results=results)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = users_collection.find_one({"username": username})
        if user and check_password_hash(user['password'], password):
            login_user(User(username))
            return redirect(url_for('search'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')


users_collection = mydb['users']

@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    logger.debug(f"Fetching product {product_id}")
    product = col1.find_one({"id": product_id})
    if product:
        # Remove the _id field
        product.pop('_id', None)
        logger.debug(f"Product {product_id} found")
        return jsonify(product)
    else:
        logger.warning(f"Product {product_id} not found")
        return jsonify({"error": "Product not found"}), 404

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('signup.html', error="Username and password required")

        if users_collection.find_one({"username": username}):
            return render_template('signup.html', error="User already exists")

        hashed_password = generate_password_hash(password)
        users_collection.insert_one({
            "username": username,
            "password": hashed_password
        })
        
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/safe_page')
@login_required
def safe_page():
    return f"Welcome to the safe page, {current_user.id}! You are authorized to view this content."


@app.route('/searchapi', methods=['GET'])
def search_api():
    logger.info("Search API accessed")
    query = request.args.get('query')
    gender = request.args.get('gender')
    masterCategory = request.args.get('masterCategory')
    subCategory = request.args.get('subCategory')
    articleType = request.args.get('articleType')
    baseColour = request.args.get('baseColour')
    season = request.args.get('season')
    year = request.args.get('year')
    usage = request.args.get('usage')
    logger.debug(f"Query parameters: query={query}, gender={gender}, masterCategory={masterCategory}, subCategory={subCategory}, articleType={articleType}, baseColour={baseColour}, season={season}, year={year}, usage={usage}")

    if not query:
        logger.warning("Query parameter missing")
        return jsonify({"error": "Query parameter is required"}), 400
    ip = request.remote_addr
    logger.info(f"User IP for search: {ip}")
    if ip == '127.0.0.1' or ip.startswith('192.168.') or ip.startswith('10.'):
        ip = '202.43.122.205'  # Use a public IP for testing local requests
        logger.debug(f"Using public IP: {ip}")
    try:
        logger.debug(f"Fetching geolocation for search")
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
        data = response.json()
        country = data.get('country')
        state = data.get('regionName')
        logger.info(f"Search geolocation: Country={country}, State={state}")
    except Exception as e:
        logger.error(f"Error in geolocation for search: {e}")
        country = 'Unknown'
        state = 'Unknown'
    finalquery = f"{query} from {country} {state}, for a {gender} in {masterCategory} - {subCategory}, article type: {articleType}, color: {baseColour}, season: {season}, year: {year}, usage: {usage}"
    logger.info(f"Final query constructed: {finalquery}")
    result = find_relevant(finalquery)
    logger.info(f"Search API returning {len(result)} results")
    return result
    
@app.route('/app', methods=['GET'])
def app_page():
    items = [{'image': 'http://assets.myntassets.com/v1/images/style/properties/9c1b19682ecf926c296f520d5d6e0972_images.jpg', 'descriptions': 'A product here'}]

    ip = request.remote_addr
    if ip == '127.0.0.1' or ip.startswith('192.168.') or ip.startswith('10.'):
        ip = '202.43.122.205' 
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
        data = response.json()
        country = data.get('country')
        state = data.get('regionName')
    except:
        country = 'Unknown'
        state = 'Unknown'
    return render_template('app.html', items=items, country=country, state=state)

if __name__ == '__main__':
    app.run(debug=True)