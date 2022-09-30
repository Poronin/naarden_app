from naarden import db, login_manager
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash = db.Column(db.Text(), nullable=False)
    table_id = db.relationship('Tables', backref='user_tables', lazy=True)
    column_id = db.relationship('Columns', backref='user_columns', lazy=True)


class Tables(db.Model):
    __tablename__ = 'tables'
    #id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    table_name = db.Column(db.Text(), nullable=False, primary_key=True)
    logical_entity = db.Column(db.Text(), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    category = db.Column(db.String(20), nullable=True)


class Columns(db.Model):
    __tablename__ = 'columns'
    #id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    column_name = db.Column(db.Text(), nullable=False, primary_key=True)
    logical_entity = db.Column(db.Text(), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    type = db.Column(db.String(20), nullable=True)
    length = db.Column(db.String(10), nullable=True)
    key = db.Column(db.String(1), nullable=True)
    virtual = db.Column(db.String(1), nullable=True)


def __repr__(self):
    return f"User('{self.username}', '{self.email}',{self.hash})"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))