import os
import logging
import requests
import json
from xml.etree import ElementTree


class ProviderException(Exception):
    pass


class FlickrProvider:
    BASE_URL = 'https://www.flickr.com/services/rest/'
    MAX_ITEMS_PER_PAGE = 10

    def get_photos(self, **kwargs):
        if 'text' in kwargs:
            # search if provided with text to search
            payload = {'method': 'flickr.photos.search', 'text': kwargs.get('text')}
        else:
            payload = {'method': 'flickr.photos.getRecent'}
        logging.debug("Fetching images: %r", payload)
        ret = self._get(payload=payload)
        return ret

    def _get(self, payload):
        res = requests.get(self.BASE_URL,
                           params={**payload, 'api_key': os.getenv('FLICKR_KEY'), 'per_page': self.MAX_ITEMS_PER_PAGE})
        if res.status_code != 200:
            raise ProviderException(f"Failed to fetch data from Flickr: {res.status_code}, {res.text}")
        
        tree = ElementTree.fromstring(res.content)
        return [photo.attrib for photo in tree.iter('photo')]
