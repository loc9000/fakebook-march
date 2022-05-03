from enum import unique
import uuid
from datetime import datetime as dt
from app import db

# MVC DESIGN PATTERN

class User(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(300))
    posts = db.relationship('Post', backref='posts', cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4().hex

    def __repr__(self):
        return f'<User: {self.email}>'


class Post(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    body = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    author = db.Column(db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
            'date_created': self.date_created,
            'author': User.query.get(self.author)
        }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4().hex

    def __repr__(self):
        return f'<Post: {self.body[30]}...>'


# ID10T