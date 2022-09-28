from crypt import methods
from flask import flash, redirect, render_template, request, session, url_for
from naarden.forms import RegistrationForm, LoginForm
from naarden.models import Users
from naarden import app
from naarden import db
from naarden import bcrypt
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    """ User login """
    if current_user.is_authenticated:
        return redirect(url_for('index'))    
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.hash , form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('index')
        else:
            flash(f'Log-in unsuccessfully', 'danger') 
    return render_template("login.html", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """ User registration """

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = Users(username=form.username.data,
        email=form.email.data,
        hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.username.data}. You can now log in!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/tables")
@login_required
def tables():
    return render_template("tables.html")