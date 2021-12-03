from dbworker import db
from datetime import datetime

class mail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    mail = db.Column(db.String(100))
    clear = db.Column(db.String(100))
    video = db.Column(db.String(10), default="N/A")
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'mail ' + str(self.id)

class access(db.Model):
    __bind_key__ = 'TWO'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    pw = db.Column(db.String(100), nullable=False)

class final(db.Model):
    __bind_key__ = 'THREE'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    mail = db.Column(db.String(100))
    clear = db.Column(db.String(100))
    video = db.Column(db.String(100), nullable=False)

