from rest.api.restplus import api
from rest.api.scraper.serializer import content
from elasticsearch import Elasticsearch
from flask_restplus import Resource, reqparse
from flask import request, jsonify
from elasticsearch_dsl import Search, Q
import logging

# Defining Elasticsearch Index
es = Elasticsearch()

# Defining logging object
log = logging.getLogger(__name__)

# Defining request parser object in order to read input from user and adding the arguments required to be entered from the user.
request_parser = reqparse.RequestParser()
request_parser.add_argument('cntnt', type=str, required=True, default=None, help='Enter the search content')
ns = api.namespace('scraper/search', description='Elastic Search')


@ns.route('/')
class ElstcSearch(Resource):

    @api.expect(request_parser)
    def get(self):
        args = request_parser.parse_args(request)
        content = args.get('cntnt')
        s = Search().query("multi_match", query=content, fields=['title', 'cntnt'])
        query = s.to_dict()
        print(query)
        result = es.search(index="cii_cntnt", body=query)
        return jsonify(result)

    @api.response(201, 'Content successfully created.')
    @api.expect(content)
    def post(self):
        """
           Indexing Content.
        """
        data = request.json
        result = es.index(index='cii_cntnt', doc_type="content", body=data)
        return None, 201
