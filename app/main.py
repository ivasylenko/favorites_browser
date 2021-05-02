import os
import logging

from app.config import Config
from app.application import FlaskApplication

logging.basicConfig(level=logging.DEBUG if Config.DEBUG else logging.INFO)

app = FlaskApplication.construct_app()

if __name__ == '__main__':
    app.run()
