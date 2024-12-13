from flask import Flask, render_template , request , session
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt 
from random import randint, choice
from string import ascii_letters
from numpy import concatenate
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bracketer.db"
app.config['SECRET_KEY'] = 'roxyiscute' 
db = SQLAlchemy(app)
app.static_folder = 'static'
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
bcrypt = Bcrypt(app)
from bracketer import admindelete, profile, admininsert , charts, loginregister , apply , home , adminupdate
from bracketer.models import users


