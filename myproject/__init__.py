import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
#creating a LoginManager object
login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkey"
#below is used for running in our computer
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sajan@localhost/sfw'
#this is for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://djpbepnjsjkbdc:88db57f16dbb9bfd085ff0dc63c6e8c1f74543692946bc08f5046be0e4193656@ec2-52-71-55-81.compute-1.amazonaws.com:5432/devc94v4hfc7ai'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)
# We can now pass in our app to the login manager
login_manager.init_app(app)
# Tell users what view to go to when they need to login.
login_manager.login_view ="login"
