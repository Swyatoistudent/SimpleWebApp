import click
from flask import Flask
import flask
from sqlalchemy.orm import sessionmaker

import sqlalchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = sqlalchemy.create_engine('sqlite:///my.db')


class Todolists(Base):
    __tablename__ = 'todolists'
    id = sqlalchemy.Column(Integer, primary_key=True, autoincrement=True)
    project_name = sqlalchemy.Column(String)
    def __init__(self,project_name):
        self.project_name = project_name

class Project(Base):
    __tablename__ = 'project'
    item_d = sqlalchemy.Column(Integer, primary_key=True, autoincrement=True)
    project_id = sqlalchemy.Column(Integer, ForeignKey('todolists.id'))
    item = sqlalchemy.Column(String)

    def __init__(self, project_id,item):
        self.project_id = project_id
        self.item = item

app = Flask(__name__)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


@app.route('/')
def root():
    session = Session()
    todolists =session.query(Todolists).all()
    session.close()
    return flask.render_template("root.html", data=todolists)


@app.route('/project_add', methods=["POST"])
def put_project():
    session = Session()
    session.add(Todolists(flask.request.form['project']))
    session.commit()
    session.close()
    return flask.redirect(flask.url_for('root'))


@app.route('/delete_project', methods=["POST"])
def delete_project():
    session = Session()
    session.query(Todolists).filter_by(id = flask.request.form['delete_project']).delete()
    session.query(Project).filter_by(project_id = flask.request.form['delete_project']).delete()
    session.commit()
    session.close()
    return flask.redirect(flask.url_for('root'))


@app.route('/<id>')
def todolist(id):
    session = Session()
    items_list = session.query(Project).filter_by(item_d = id)
    return flask.render_template("index.html", data=items_list, project_id=id)


@app.route('/<id>/item_add', methods=["POST"])
def put_item(id):
    session = Session()
    session.add(Project(flask.request.form['item'],id))
    session.commit()
    session.close()
    return flask.redirect(f'/{id}')


@app.route('/<id>/delete_item', methods=["POST"])
def delete_item(id):
    session = Session()
    session.query(Project).filter_by(item_d = flask.request.form['delete_files']).delete()
    session.commit()
    session.close()
    return flask.redirect(f'/{id}')