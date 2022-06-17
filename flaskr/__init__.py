import os
from flask_cors import CORS
import click
from flask import Flask, g
from flask_jwt_extended import JWTManager
from flask.cli import with_appcontext



import sqlalchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    jwt = JWTManager(app)


    # SQLITE path
    db_path = os.path.join(app.instance_path, "flaskr.sqlite")
    db_url = f"sqlite:///{db_path}"

    os.makedirs(app.instance_path, exist_ok=True)
    print(db_url)
    app.config.from_mapping(
        SECRET_KEY='r.i.p my motherboard',
        SQLALCHEMY_DATABASE_URI= db_url

    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # initial db
    db.init_app(app)

    app.cli.add_command(init_db_command)
    from flaskr import project,auth
    app.register_blueprint(auth.bp)
    app.register_blueprint(project.bp)
    app.add_url_rule("/", endpoint="root")
    return app

def init_db():
    db.drop_all()
    db.create_all()

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")

