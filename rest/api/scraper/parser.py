from flask_restplus import reqparse

request_parser = reqparse.RequestParser()
request_parser.add_argument('url_txt', type=str, required=True, default=None, help='Enter the URL need to be scraped')