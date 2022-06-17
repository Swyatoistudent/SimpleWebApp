import flask
from flask import Blueprint,g
from flaskr.project.models import Project,TodoList
from flaskr import db
from flaskr.auth.views import login_required
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
bp = Blueprint("project", __name__)

@bp.route('/')
def root():
    todolists =Project.query.filter_by(id=1).all()
    return {'data':
                [{"id":i.id,
                  "user_id":i.user_id,
                  "name": i.name}
                 for i in todolists]},\
           200
@bp.route('/project_add', methods=["POST"])
def put_project():
    db.session.add(Project(user_id=1,name=flask.request.json['name']))
    db.session.commit()
    return 'ok',200


@bp.route('/projects/delete_project', methods=["POST"])
@login_required
def delete_project():
    Project.query.filter_by(id = flask.request.form['delete_project']).delete()
    TodoList.query.filter_by(project_id=flask.request.form['delete_project']).delete()
    db.session.commit()
    return flask.redirect(flask.url_for('root'))

@bp.route('/projects/<id>')
def todolist(id):

    items_list = db.session.query(TodoList).filter_by(project_id = id).all()
    return {'items': [{"project_id":i.project_id,
                       "item_id":i.item_id,"user_id":i.user_id,
                       "item": i.item}
                      for i in items_list]},\
           200
#
#
@bp.route('/projects/<id>/item_add', methods=["POST"])
def put_item(id):

    db.session.add(TodoList(project_id =id,item=flask.request.json['item']))
    db.session.commit()
    return 'ok',200
#
#
@bp.route('/projects/<id>/delete_item', methods=["POST"])
@login_required
def delete_item(id):
    TodoList.query.filter_by(item_id = flask.request.form['delete_files']).delete()

    db.session.commit()
    return flask.redirect(f'/projects/{id}')



