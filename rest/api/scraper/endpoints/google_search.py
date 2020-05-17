from flask import request, jsonify
from flask_restplus import Resource, reqparse
from rest.api.restplus import api
from rest.api.scraper.required_parameters import google_params
from urllib.parse import urlparse
from googlesearch import search
import logging

# Defining logging object
log = logging.getLogger(__name__)

# Defining request parser object in order to read input from user and adding the arguments required to be entered from the user.
request_parser = reqparse.RequestParser()
request_parser.add_argument('SEARCH_QUERY', type=str, required=True, default=None, help='Enter the search query')
request_parser.add_argument('look_back', type=str, required=False, default='day', help='Pick one from hour/day/week/month/year. Default is day')


# Defining namespace for this endpoint
ns = api.namespace('scraper/google_search', description='GoogleSearch')

exclusion = google_params['exclusion']

def url_purifier(url):
	"""	This function returns True if the First Level Domain(FLD) not in exclusion list else returns False """
	domains = urlparse(url).netloc.split('.')
	for domain in domains:
		if domain in exclusion:
			return False
	return True


# Routing webservice
@ns.route('/')
class GoogleSearch(Resource):
	# Expecting an input query/search string
	@api.expect(request_parser)
	def get(self):
		""" Searches input query/search string in GOOGLE and returns urls of search results excluded from certain domains. """
		args = request_parser.parse_args(request)
		query = args.get('SEARCH_QUERY').strip()
		lookback = args.get('look_back').strip()
		try:
			tbs = google_params['default_tbs_lookback']
			if lookback != None and lookback in google_params['tbs_look_back']:
				tbs = 'qdr:'+lookback[0]
			result = list(search(query, tbs=tbs, start=google_params['start'], stop=google_params['stop']))
			result = [r for r in result if url_purifier(r) == True]
			return jsonify(search_query=query, google_search_results=result, error_message='None', lookback=tbs)
		except Exception as e:
			return jsonify(search_query=query, google_search_results='None', error_message=str(e))