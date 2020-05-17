from flask import request, jsonify
from flask_restplus import Resource, reqparse
from rest.api.restplus import api
import logging
import pandas as pd
from urllib.parse import urlparse
from rest.api.scraper.parser import  request_parser
import json, cloudscraper
from bs4 import BeautifulSoup as bs
from newspaper import Article


# Defining logging object
log = logging.getLogger(__name__)

# Creating scraper object
scraper = cloudscraper.create_scraper()


# Defining request parser object for getting input url from user.
request_parser = reqparse.RequestParser()
request_parser.add_argument('URL', type=str, required=True, help='Enter the url')
request_parser.add_argument('block_tag', type=str, required=True, help='Enter the block_tag')
request_parser.add_argument('block_type', type=str, required=True, help='Enter the block_type')
request_parser.add_argument('block_type_name', type=str, required=True,  help='Enter the block_type_name')
request_parser.add_argument('block_prep_url', type=str, required=False, default='', help='Enter the block_prep_url')
#request_parser.add_argument('file_location', type=str, required=True, default=None, help='Enter the absolute path of excel file which has all required attributes')

ns = api.namespace('scraper/temp_scraper', description='Template Scraper')

@ns.route('/')
class TempScraper(Resource):

	@api.expect(request_parser)
	def get(self):
		args = request_parser.parse_args(request)
		url = args.get('URL')
		block_tag = args.get('block_tag')
		block_type = args.get('block_type')
		block_type_name = args.get('block_type_name')
		block_prep_url = args.get('block_prep_url')
		finl_finl = {}
		url_dic = {}
		try:
			url_dic.update({ 'url_txt':url.strip(), 'tag_html_typ':block_tag.strip(), 'sectn_typ':block_type.strip(), 'clas_or_sctn_name':block_type_name.strip(), 'prepend_url_txt':block_prep_url.strip() })
		except Exception as e:
			return jsonify(error_message=str(e)+' ----- 1')
		
		def check(ref):
			for each in ['#','print','login','about','contact','cookie','faq','contact-us','terms','policy','image','video','button','toggle','mail','twitter','instagram','facebook','career','page']:
				if each in ref.lower():
					return True
			if 'news' or 'press' in ref.lower():
				return False
			else:
				return None

		def temp_scrape(url,tag,sec,cls):
			links = []
			tmp_links = []
			try:
				txt = scraper.get(url)
				try:
					txt = txt.text
				except AttributeError:
					txt = txt
				except:
					raise Exception('Issue with cloudscraper')
			except:
				return set(tmp_links)
			soup = bs(txt)
			divs = soup.findAll(tag, {sec : cls})
			for div in divs:
				links = div.findAll('a')
				for link in links:
					ref = link.get('href')
					if ref == None:
						continue
					chk = check(ref)
					if chk != True and chk != None:
						tmp_links.append(ref)
			return set(tmp_links)

		def prep_chk(prep,urls_ext):
			final_links = []
			for u in urls_ext:
				if 'http' in u:
					final_links.append(u)
				elif prep[-1] == '/' and u[0] == '/':
					final_links.append(prep+u[1:])
				elif prep[-1] != '/' and u[0] == '/':
					final_links.append(prep+u)
				elif prep[-1] == '/' and u[0] != '/':
					final_links.append(prep+u)
				elif prep[-1] != '/' and u[0] != '/':
					final_links.append(prep+'/'+u)
				else:
					return set([])
			return set(final_links)

		try:
			if str(url_dic['tag_html_typ']) != '':
				new_tmp = set()
				abs_tmp = set()
				tmp = temp_scrape(url_dic['url_txt'],url_dic['tag_html_typ'],url_dic['sectn_typ'],url_dic['clas_or_sctn_name'])
				prep = str(url_dic['prepend_url_txt'])
				if prep != '' and len(tmp) > 0:
					new_tmp = prep_chk(prep,tmp)
				elif prep == '' and len(tmp) > 0:
					upars = urlparse(url_dic['url_txt']).scheme+'://'+urlparse(url_dic['url_txt']).netloc
					abs_tmp = prep_chk(upars,tmp)
				finl = list(set(new_tmp.union(abs_tmp)))
				if url_dic['url_txt'] in finl:
					finl.remove(url_dic['url_txt'])
			finl_dct = {}
			finl_lst = []
			for f in finl:
				try:
					article = Article(f)
					article.download()
					article.parse()
					title = str(article.title)
				except:
					title = ''
				finl_lst.append({ 'url' : f, 'title' : title})
			return jsonify(templated_url=url, extracted_urls=finl_lst, error_message='None')
		except Exception as e:
			return jsonify(error_message=str(e)+' ------ 2')