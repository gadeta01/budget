from flask import Flask, render_template, g, jsonify
from flask_wtf import Form
import os
import urllib.parse
import psycopg2
import bcrypt

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

@app.route('/dashboard')  
def dashboard():              
    return render_template('dashboard.html')

@app.route('/transactions')  
def transactions():             
    return render_template('transactions.html')

@app.route('/categories')
def categories():
    return render_template('categories.html')

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


if __name__ == '__main__':
  app.run()  