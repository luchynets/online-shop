from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
import pymysql
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		idd = str(request.form['submit_button'])
		return redirect(url_for('buy', id = idd))
	db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='shop', charset='utf8mb4')
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM products""")
	products = cursor.fetchall()
	db.close()
	return render_template('index.html', products=products)

@app.route('/buy/<id>', methods=['POST', 'GET'])
def buy(id = None):
	db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='shop', charset='utf8mb4')
	cursor = db.cursor()
	cursor.execute("""SELECT name, price FROM products WHERE id = %s""", (id))
	product = cursor.fetchall()
	db.close()
	promo = {'haudi ho': 10, 'lito2021': 50, '2021': 5, 'halavatop2021': 500}
	second = 1/50*int(product[0][1])
	pr = 0
	if request.method == 'POST':
		if request.form['sub'] == 'promo':
			get_promo = str(request.form['promo'])
			if get_promo in promo:
				pr += promo[get_promo]
	total = int(product[0][1]) + 1 + 1/50*int(product[0][1]) - pr
	return render_template('buy.html', product=product, second=second, total=total, promo=pr)

@app.route('/add', methods=['POST', 'GET'])
def add():
	if request.method == 'POST':
		if request.form['submit'] == 'Add':
			name = request.form['name']
			price = int(request.form['price'])
			description = request.form['description']
			db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='shop', charset='utf8mb4')
			cursor = db.cursor()
			cursor.execute("""INSERT INTO products (id, name, price, description) VALUES (0, %s, %s, %s)""", (name, int(price), description))
			db.commit()
			db.close()
	return render_template('add.html')

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)
