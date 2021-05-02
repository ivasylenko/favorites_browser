import os
import logging
from dotenv import load_dotenv
load_dotenv()
from app.resources import app, db, FlickrPost

logging.basicConfig(level=logging.DEBUG if os.getenv('DEBUG') else logging.INFO)


if __name__ == '__main__':
    app.run()
