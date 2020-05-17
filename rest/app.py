import logging.config
import os
from flask import Flask, Blueprint
from rest import settings
from rest.api.scraper.endpoints.newspaper_scraper import ns as article_scraper_namespace
from rest.api.scraper.endpoints.rss_scraper import ns as rss_namespace
from rest.api.scraper.endpoints.google_search import ns as google_search_namespace
#from rest.api.scraper.endpoints.elastic_search import ns as elastic_search_namespace
from rest.api.scraper.endpoints.template_scraper import ns as temp_namespace
from rest.api.restplus import api

app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

#Add all the required namespaces into below list in order to register them in API
namespaces_included = [article_scraper_namespace,rss_namespace,google_search_namespace,temp_namespace]

def configure_app(flask_app):
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    for namesps in namespaces_included:
        api.add_namespace(namesps)
    flask_app.register_blueprint(blueprint)


def main():
    initialize_app(app)
    #log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    #app.run(host=settings.FLASK_SERVER_NAME,port=settings.FLASK_SERVER_PORT)
    app.run(host='localhost',port=8890) 


if __name__ == "__main__":
    main()
