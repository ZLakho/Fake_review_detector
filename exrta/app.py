
import json
import atexit
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Dummy data for products
products = {
    '1': {'name': 'Product A', 'image': 'images/shoes.jpeg'},
    '2': {'name': 'Product B', 'image': 'https://example.com/product_b_image.jpg'},
    '3': {'name': 'Product C', 'image': 'https://example.com/product_c_image.jpg'},
    '4': {'name': 'Product D', 'image': 'https://example.com/product_d_image.jpg'},
    '5': {'name': 'Product E', 'image': 'https://example.com/product_e_image.jpg'},
    '6': {'name': 'Product F', 'image': 'https://example.com/product_f_image.jpg'},
    '7': {'name': 'Product G', 'image': 'https://example.com/product_g_image.jpg'},
    '8': {'name': 'Product H', 'image': 'https://example.com/product_h_image.jpg'},
    '9': {'name': 'Product I', 'image': 'https://example.com/product_i_image.jpg'},
    '10': {'name': 'Product J', 'image': 'https://example.com/product_j_image.jpg'},
    '11': {'name': 'Product K', 'image': 'https://example.com/product_k_image.jpg'},
    '12': {'name': 'Product L', 'image': 'https://example.com/product_l_image.jpg'},
    '13': {'name': 'Product M', 'image': 'https://example.com/product_m_image.jpg'},
    '14': {'name': 'Product N', 'image': 'https://example.com/product_n_image.jpg'},
    '15': {'name': 'Product O', 'image': 'https://example.com/product_o_image.jpg'},
    '16': {'name': 'Product P', 'image': 'https://example.com/product_p_image.jpg'},
    '17': {'name': 'Product Q', 'image': 'https://example.com/product_q_image.jpg'},
    '18': {'name': 'Product R', 'image': 'https://example.com/product_r_image.jpg'},
    '19': {'name': 'Product S', 'image': 'https://example.com/product_s_image.jpg'},
    '20': {'name': 'Product T', 'image': 'https://example.com/product_t_image.jpg'},
}

# Load reviews from file
try:
    with open('reviews.json', 'r') as f:
        reviews = json.load(f)
except FileNotFoundError:
    # If the file doesn't exist, initialize an empty reviews dictionary
    reviews = {str(i): [] for i in range(1, 21)}

# Admin credentials
admin_username = "admin"
admin_password = "admin"

# Function to check if a review is fake
def is_fake_review(ip_address):
    fake_threshold = 3  # Adjust this threshold based on your needs
    count = sum(1 for review_list in reviews.values() for review in review_list if review['ip_address'] == ip_address)
    return count > fake_threshold

# Save reviews before each request
@app.before_request
def save_reviews():
    with open('reviews.json', 'w') as f:
        json.dump(reviews, f)


# Routes

@app.route('/')
def home():
    return render_template('home.html', products=products, reviews=reviews)

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('home'))


@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' in session:
        return render_template('admin_dashboard.html', products=products, reviews=reviews)
    else:
        return redirect(url_for('home'))

@app.route('/delete_review/<product_id>', methods=['POST'])
def delete_review(product_id):
    if 'admin' in session:
        # Delete reviews for the specified product_id
        reviews[product_id] = []
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('home'))
  
@app.route('/product/<product_id>', methods=['GET', 'POST'])
def product(product_id):
    if request.method == 'POST':
        user_review = request.form['review']
        user_ip = request.remote_addr  # Get user's IP address

        if not is_fake_review(user_ip):
            reviews[product_id].append({'review': user_review, 'ip_address': user_ip})

    return render_template('product.html', product=products[product_id], reviews=reviews[product_id])

# Save reviews to file before exiting
@app.before_request
def save_reviews():
    with open('reviews.json', 'w') as f:
        json.dump(reviews, f)

# Save reviews to file before exiting
atexit.register(save_reviews)


if __name__ == '__main__':
    app.run(debug=True)
