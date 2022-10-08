import errno
from xml.dom import ValidationErr
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from naarden.models import Users, Tables, Columns, Relationships
import json
from naarden import db
from sqlalchemy import and_, or_, not_ , update

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('User already exists')
    
    def validate_email(self, email):
        email = Users.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already exists')
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log-in')


class UploadTablesFile(FlaskForm):
    file = FileField('File containing the tables:', validators=[FileAllowed(['json'])])
    submit = SubmitField('Upload')

    def validate_file(self, file):
        try:
            f = json.load(self.file.data)
            for l in f:
                foundField = Tables.query.filter(Tables.user_id == int(current_user.id), 
                                                 and_( Tables.table_name == l['tab_log_prop'] )).first()
                if not foundField:
                    # field not found then create
                    newTable = Tables( user_id = int(current_user.id),
                                       table_name = l['tab_log_prop'],
                                       logical_entity = l['tab_nam'],
                                       description = l['tab_desc'],
                                       #category = l['tab_cat']
                                    )
                    db.session.add(newTable)
                else:
                    # field found then update
                    foundField.user_id = int(current_user.id)
                    foundField.table_name = l['tab_log_prop']
                    foundField.logical_entity = l['tab_nam']
                    foundField.description = l['tab_desc']
                    #foundField.category = l['tab_cat']
        except:
            raise ValidationError("File contains errors")


class UploadColumnsFile(FlaskForm):
    file = FileField('File containing the tables:', validators=[FileAllowed(['json'])])
    submit = SubmitField('Upload')

    def validate_file(self, file):
        try:
            f = json.load(self.file.data)
            for l in f:
                foundField = Columns.query.filter(Columns.user_id == int(current_user.id), 
                                                    and_( Columns.table_name == l['tab_log_prop'],
                                                          Columns.column_name == l['fld_log_prop'] )
                                                ).first()
                if not foundField:
                    # field not found then create
                    newTable = Columns( user_id = int(current_user.id),
                                        table_name = l['tab_log_prop'],
                                        column_name = l['fld_log_prop'],
                                        id = l['fld_nr'],
                                        logical_entity = l['fld_nam'],
                                        description = l['fld_desc'],
                                        type = l['fld_typ'],
                                        length = l['fld_len'],
                                        key = l['fld_key'],
                                        virtual = l['fld_virt']
                                    )
                    db.session.add(newTable)
                else:
                    # field found then update
                    foundField.user_id = int(current_user.id)
                    foundField.table_name = l['tab_log_prop']
                    foundField.column_name = l['fld_log_prop']
                    foundField.id = l['fld_nr']
                    foundField.logical_entity = l['fld_nam']
                    foundField.description = l['fld_desc']
                    foundField.type = l['fld_typ']
                    foundField.length = l['fld_len']
                    foundField.key = l['fld_key']
                    foundField.virtual = l['fld_virt']
        except :
            raise ValidationError("File contains errors")


class UploadRelationshipsFile(FlaskForm):
    file = FileField('File containing the tables:', validators=[FileAllowed(['json'])])
    submit = SubmitField('Upload')

    def validate_file(self, file):
        # JSON to string
        f = json.load(self.file.data)
        relationships_str = json.dumps(f)
        foundField = Relationships.query.filter(Columns.user_id == int(current_user.id)).first()
        if not foundField:
            # field not found then create
            new_relationships = Relationships(user_id=int(current_user.id), file=relationships_str)
        else:
            # field found then update  
            foundField.file = relationships_str
        db.session.add(new_relationships)