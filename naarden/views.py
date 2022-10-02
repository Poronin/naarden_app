from crypt import methods
from flask import flash, redirect, render_template, request, session, url_for
from naarden.forms import RegistrationForm, LoginForm
from naarden.models import Users, Tables, Columns
from naarden import app
from naarden import db
from sqlalchemy import and_, or_, not_
from naarden import bcrypt
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    """ User login """
    if current_user.is_authenticated:
        return redirect(url_for('tables'))    
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.hash , form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('tables'))
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


@app.route("/tables", methods=['GET', 'POST'])
@login_required
def tables():
    q = request.args.get("q")
    if q:
        q = "%{}%".format(request.args.get("q")).upper()
        user_tables = Tables.query.filter(  Tables.user_id==current_user.id,
                                            and_(
                                                or_(
                                                    Tables.table_name.like(q),
                                                    Tables.description.like(q),
                                                    Tables.logical_entity.like(q),
                                                    Tables.category.like(q)
                                                )
                                            )
                                        )
    else:
        user_tables = Tables.query.filter(Tables.user_id==current_user.id)
    return render_template("tables.html", user_tables=user_tables)


@app.route("/columns")
@login_required
def columns():
    q = request.args.get("q")
    if q:
        q = "%{}%".format(request.args.get("q")).upper()
        user_columns = Columns.query.filter(  Columns.user_id==current_user.id,
                                                    and_(
                                                        or_(
                                                            Columns.column_name.like(q),
                                                            Columns.description.like(q),
                                                            Columns.logical_entity.like(q),
                                                            Columns.type.like(q),
                                                            Columns.length.like(q)
                                                        )
                                                    )
                                                )
    else:
        user_columns = Columns.query.filter_by(user_id=current_user.id)
    return render_template("columns.html", columns=user_columns)


@app.route("/tables/<string:table_columns>")
@login_required
def table_columns(table_columns):
    q = request.args.get("q")
    if q:
        q = "%{}%".format(request.args.get("q")).upper()
        user_table_columns = Columns.query.filter(  Columns.user_id==current_user.id,
                                                    Columns.table_name==table_columns,
                                                    and_(
                                                        or_(
                                                            Columns.column_name.like(q),
                                                            Columns.description.like(q),
                                                            Columns.logical_entity.like(q),
                                                            Columns.type.like(q),
                                                            Columns.length.like(q)
                                                        )
                                                    )
                                                )
    else:
        user_table_columns = Columns.query.filter_by(user_id=current_user.id, table_name=table_columns)
    return render_template("columns.html", columns=user_table_columns, table_name=table_columns)