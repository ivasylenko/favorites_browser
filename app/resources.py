import logging
import os
from sqlalchemy import desc, asc, or_
from flask import request, url_for
from flask_restful import Resource, fields, marshal_with

from app.config import Config
from app.providers import FlickrProvider
from app.models import FlickrPost, FLICKR_POST_FIELDS
from app.application import FlaskApplication
db = FlaskApplication.DB

FLICKR_POST_RESPONSE_FIELDS = {'error': fields.String,
                               'data': fields.Nested(FLICKR_POST_FIELDS, allow_null=True),
                               'prev_url': fields.String,
                               'next_url': fields.String}


class FlickrFeed(Resource):
    PROVIDER = FlickrProvider()

    @marshal_with(FLICKR_POST_RESPONSE_FIELDS)
    def get(self):
        """Retrieve Posts from Origin
        Either most recent or search by text if `text` provided
        """
        logging.debug('Get Flickr Posts: args=%r', request.args)
        text = request.args.get('text')
        posts = self.PROVIDER.get_photos(text=text)
        logging.debug("Fetched posts: %r", posts)
        return {'data': posts}


class FlickrFavorite(Resource):
    @marshal_with(FLICKR_POST_RESPONSE_FIELDS)
    def get(self):
        """Handles Favorites Posts
        parameters:
        order_by - field
        order - one of (asc, desc)
        page - number of page to fetch

        all further parameters are considered for search with logical OR e.g.
        ?server=123&tags=cosmos - will returns all Posts that has cosmos title or 123 as a server
        parameters should correspond to Model fields
        """
        asc_or_desc = asc
        field_to_order_by = None

        args = {**request.args}
        logging.debug('Get Favorite Flickr Posts: args=%r', args)

        order_by = args.pop('order_by', None)
        if order_by:
            if not hasattr(FlickrPost, order_by):
                return {'error': f'unknown fields to be ordered by: {order_by}'}, 400
            field_to_order_by = getattr(FlickrPost, order_by)

        order = args.pop('order', None)
        if order == 'desc':
            asc_or_desc = desc

        page = args.pop('page', 1)
        try:
            if not isinstance(page, int):
                page = int(page)
        except ValueError as exc:
            logging.exception('Invalid page=%r parameter', page)
            return {'error': f'failed parsing page parameter: {page}'}, 400

        # All other parameters are considered for search
        qs = FlickrPost.query
        filters = []
        for field, value  in args.items():
            if hasattr(FlickrPost, field):
                filters.append(getattr(FlickrPost, field) == value)

        if filters:
            qs = qs.filter(or_(*filters))

        if field_to_order_by:
            qs = qs.order_by(asc_or_desc(field_to_order_by))

        posts = qs.paginate(page, Config.POSTS_PER_PAGE, False)
        
        data = [post.to_dict() for post in posts.items]
        next_url = url_for('flickrfavorite', page=posts.next_num) if posts.has_next else None
        prev_url = url_for('flickrfavorite', page=posts.prev_num) if posts.has_prev else None

        return {'data': data, 'prev_url': prev_url, 'next_url': next_url}

    def post(self):
        """Allows to submit json Post - to mark as favorite
        """
        logging.debug('Post Favorite request with json=%r', request.json)
        try:
            post_to_mark = FlickrPost(**request.json)
            db.session.add(post_to_mark)
            db.session.commit()
        except Exception as exc:
            logging.exception('Failed to mark %r as favorite', request.json)
            return {'error': f'Failed to mark {request.json} as favorite'}, 400

        return {'data': f'Post {post_to_mark.id} marked as favorite'}

    def delete(self):
        """Allows to submit Favorites Posts ids to remove - unmark
        parameters:
        id - comma-separated list of ids
        """
        logging.debug('Delete Favorite request with args=%r', request.args)
        if 'id' not in request.args:
            return {'error': f'id paramter is required for deletion'}, 400

        ids_to_delete = request.args.get('id').split(',')

        deleted_count = FlickrPost.query.filter(FlickrPost.id.in_(ids_to_delete)).delete()
        db.session.commit()

        logging.debug('Removed %r favorite posts', deleted_count)

        return {'data': deleted_count}

def assign_resources(api):
    api.add_resource(FlickrFeed, '/feed')
    api.add_resource(FlickrFavorite, '/favorites')
