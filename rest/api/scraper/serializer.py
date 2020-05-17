from flask_restplus import fields
from rest.api.restplus import api

news = api.model('HTML Scraper', {
    'url_txt': fields.String(required=True, description='HTML Scraper URL'),
})

content = api.model('Content', {
    'cntnt': fields.String(required=True, describtion='Article Content'),
    'title': fields.String(required=True, describtion='Article Title'),
    'jobnm': fields.String(required=True, describtion='Job Name'),
    'tag': fields.String(required=True, description="Tag"),
    'weight': fields.Float(required=True, description="Weight"),
    'original': fields.String(required=True, description="Original Content"),
    'keyword': fields.List(fields.String,required=True,description="Keywords"),
    'run_ts': fields.DateTime(required=True, description="Run Time stamp"),
    'id':fields.String(required=True, description="ID"),
    'url':fields.String(required=True,description="url"),
    'meta_type':fields.String(required=True,description="meta_type"),
    'pub_ts': fields.DateTime(required=True, description="Run Time stamp"),
    'summary': fields.String(required=True, description="Original Content")
})
