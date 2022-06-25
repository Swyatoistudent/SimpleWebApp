import flask
from flaskr.auth.models import Users
from flask import Blueprint,jsonify
from functools import wraps
from flaskr import db
import jwt
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import decode_token
from flask import Flask, jsonify, make_response, request
bp = Blueprint("auth", __name__)
from flask import g, request, redirect, url_for, session




# @bp.before_app_request
# def before():

#     if 'user_id' in session:
#         user = Users.query.filter_by(id=session['user_id']).first()
#         g.user = user
#     else:
#         g.user = None

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))
#         return f(*args, **kwargs)
#     return decorated_function



# @bp.route('/login', methods=["POST"])
# def login():

#     username = flask.request.json['username']
#     password = flask.request.json['password']
#     print(username)
#     user = Users.query.filter_by(username= username).first()
#     print(user)
#     if user:
#         access_token = create_access_token(identity=username)
#         return jsonify(access_token=access_token)
#     else:
#         return '401'



# @bp.route('/register', methods = ["GET","POST"])
# def register():
#     if request.method == "POST":

#         username = flask.request.json['username']
#         password = flask.request.json['password']
#         db.session.add(Users(username=username,password=password))
#         db.session.commit()
#     return '200'

# @bp.route('/logout')
# def log_out():
#     session.pop('user_id')
#     return flask.redirect('/login')

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
           token = request.headers['Authorization']
        if not token:
           return jsonify({'message': 'a valid token is missing'})

        try:
           data = decode_token(token)
           current_user=Users.query.filter_by(username=data['sub']).first()
        except:
           return 401

        return f(current_user, *args, **kwargs)
   return decorator
@bp.route('/register', methods=['POST'])
def signup_user(): 
   data = request.get_json() 
   hashed_password = data['password']
    
   new_user = Users(username=data['username'], password=hashed_password)
   db.session.add(new_user) 
   db.session.commit()   
   return jsonify({'message': 'registered successfully'})   

@bp.route('/login', methods=['POST']) 
def login_user():
   auth = flask.request.json
  
   user = Users.query.filter_by(username=auth['username']).first()  
   if user:
        if user.password== auth['password']:
            token = create_access_token(identity=user.username)
            return {"access_token" : token}

   return ('could not verify',  401, {'Authentication': '"login required"'})

@bp.route('/logout')
def log_out():
    return 'ok',200