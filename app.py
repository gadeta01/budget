
import os
import urllib.parse
import psycopg2
import bcrypt
from flask import Flask, jsonify, render_template, redirect, url_for,g, jsonify
from flask import request
from flask_wtf import Form
from wtforms import StringField,ValidationError, SelectField, TextAreaField, FloatField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired, Optional

app = Flask(__name__)
app.debug = True
app.secret_key="supersecretkey"

def connect_db():
	print("In connect_db")
	if not 'DATABASE_URL' in os.environ:
		print("You must have DATABASE_URL in your environment variable. See documentation.")
		print("Execute 'source .env' to set up this environment variable if running locally.")
		return

	try:
		urllib.parse.uses_netloc.append("postgres")
		url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

		db = psycopg2.connect(
		    database=url.path[1:],
		    user=url.username,
		    password=url.password,
		    host=url.hostname,
		    port=url.port
		)

		return db

	except Exception as ex:
		print(ex)
		print("Unable to connect to database on system.")
		return

def get_db():
	print("In get_db")
	"""Opens a new database connection if there is none yet for the
	current application context.
	"""
	if not hasattr(g, 'envelope'):
		g.envelope = connect_db()
	return g.envelope

def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    # Check hashed password. Useing bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)


@app.route('/')
def home():
    #depending on session could return something different

    return render_template('login.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        token = dblogin(email, password)
        if token != ('Error: Invalid Userid or Password', 400):
            return redirect(url_for('dashboard'))
        else:
            error = 'Incorrect password'
        return render_template('login.html', error=error)

    return redirect(url_for('dashboard'))

@app.route('/dashboard')  
def dashboard():        
    #TODO get categories from database      
    categories = []
    rent = {"name": "Rent", "balance": 700, "per_month":700}
    categories.append(rent)
    groceries = {"name": "Groceries", "balance": 40, "per_month":120}
    categories.append(groceries)
    return render_template('dashboard.html', categories=categories)

@app.route('/transactions')
def transactions():
    return render_template('transactions.html')

@app.route('/categories', methods=['GET','POST'])
def categories():

    spendingform = SpendingForm() #spendingform at bottom of index page
    if spendingform.validate_on_submit():

        #store results in database
        income = spendingform.income.data
        entertainment = spendingform.entertainment.data
        education = spendingform.education.data
        shopping = spendingform.shopping.data
        personal_care = spendingform.personal_care.data
        health_fitness = spendingform.health_fitness.data
        kids = spendingform.kids.data
        food = spendingform.food.data
        gifts = spendingform.gifts.data
        investment = spendingform.investment.data
        utilities = spendingform.utilities.data
        transport = spendingform.transport.data
        travel = spendingform.travel.data
        fees_charges = spendingform.fees_charges.data
        business_services = spendingform.business_services.data
        taxes = spendingform.taxes.data

        print("income: ", income)

        return redirect(url_for('dashboard'))

    return render_template('categories.html',spendingform=spendingform)

@app.route('/fillbudget')
def fillbudget():
    return render_template('fillbudget.html')

@app.route('/create/user/<email>')
def createUser(email):
	db = get_db()
	cur = db.cursor()
	print(type(email))
	# something = """INSERT INTO "User" (email) VALUES (%s)""", (email)
	# something = """INSERT INTO "User" (email) VALUES (""" + email + ")"
	# print(something)
	# cur.execute(something)
	# db.commit()

	cur.execute("""INSERT INTO "User" (email, password) VALUES (%s,%s)""", (email,"something",))
	db.commit()

	return 'done'


@app.route('/create/category/<title>/<permonth>/<accumulated>/<userid>')
def createCategory(title, permonth, accumulated, userid):
	db = get_db()
	cur = db.cursor()

	# title varchar(50),
	# permonth integer NOT NULL,
	# accumulated integer NOT NULL,
	# userid integer NOT NULL,

	cur.execute("""INSERT INTO "Category" (title, permonth, accumulated, userid) VALUES (%s,%s,%s,%s)""", (title, str(permonth), str(accumulated), str(userid)))
	db.commit()


	print(title)
	return title
	
@app.route('/view/category/')
def viewCategory():
	db = get_db()
	cur = db.cursor()


	cur.execute("""Select * from "Category" """)
	lst = cur.fetchall()
	


	print(lst)
	return str(lst)


class SpendingForm(Form):
    income = FloatField('', validators=[Optional()])
    entertainment = FloatField('', validators=[Optional()])
    education = FloatField('', validators=[Optional()])
    shopping = FloatField('', validators=[Optional()])
    personal_care = FloatField('', validators=[Optional()])
    health_fitness = FloatField('', validators=[Optional()])
    kids = FloatField('', validators=[Optional()])
    food = FloatField('', validators=[Optional()])
    gifts = FloatField('', validators=[Optional()])
    investment = FloatField('', validators=[Optional()])
    utilities = FloatField('', validators=[Optional()])
    transport = FloatField('', validators=[Optional()])
    travel = FloatField('', validators=[Optional()])
    fees_charges = FloatField('', validators=[Optional()])
    business_services = FloatField('', validators=[Optional()])
    taxes = FloatField('', validators=[Optional()])

def dblogin(email, password):
    #TODO implement login
    return ("success")


if __name__ == '__main__':
  app.run()
