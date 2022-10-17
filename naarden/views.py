from crypt import methods
from flask import flash, redirect, render_template, request, session, url_for
from naarden.forms import RegistrationForm, LoginForm, UploadTablesFile, UploadColumnsFile, UploadRelationshipsFile
from naarden.models import Users, Tables, Columns
from naarden import app
from naarden import db
from sqlalchemy import and_, or_
from naarden import bcrypt
from flask_login import login_user, logout_user, current_user, login_required
import json


added_tables = None
tables_to_query = []

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
    # get requests
    q = request.args.get("q")
    add = request.args.get("add")
    remove = request.args.get("remove")

    # process requests
    if q:
        q = "%{}%".format(request.args.get("q")).upper()
        q = q.replace(' ','%')
        print(q)
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
    elif add:
        if not add in tables_to_query:
            tables_to_query.append(add)
            added_tables = Tables.query.filter(Tables.user_id==current_user.id, and_(Tables.table_name == add)).first()
            print(f'Added table: {added_tables.table_name}')
            print(f'List of tables to query after adding: {tables_to_query}')
            return [{"table_name":added_tables.table_name, "logical_entity":added_tables.logical_entity, "description":added_tables.description}]     
        else:
            return {}
    elif remove:
        if remove in tables_to_query:
            tables_to_query.remove(remove)
            added_tables = Tables.query.filter(Tables.user_id==current_user.id, and_(Tables.table_name == remove)).first()
            print(f'Removed talble: {added_tables.table_name}')
            print(f'List of tables to query after removing: {tables_to_query}')
            return {"table_name":added_tables.table_name, "logical_entity":added_tables.logical_entity, "description":added_tables.description}     
        else:
            return {}
    else:
        user_tables = Tables.query.filter(Tables.user_id==current_user.id)
    added_tables = Tables.query.filter(Tables.user_id==current_user.id, and_(Tables.table_name.in_(tables_to_query)))
    return render_template("tables.html", user_tables=user_tables, added_tables=added_tables, tables_to_query=tables_to_query)


@app.route("/columns")  
@login_required
def columns():
    q = request.args.get("q")
    q = q.replace(' ','%')
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
        user_columns = Columns.query.filter_by(user_id=current_user.id).limit(1000).all()
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
                                                ).order_by(Columns.id)
    else:
        user_table_columns = Columns.query.filter_by(user_id=current_user.id, table_name=table_columns)
    return render_template("columns.html", columns=user_table_columns, table_name=table_columns)


##################
# upload webpage #
##################
@app.route("/upload")
@login_required
def upload():
    formTablesFile = UploadTablesFile()
    formColumnsFile = UploadColumnsFile()
    formRelationshipsFile = UploadRelationshipsFile()
    return render_template('upload.html', 
                            formTablesFile=formTablesFile,
                            formColumnsFile=formColumnsFile,
                            formRelationshipsFile=formRelationshipsFile)


@app.route("/upload/tables", methods=['POST'])
@login_required
def upload_tables():
    formTablesFile = UploadTablesFile()
    formColumnsFile = UploadColumnsFile()
    formRelationshipsFile = UploadRelationshipsFile()
    if formTablesFile.validate_on_submit():
        db.session.commit()
        flash(f'File processed correctly!', 'success')
        return redirect(url_for('tables'))
    return render_template('upload.html', 
                            formTablesFile=formTablesFile,
                            formColumnsFile=formColumnsFile,
                            formRelationshipsFile=formRelationshipsFile)


@app.route("/upload/columns", methods=['POST'])
@login_required
def upload_columns():
    formTablesFile = UploadTablesFile()
    formColumnsFile = UploadColumnsFile()   
    formRelationshipsFile = UploadRelationshipsFile()
    if formColumnsFile.validate_on_submit():
        db.session.commit()
        flash(f'File processed correctly!', 'success')
        return redirect(url_for('columns'))
    return render_template('upload.html', 
                            formTablesFile=formTablesFile,
                            formColumnsFile=formColumnsFile,
                            formRelationshipsFile=formRelationshipsFile)


@app.route("/upload/relationships", methods=['POST'])
@login_required
def upload_relationships():
    formTablesFile = UploadTablesFile()
    formColumnsFile = UploadColumnsFile()
    formRelationshipsFile = UploadRelationshipsFile()
    if formRelationshipsFile.validate_on_submit():
        db.session.commit()
        flash(f'File processed correctly!', 'success')
        return redirect(url_for('tables'))
    return render_template('upload.html', 
                            formTablesFile=formTablesFile,
                            formColumnsFile=formColumnsFile,
                            formRelationshipsFile=formRelationshipsFile)