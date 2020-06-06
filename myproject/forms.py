from wtforms import Form,StringField,PasswordField,SubmitField,SelectMultipleField,IntegerField,TextAreaField,RadioField
from wtforms.validators import DataRequired,Email,EqualTo
from myproject.models import User
from wtforms import ValidationError

class LoginForm(Form):
    email = StringField('Email:',validators=[DataRequired(),Email()])
    password = PasswordField('Password:',validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(Form):
    name = StringField('Name:',validators=[DataRequired()])
    email = StringField('Email:',validators=[DataRequired(),Email()])
    ph = StringField('Phone Number:',validators=[DataRequired()])
    password = PasswordField('Password:',validators=[DataRequired(),EqualTo('pass_confirm')])
    pass_confirm = PasswordField('Confirm Password:',validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self,field):
        if User.query.filter_by(email=field).first():
            return("Your email has been registered already")

class Purchase(Form):
    itemid = StringField('itemcode ',validators=[DataRequired()])
    email = StringField('Email:',validators=[DataRequired(),Email()])
    size = StringField('Enter Your Size: ',validators=[DataRequired()])
    location = StringField('Delivery Location: ',validators=[DataRequired()])
    city = StringField('city:',validators=[DataRequired()])
    pin = StringField('Pin-code: ',validators=[DataRequired()])

class RemoveItem(Form):
    id = StringField('id ',validators=[DataRequired()])

class AddItem(Form):
    itemid = StringField("itemid",validators=[DataRequired()])
    itemname = StringField('name',validators=[DataRequired()])
    price = StringField('price',validators=[DataRequired()])
