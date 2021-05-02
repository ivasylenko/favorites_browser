import logging
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from app.config import Config


class FlaskApplication:
    APP = None
    API = None
    DB = None

    @classmethod
    def construct_app(cls):
        logging.info("Create Favorites Feed app")
        assert not (cls.APP or cls.API or cls.DB)

        cls.APP = Flask(__name__)
        cls.APP.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI

        cls.API = Api(cls.APP)
        cls.DB = SQLAlchemy(cls.APP)

        # this import is here to avoid circular imports
        from app.resources import assign_resources
        assign_resources(cls.API)

        return cls.APP