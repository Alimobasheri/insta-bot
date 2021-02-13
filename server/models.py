from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    captions = db.relationship('Caption', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Caption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), unique=True, nullable=False)
    file_path = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_updating =  db.Column(db.Boolean, unique=True, nullable=False)
class FakeUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
