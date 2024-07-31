from bracketer import app , db
from flask import render_template
from bracketer.models import users
@app.route('/')
@app.route('/home')

def homepage():
    if db.session.query(users).filter(users.ADMIN == True).count() == 0:
        print('hi')
        newadmin = users(USER = "admin" , PW = "4vacM7WYkUwUy39" , ADMIN = True)
        db.session.add(newadmin)
        db.session.commit()
    return render_template('home.html')