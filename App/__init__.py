from flask import Flask
from flask_bcrypt import Bcrypt
import os
# SQLAlchemy (source code) is a well-regarded database toolkit and object-relational mapper (ORM) implementation written in Python.
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail




app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mohamedbouhdida100*@localhost/todoapp'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '83cc3912609c6e'
app.config['MAIL_PASSWORD'] = '565d82f9237059'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
  # database name
mail = Mail(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_direc"
login_manager.login_message_category = "info"

from App import routes
from App.models import admin
import App.api


 
