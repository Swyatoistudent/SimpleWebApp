import sqlite3
from flask import g, Flask
import click
from flask.cli import with_appcontext


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("mydb.db")
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.executescript("""CREATE TABLE IF NOT EXISTS todolists(
                    id INTEGER  PRIMARY KEY AUTOINCREMENT,
                    project_name TEXT
                    );
    """)
    cursor.executescript("""CREATE TABLE IF NOT EXISTS project(
          item_id INTEGER PRIMARY KEY AUTOINCREMENT,
          project_id INTEGER,
          item TEXT,
          foreign key (project_id) references todolists (id)
    );
    """)




@click.command('init-db')
@with_appcontext
def db_init():
    init_db()

