import os
import logging

from app.config import Config
from app.application import FlaskApplication

logging.basicConfig(level=logging.DEBUG if Config.DEBUG else logging.INFO)


if __name__ == '__main__':
    FlaskApplication.construct_app()
    FlaskApplication.run()
