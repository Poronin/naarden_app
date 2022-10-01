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
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}',{self.hash})"


class Tables(db.Model):
    __tablename__ = 'tables'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),primary_key=True)
    table_name = db.Column(db.Text(), primary_key=True)
    logical_entity = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    category = db.Column(db.String(20), nullable=True)
    column_id = db.relationship('Columns', backref='table_columns', lazy=True)
    
    def __repr__(self):
        return f"User('{self.user_id}', '{self.table_name}','{self.logical_entity}', '{self.description}','{self.category}')"


class Columns(db.Model):
    __tablename__ = 'columns'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    table_name = db.Column(db.Text, db.ForeignKey('tables.table_name'), primary_key=True)
    column_name = db.Column(db.Text(), primary_key=True)
    logical_entity = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    type = db.Column(db.String(20), nullable=True)
    length = db.Column(db.String(10), nullable=True)
    key = db.Column(db.String(1), nullable=True)
    virtual = db.Column(db.String(1), nullable=True)

    def __repr__(self):
        return f"User('{self.user_id}', '{self.table_name}', '{self.column_name}','{self.logical_entity}', '{self.description}','{self.type}', '{self.length}', '{self.key}','{self.virtual}')"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))