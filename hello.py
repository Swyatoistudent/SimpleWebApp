from flask import Flask
import flask
import database

app = Flask(__name__)
database.init_db()
@app.route('/')
def root():
    db = database.get_db()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM todolists""")
    todolists = cursor.fetchall()
    return flask.render_template("root.html", data=todolists)


@app.route('/project_add', methods=["POST"])
def put_project():
    db = database.get_db()
    cursor = db.cursor()
    cursor.execute("""INSERT INTO todolists(project_name) VALUES ('{}')""".format(flask.request.form['project']))
    db.commit()
    return flask.redirect(flask.url_for('root'))


@app.route('/delete_project', methods=["POST"])
def delete_project():
    db = database.get_db()
    cursor = db.cursor()
    cursor.execute(f"""DELETE FROM project where project_id = {flask.request.form['delete_project']}""")
    cursor.execute(f"""DELETE FROM todolists where id = {flask.request.form['delete_project']}""")
    db.commit()
    return flask.redirect(flask.url_for('root'))


@app.route('/<id>', methods=["GET"])
def todolist(id):
    db = database.get_db()
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM project Where project_id = {id}""")
    items_list = cursor.fetchall();
    return flask.render_template("index.html", data=items_list, project_id=id)


@app.route('/<id>/item_add', methods=["POST"])
def put_item(id):
    db = database.get_db()
    cursor = db.cursor()
    cursor.execute(f"""INSERT INTO project(project_id,item) VALUES ('{id}','{flask.request.form['item']}')""")
    db.commit()
    return flask.redirect(f'/{id}')


@app.route('/<id>/delete_item', methods=["POST"])
def delete_item(id):
    db = database.get_db()
    cursor = db.cursor()
    cursor.execute(f"""DELETE FROM project WHERE item_id = {flask.request.form['delete_files']}""")
    db.commit()
    return flask.redirect(f'/{id}')
