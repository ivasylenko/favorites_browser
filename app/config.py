import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    DEBUG = 'DEBUG' in os.environ
    POSTS_PER_PAGE = 10
    FLICKR_URL = 'https://www.flickr.com/services/rest/'
    FLICKR_KEY = os.environ['FLICKR_KEY']
