import flask
from flaskr.auth.models import Users
from flask import Blueprint
from functools import wraps
from flaskr import db
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



@bp.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username= username,password=password).first()
        if user is None:
            return flask.render_template("login.html",massage = "login failed")
        session['user_id'] = user.id
        return flask.redirect(url_for('root'))
    else:
        return flask.render_template("login.html")
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