from flask import Flask, render_template
from flask_wtf import Form

app = Flask(__name__)   
app.debug = True
app.secret_key="supersecretkey"   

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




if __name__ == '__main__':
  app.run()  