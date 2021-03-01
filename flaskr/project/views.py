import flask
from flask import Blueprint,g
from flaskr.project.models import Project,TodoList
from flaskr import db
from flaskr.auth.views import login_required
bp = Blueprint("project", __name__)
@bp.route('/')
@login_required
def root():
    todolists =Project.query.filter_by(user_id =g.user.id).all()
    return flask.render_template("root.html", data=todolists)
@bp.route('/project_add', methods=["POST"])
@login_required
def put_project():
    db.session.add(Project(user_id=g.user.id,name=flask.request.form['project']))
    db.session.commit()
    return flask.redirect(flask.url_for('root'))


@bp.route('/projects/delete_project', methods=["POST"])
@login_required
def delete_project():
    Project.query.filter_by(id = flask.request.form['delete_project']).delete()
    TodoList.query.filter_by(project_id=flask.request.form['delete_project']).delete()
    db.session.commit()
    return flask.redirect(flask.url_for('root'))

@bp.route('/projects/<id>')
@login_required
def todolist(id):

    items_list = db.session.query(TodoList).filter_by(project_id = id,user_id = g.user.id).all()
    return flask.render_template("index.html", data=items_list, project_id=id)
#
#
@bp.route('/projects/<id>/item_add', methods=["POST"])
@login_required
def put_item(id):

    db.session.add(TodoList(user_id=g.user.id,project_id =id,item=flask.request.form['item']))
    db.session.commit()
    return flask.redirect(f'/projects/{id}')
#
#
@bp.route('/projects/<id>/delete_item', methods=["POST"])
@login_required
def delete_item(id):
    TodoList.query.filter_by(item_id = flask.request.form['delete_files']).delete()

    db.session.commit()
    return flask.redirect(f'/projects/{id}')



