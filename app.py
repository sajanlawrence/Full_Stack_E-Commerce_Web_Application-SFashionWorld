from myproject import app,db
from flask import render_template,redirect,url_for,flash,abort,request
from flask_login import login_required,login_user,logout_user
from myproject.models import User,Buy,Adding
from myproject.forms import LoginForm,RegistrationForm,Purchase,AddItem,RemoveItem
import stripe

public_key = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'

stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"
@app.route('/payment', methods=['POST'])
def payment():
    # CUSTOMER INFORMATION
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])
    # CHARGE/PAYMENT INFORMATION
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=1999,
        currency='usd',
        description='Donation'
    )

    return redirect(url_for('paymentsuccess'))

@app.route('/paymentsuccess')
def paymentsuccess():
    return render_template('paymentsuccess.html')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out! Continue shopping? Please login.')
    return redirect(url_for('home'))

@app.route('/formfill',methods=['GET','POST'])
@login_required
def formfill():
    form = Purchase(request.form)
    if form.validate():
        user = None
        user = User.query.filter_by(email=request.form['email']).first()
        if user == None:
            flash("Invalid Email")
            return redirect(url_for('formfill'))
        item_id = request.form['itemid']
        item =None
        item = Adding.query.filter_by(itemid=item_id).first()
        if item == None:
            flash("Invalid Item ID")
            return redirect(url_for("formfill"))
        user_email = request.form['email']
        user = User.query.filter_by(email=user_email).first()
        user_name = user.name
        user_ph = user.ph
        item_name = item.itemname
        item_price = item.price
        buying = Buy(itemid=item_id,itemname=item_name,price=item_price,name=user_name,email=user_email,ph=user_ph,size=request.form['size'],location=request.form['location'],city=request.form['city'],pin=request.form['pin'])
        db.session.add(buying)
        db.session.commit()
        flash("Purchase Successful")
        return render_template('details.html',buying=buying,public_key=public_key)
    return render_template('formfill.html',form=form)

@app.route('/adminhome')
@login_required
def adminhome():
    return render_template("adminhome.html")


@app.route('/view')
@login_required
def view():
    itemlist = Buy.query.all()
    return render_template('view.html',itemlist=itemlist)

@app.route('/viewitems')
@login_required
def viewitems():
    items = Adding.query.all()
    return render_template('viewitems.html',items=items)


@app.route('/removeitem',methods=['GET','POST'])
@login_required
def removeitem():
    form = RemoveItem(request.form)
    if form.validate():
        delete = Buy.query.filter_by(id=request.form['id']).first()
        db.session.delete(delete)
        db.session.commit()
        flash('Item Deleted!!!!!!')
        return redirect(url_for('removeitem'))
    return render_template('removeitem.html',form=form)

@app.route('/additem',methods=['GET','POST'])
@login_required
def additem():
    form = AddItem(request.form)
    if form.validate():
        item = Adding(itemid=request.form['itemid'],itemname=request.form['itemname'],price=request.form['price'])
        db.session.add(item)
        db.session.commit()
        flash('Item added!!!!!!')
        return redirect(url_for('additem'))
    return render_template('additem.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        user = None
        user = User.query.filter_by(email=request.form['email']).first()
        if user != None:
            if user.check_password(request.form['password']) and request.form['email'] == "admin@gmail.com":
                login_user(user)
                return redirect(url_for('adminhome'))

            if user.check_password(request.form['password']):
                login_user(user)
                flash("Login Successful!! Now you can start shopping. Have a nice day!")
                return redirect(url_for('home'))
        flash("Incorrect E-mail or Password")
    return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        hh = None
        hh = form.check_email(request.form['email'])
        if hh == "Your email has been registered already":
            flash("That email id is already taken....")
            return redirect(url_for('register'))
        user = User(name=request.form['name'],email=request.form['email'],ph=request.form['ph'],password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',form=form)
@app.route('/men')
def men():
    return render_template('men.html')
@app.route('/lady')
def lady():
    return render_template('lady.html')

if __name__ == '__main__':
    app.run(debug=True)
