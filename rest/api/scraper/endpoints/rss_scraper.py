from flask import request, jsonify
from flask_restplus import Resource, reqparse
from rest.api.restplus import api
from newspaper import fulltext
import logging, urllib, cloudscraper, feedparser, requests, html2text
from rest.api.scraper.required_parameters import rss_params
from rest.api.scraper.parser import  request_parser
import json
from bs4 import BeautifulSoup

#Creating scraper object
scraper = cloudscraper.create_scraper()

#Creating html2text object and setting property ignore_images from that provided html content. 
h = html2text.HTML2Text()
h.ignore_images = True

# Defining logging object
log = logging.getLogger(__name__)

# Defining request parser object for getting input url from user.
request_parser = reqparse.RequestParser()
request_parser.add_argument('RSS_FEED', type=str, default=None, help='Enter the RSS_FEED need to be parsed')

ns = api.namespace('scraper/rss_scraper', description='RSS Scraper')

@ns.route('/')
class RssScraper(Resource):

    @api.expect(request_parser)
    def get(self):
        """ Parses given RSS/XML, extracts URL's present in the feed and their respective link,title,summary,published,author. """
        args = request_parser.parse_args(request)
        url = args.get("RSS_FEED")
        urls_to_parse = []

        # Add the required fields need to be extracted from the parser.entries. It will be handled automatically.
        required_fields = rss_params['feed_parser_fields']
        try:
            # Get the response from the provided url
            response = scraper.get(url)           
        except Exception as e:           
            return jsonify(rss_feed = url, extracted_urls = [{}], error_message = 'Response not found. Double check the url of website specified.')

        def myparse(**kwargs):
            """  This function parses a feed from XML string or URL based on argument sent and returns 'FeedParserDict'. """
            if kwargs['typ'] == 'response' and isinstance(kwargs['rep'],requests.models.Response) == True:
                return feedparser.parse(kwargs['rep'].text)
            elif kwargs['typ'] == 'url' and isinstance(kwargs['rep'],str) == True:
                return feedparser.parse(kwargs['rep'])
            else:
                return jsonify(rss_feed = url, extracted_urls = [{}], error_message = 'Response/URL mismatch with type provided in myparse function as argument.')

        try:
            parser = myparse(rep = response,typ = 'response')

            #Checking if the returned response from myparse() is a html content. Ignoring if so because feed parser can't parse HTML content.
            if 'html' in parser.feed.keys():
                 return jsonify(rss_feed = url, extracted_urls = [{}], error_message = 'Seems like URL is not an XML/RSS. It might be a HTML')

            if len(parser.entries) <= 0 and len(parser.feed) <= 0:
                try:
                    parser = myparse(rep = url,typ = 'url')
                except Exception as e:
                    return jsonify(rss_feed = url, extracted_urls = [{}], error_message = str(e))

            if len(parser.entries) > 0:
                for i in range(0,len(parser.entries)):
                    js = {} #Returns a json for each iteration and collected into a list of json.
                    try:
                        for fld in required_fields:
                            try:
                                js.update({fld : parser.entries[i][fld]})
                            except:
                                js.update({fld : ''})
                                pass
                        # Renaming published to pubdate as required. This pop will rename if published exists to pubdate else it will create pubdate with empty string as specified.
                        js['pubdate'] = js.pop('published')

                        #Checking if the extracted summary is a html or not. If True then convert that html to text and remove all newline characters else ignore. 
                        if bool(BeautifulSoup(js['summary'],'html.parser').find()):
                            js['summary'] = h.handle(js['summary']).replace('\n','')
                        urls_to_parse.append(js)
                    except:
                        pass
            else:
                if 'link' in parser.feed.keys() and len(parser.feed.link) > 0:
                    urls_to_parse.append(parser.feed.link)
                else:               
                    return jsonify(rss_feed = url, extracted_urls = [{}], error_message = 'Cannot parse given URL, it might not be a valid RSS')        
            return jsonify(rss_feed = url, extracted_urls = urls_to_parse, error_message = 'None')
        except Exception as excp:
            return jsonify(rss_feed = url, extracted_urls = [{}], error_message = str(excp))
