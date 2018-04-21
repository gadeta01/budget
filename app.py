from flask import Flask, jsonify, render_template, redirect, url_for
from flask import request
from flask_wtf import Form
from wtforms import StringField,ValidationError, SelectField, TextAreaField, FloatField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired, Optional

app = Flask(__name__)
app.debug = True
app.secret_key="supersecretkey"

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

        return render_template('categories.html',spendingform=spendingform)

    return render_template('categories.html',spendingform=spendingform)

@app.route('/fillbudget')
def fillbudget():
    return render_template('fillbudget.html')

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
