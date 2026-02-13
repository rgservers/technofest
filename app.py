import pymongo
import flask
import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from vector_organizer import find_relevant
import requests

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
col1 = mydb['testdb']
users_collection = mydb['users']

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    results = []
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            try:
                # Get similar item IDs
                similar_items = find_relevant(query)

                # Fetch full item details for the top similar items
                item_ids = list(similar_items.keys())[:10]  # Top 10
                if item_ids:
                    items = list(col1.find({"id": {"$in": item_ids}}))
                    # Sort by similarity score
                    items.sort(key=lambda x: similar_items.get(x['id'], 0), reverse=True)
                    results = items
            except Exception as e:
                print(f"Search error: {e}")
                # Fallback to sample data
                results = [
                    {"id": "sample1", "productDisplayName": "Sample Shirt", "masterCategory": "Apparel", "subCategory": "Topwear", "baseColour": "Blue", "season": "Summer", "gender": "Men"}
                ]
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
@login_required
def search_api():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    results = [
        {"productDisplayName": "Sample Shirt", "masterCategory": "Apparel", "subCategory": "Topwear", "baseColour": "Blue", "season": "Summer"}
    ]
    return find_relevant(query)
    
@app.route('/app', methods=['GET'])
def app_page():
    items = [{'image': 'http://assets.myntassets.com/v1/images/style/properties/9c1b19682ecf926c296f520d5d6e0972_images.jpg', 'descriptions': 'A product here'}]

    ip = request.remote_addr
    if ip == '127.0.0.1' or ip.startswith('192.168.') or ip.startswith('10.'):
        ip = '8.8.8.8'  # Use a public IP for testing local requests
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
        data = response.json()
        country = data.get('country')
        state = data.get('regionName')
    except:
        country = 'Unknown'
        state = 'Unknown'
    return render_template('app.html', items = items, country=country, state=state)

if __name__ == '__main__':
    app.run(debug=True)