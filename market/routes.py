from market import app
from flask import render_template, flash, redirect, url_for
from market.models import Item, User
from market.forms import RegistrationForm, LoginForm
from market import db
from flask_login import login_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user_by_username = User.query.filter_by(username=form.username.data).first()
        existing_user_by_email = User.query.filter_by(email_address=form.email_address.data).first()

        if existing_user_by_username:
            flash('This username already taken. please choose a different username', category='danger')
        elif existing_user_by_email:
            flash('This email is already taken. please choose different email address', category='danger')
        else:
            user_to_create = User(username=form.username.data, email_address=form.email_address.data,
                                  password=form.password1.data)
            db.session.add(user_to_create)
            db.session.commit()
            login_user(user_to_create)
            return redirect(url_for('home_page'))
        return redirect(url_for('register_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error has been found: {err_msg}', category='danger')
    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template('login.html', form=form)



@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out", category="info")
    return redirect(url_for('home_page'))

@app.route('/item-info/<int:item_id>')
def item_info(item_id):
    item = Item.query.get(item_id)
    if item is None:
        flash('Item not found', category='danger')
        return redirect('market_page')
    
    return render_template('item_info.html', item=item)