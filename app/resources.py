import logging
import os
from sqlalchemy import desc, asc, or_
from flask import Flask, request, url_for
from flask_restful import Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from app.providers import FlickrProvider


feed_post = { 'id': fields.Integer, 'title': fields.String, 'owner': fields.String, 'secret': fields.String,
              'server': fields.String}
feed_response = {'error': fields.String,
                 'data': fields.Nested(feed_post, allow_null=True),
                 'prev_url': fields.String,
                 'next_url': fields.String,
                }

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_CONN_STR']

api = Api(app)
db = SQLAlchemy(app)


class FlickrPost(db.Model):
    __tablename__ = 'flickr'
    id = db.Column(db.Integer, primary_key=True)
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

class FlickrFeed(Resource):
    PROVIDER = FlickrProvider()
    @marshal_with(feed_response)
    def get(self):
        logging.debug("Feed request with args=%r", request.args)
        return {'data': self.PROVIDER.get_photos(**request.args)}


class FlickrFavorite(Resource):
    POSTS_PER_PAGE = 10

    @marshal_with(feed_response)
    def get(self):
        logging.debug("Get Favorite request with args=%r", request.args)
        asc_or_desc = asc
        field_to_order_by = None

        args = {**request.args}
        order_by = args.pop('order_by', None)
        if order_by:
            if not hasattr(FlickrPost, order_by):
                return {"error": f"unknown fields to be ordered by: {order_by}"}
            field_to_order_by = getattr(FlickrPost, order_by)

        _desc = args.pop('desc', None)
        if _desc:
            asc_or_desc = desc

        page = int(args.pop('page', 1))

        qs = FlickrPost.query
        filters = []
        for field, value  in args.items():
            if hasattr(FlickrPost, field):
                filters.append(getattr(FlickrPost, field) == value)

        if filters:
            logging.debug("search by: %r", filters)
            qs = qs.filter(or_(*filters))
    
        posts = qs.order_by(asc_or_desc(field_to_order_by)).paginate(page, self.POSTS_PER_PAGE, False)

        next_url = url_for('flickrfavorite', page=posts.next_num) if posts.has_next else None
        prev_url = url_for('flickrfavorite', page=posts.prev_num) if posts.has_prev else None

        return {'data': [post.to_dict() for post in posts.items], 'prev_url': prev_url, 'next_url': next_url}

    def post(self):
        logging.debug("Post Favorite request with json=%r", request.json)
        try:
            db.session.add(FlickrPost(**request.json))
            db.session.commit()
        except Exception as exc:
            logging.exception("Failed to mark %r as favorite", request.json)
            return {'error': f'Failed to mark {request.json} as favorite'}, 400

        return {'data': 'Post marked as favorite'}

    def delete(self):
        logging.debug("Delete Favorite request with args=%r", request.args)
        if 'id' not in request.args:
            return dict(error=f'id paramter is required for deletion'), 404
        post_id_to_delete = request.args.get('id').split(',')
        deleted_count = FlickrPost.query.filter(FlickrPost.id.in_(post_id_to_delete)).delete()
        db.session.commit()
        logging.debug("Removed %r favorite posts", deleted_count)

        return {'data': deleted_count}

api.add_resource(FlickrFeed, '/feed')
api.add_resource(FlickrFavorite, '/favorites')
db.create_all()
