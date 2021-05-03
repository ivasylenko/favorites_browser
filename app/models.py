from flask_restful import fields

from app.application import FlaskApplication
db = FlaskApplication.DB


FLICKR_POST_FIELDS = {'id': fields.Integer, 'title': fields.String, 'owner': fields.String,
                      'secret': fields.String, 'server': fields.String}


class FlickrPost(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    owner = db.Column(db.String(80), unique=False, nullable=False)
    secret = db.Column(db.String(80), unique=False, nullable=False)
    server = db.Column(db.String(80), unique=False, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'owner': self.owner,
            'secret': self.secret,
            'server': self.server
        }

    def __repr__(self):
        return f"FlickrPost(id={self.id})"

db.create_all()
