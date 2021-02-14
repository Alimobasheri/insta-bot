from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    captions = db.relationship('Caption', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Caption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), unique=False, nullable=False)
    filePath = db.Column(db.String(120), unique=False, nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)

class Updates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isUpdating =  db.Column(db.String(5), unique=False, nullable=False)
class FakeUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
