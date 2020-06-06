from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),index=True)
    email = db.Column(db.String(64),unique=True,index=True)
    ph = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))


    def __init__(self,name,email,ph,password):
        self.name = name
        self.email = email
        self.ph = ph
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class Buy(db.Model,UserMixin):
    __tablename__ = "buy"
    id = db.Column(db.Integer,primary_key=True)
    itemid = db.Column(db.String(64))
    itemname = db.Column(db.String(64))
    price = db.Column(db.String(64))
    name = db.Column(db.String(64),index=True)
    email = db.Column(db.String(64),unique=False,index=True)
    ph = db.Column(db.String(64))
    size = db.Column(db.String(64))
    location = db.Column(db.String(256),unique=False,index=True)
    city = db.Column(db.String(64))
    pin = db.Column(db.String(64))

    def __init__(self,itemid,itemname,price,name,email,ph,size,location,city,pin):
        self.itemid = itemid
        self.itemname = itemname
        self.price = price
        self.name = name
        self.email = email
        self.ph = ph
        self.size = size
        self.location = location
        self.city = city
        self.pin = pin

class Adding(db.Model,UserMixin):
    __tablename__ = "items"
    itemid = db.Column(db.String(64),primary_key=True)
    itemname = db.Column(db.String(64),index=True)
    price = db.Column(db.String(64))

    def __init__(self,itemid,itemname,price):
        self.itemid = itemid
        self.itemname = itemname
        self.price = price
