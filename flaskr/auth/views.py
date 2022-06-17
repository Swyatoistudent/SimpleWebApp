import flask
from flaskr.auth.models import Users
from flask import Blueprint,jsonify
from functools import wraps
from flaskr import db

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

bp = Blueprint("auth", __name__)
from flask import g, request, redirect, url_for, session





@bp.before_app_request
def before():

    if 'user_id' in session:
        user = Users.query.filter_by(id=session['user_id']).first()
        g.user = user
    else:
        g.user = None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function



@bp.route('/login', methods=["POST"])
def login():

    username = flask.request.json['username']
    password = flask.request.json['password']
    print(username)
    user = Users.query.filter_by(username= username).first()
    print(user)
    if user is None:
        return 'bad username/password',401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)



@bp.route('/register', methods = ["GET","POST"])
def register():
    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']
        db.session.add(Users(username=username,password=password))
        db.session.commit()
        return flask.redirect(url_for("auth.login"))
    else:
        return flask.render_template("auth.html")
@bp.route('/logout')
def log_out():
    session.pop('user_id')
    return flask.redirect('/login')