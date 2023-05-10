from flask import render_template, flash, redirect, url_for, request
from app.config import app, db, login

from flask_login import current_user, login_user, logout_user, login_required
from app.forms import RegestrationForm, LoginForm, AddGoodForm
from app.models import User, Treat
from werkzeug.utils import secure_filename

from json import loads, dumps

import os.path as path
from os import getcwd

@app.before_request
def create_tables():
    db.create_all()
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@app.route('/index/')
def index():
    best_treats = [Treat.query.filter_by(name='Natūralūs skanėstai vištos kojos šunims').first(), Treat.query.filter_by(name='Skanėstai Šunims sveikam metabolizmui').first(), Treat.query.filter_by(name="Džiovinta jaučio ausis").first()]


    return render_template('index.html', title='Home', best_treats=best_treats)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
       return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Incorrect login data: check password or username")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    
    return render_template("login.html", title="Sign in", form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegestrationForm()
    if form.validate_on_submit():
        flash("Congrats!")
        user = User(username=form.username.data, email=form.email.data, password_hash=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/cart/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    cart = loads(user.cart)
    normal_cart = []

    for treat in cart:
        normal_cart.append(Treat.query.filter_by(name=treat).first())


    return render_template('cart.html', title='Cart', cart=normal_cart)

@app.route('/treat/<name>', methods=['GET', 'POST'])
def treat(name):
    treat = Treat.query.filter_by(name=name).first()

    if request.method == 'POST':
        cart = loads(current_user.cart)
        cart.append(treat.name)
        current_user.cart = dumps(cart)
        db.session.commit()

        # return redirect(url_for('cart', username=current_user.username))
    
    return render_template('treat.html', title=treat.name, treat=treat)

@app.route('/catalog')
def food():
    treats = Treat.query.all()
    return render_template('treats.html', title='Treats', treats=treats)

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

@app.route('/add_treat', methods=["GET", "POST"])
def add_good():
    form = AddGoodForm()
    if form.validate_on_submit():
        flash('Good succefully added to DataBase')
        image = form.image.data
        print(image)
        treat = Treat(name=form.name.data, descreption=form.descreption.data, price=form.price.data, count=form.count.data, image=image.filename)
        filename = secure_filename(image.filename)
        image.save(path.join(
            path.abspath(path.dirname(__file__)), getcwd() + '\\app\\static\\images\\', filename
        ))
        db.session.add(treat)
        db.session.commit()
    return render_template('add_treat.html', title='Add treat', form=form)