import logging
import traceback

from flask_restplus import Api
from rest import settings

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Python Scraper',
          description='Python Scraper Application')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500



