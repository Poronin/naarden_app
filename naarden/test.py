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
from naarden.webapp import Model
from naarden.webapp import Node
from naarden.webapp import QueueFrontier
# importing required library
import itertools
from flask import current_app

#app_ctx = app.app_context()
#app_ctx.push()
#current_app.name
#user = Users.query.filter_by(email='test1@gmail.com').first()
#login_user(user, remember=True)

model = Model(1)

# nodes input from user
nodes_to_find = ['HLODPLP', 'HLODPEP']

model.search(nodes_to_find)

model.remove_bidirectional_nodes()

model.solutions
model.nodes
query = model.query()
print(query, end='\n')

#app_ctx.pop()