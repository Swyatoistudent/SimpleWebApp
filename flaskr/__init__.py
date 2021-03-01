import os

import click
from flask import Flask, g
import flask
from flask.cli import with_appcontext
from sqlalchemy.orm import sessionmaker

import sqlalchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)
    # SQLITE path
    db_path = os.path.join(app.instance_path, "flaskr.sqlite")
    db_url = f"sqlite:///{db_path}"

    os.makedirs(app.instance_path, exist_ok=True)
    print(db_url)
    app.config.from_mapping(
        SECRET_KEY='dev',
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
# class Todolists(Base):
#     __tablename__ = 'todolists'
#     id = sqlalchemy.Column(Integer, primary_key=True, autoincrement=True)
#     project_name = sqlalchemy.Column(String)
#     def __init__(self,project_name):
#         self.project_name = project_name
#
# class Project(Base):
#     __tablename__ = 'project'
#     item_d = sqlalchemy.Column(Integer, primary_key=True, autoincrement=True)
#     project_id = sqlalchemy.Column(Integer, ForeignKey('todolists.id'))
#     item = sqlalchemy.Column(String)
#
#     def __init__(self, project_id,item):
#         self.project_id = project_id
#         self.item = item
#
#
# Session = sessionmaker(bind=engine)
# Base.metadata.create_all(engine)
#
#
# @app.route('/')
# def root():
#     session = Session()
#     todolists =session.query(Todolists).all()
#     session.close()
#     return flask.render_template("root.html", data=todolists)
#
#
# @app.route('/project_add', methods=["POST"])
# def put_project():
#     session = Session()
#     session.add(Todolists(flask.request.form['project']))
#     session.commit()
#     session.close()
#     return flask.redirect(flask.url_for('root'))
#
#
# @app.route('/delete_project', methods=["POST"])
# def delete_project():
#     session = Session()
#     session.query(Todolists).filter_by(id = flask.request.form['delete_project']).delete()
#     session.query(Project).filter_by(project_id = flask.request.form['delete_project']).delete()
#     session.commit()
#     session.close()
#     return flask.redirect(flask.url_for('root'))
#
#
# @app.route('/<id>')
# def todolist(id):
#     session = Session()
#     items_list = session.query(Project).filter_by(item_d = id)
#     return flask.render_template("index.html", data=items_list, project_id=id)
#
#
# @app.route('/<id>/item_add', methods=["POST"])
# def put_item(id):
#     session = Session()
#     session.add(Project(id,flask.request.form['item']))
#     session.commit()
#     session.close()
#     return flask.redirect(f'/{id}')
#
#
# @app.route('/<id>/delete_item', methods=["POST"])
# def delete_item(id):
#     session = Session()
#     session.query(Project).filter_by(item_d = flask.request.form['delete_files']).delete()
#     session.commit()
#     session.close()
#     return flask.redirect(f'/{id}')

