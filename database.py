import sqlite3
from flask import g, Flask
import click
from flask.cli import with_appcontext
import sqlalchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = sqlalchemy.create_engine('sqlite:///my.db')


class Todolists(Base):
    __tablename__ = 'todolists'
    id = sqlalchemy.Column(Integer, primary_key=True, autoincrement=True)
    project_name = sqlalchemy.Column(String)


class project(Base):
    __tablename__ = 'project'
    item_d = sqlalchemy.Column(Integer, primary_key=True, autoincrement=True)
    project_id = sqlalchemy.Column(Integer, ForeignKey('todolists.id'))
    item = sqlalchemy.Column(String)

    # cursor = db.cursor()
    # cursor.executescript("""CREATE TABLE IF NOT EXISTS todolists(
    #                 id INTEGER  PRIMARY KEY AUTOINCREMENT,
    #                 project_name TEXT
    #                 );
    # """)
    # cursor.executescript("""CREATE TABLE IF NOT EXISTS project(
    #       item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #       project_id INTEGER,
    #       item TEXT,
    #       foreign key (project_id) references todolists (id)
    # );
    # """)


Base.metadata.create_all(engine)
