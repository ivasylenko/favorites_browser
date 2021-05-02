import os
import logging
import requests
import json
from xml.etree import ElementTree

from app.config import Config


class ProviderException(Exception):
    pass


class FlickrProvider:
    def get_photos(self, text=None):
        """Allows to
        1. Fetch up to Config.POSTS_PER_PAGE recent Flickr Posts.
        2. Search Flickr Posts by `text` provided.
        """
        payload = {'method': 'flickr.photos.getRecent'}

        if text:
            payload['method'] = 'flickr.photos.search'
            payload['text'] = text

        logging.debug("Fetch Flickr Posts request payload=%r", payload)
        res = requests.get(Config.FLICKR_URL, params={**payload, 'api_key': Config.FLICKR_KEY,
                                                      'per_page': Config.POSTS_PER_PAGE})
        if res.status_code != 200:
            raise ProviderException(f"Failed to fetch data from Flickr: {res.status_code}, {res.text}")

        tree = ElementTree.fromstring(res.content)

        return [photo.attrib for photo in tree.iter('photo')]
