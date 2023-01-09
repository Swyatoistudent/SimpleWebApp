from flaskr import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(80),  nullable=False)


class TodoList(db.Model):
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    item = db.Column(db.String(80))

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    time = db.Column(db.String(80))
    number = db.Column(db.Integer)