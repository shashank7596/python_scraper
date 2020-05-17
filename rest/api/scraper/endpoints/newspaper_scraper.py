from flask import request, jsonify
from flask_restplus import Resource, reqparse
from rest.api.restplus import api
from rest.api.scraper.required_parameters import article_params
from newspaper import fulltext
from newspaper import Article
import logging, urllib, cloudscraper, re
from bs4 import BeautifulSoup
import requests
import html2text


# Creating html2text object and setting up configs.
h = html2text.HTML2Text()

h.ignore_links = True
h.ignore_images = True
h.unicode_snob = True



# Creating scraper object
scraper = cloudscraper.create_scraper()

# Creating request parser object
request_parser = reqparse.RequestParser()
request_parser.add_argument('URL', type=str, default=None, help='Enter URL need to be scraped.')

# Creating logging object
log = logging.getLogger(__name__)

# Defining namespace for article scraper.
ns = api.namespace('scraper/articlescraper', description='ArticleScraper')


def extract_title(ht, lang='en'):
    """ Extracts title from url using regex matching. If nothing found returns NONE."""
    try:
        article = Article(ht, language=lang)
        article.download()
        article.parse()
        return str(article.title)
    except Exception as exx:
        return 'None'


def extract_content_article(ht, lang='en'):
    """ This method uses regular article scraping instead of the fulltext present in newspaper. Parses out the content."""
    article = Article(ht, language=lang)
    article.download()
    article.parse()
    cntnt = str(article.text)
    return cntnt


def cloudscrape(ur):
    html_txt = scraper.get(ur)
    return html_txt


def req(ur):
    return requests.get(ur).text


def content_cleaner(cont):
    cont = str(cont).replace('\r','').replace('\t','')
    cont = re.sub(r'\n\n+', '\n', cont) # cont = re.sub(r'\s\s+', '', cont)
    return cont


# Routing webservice
@ns.route('/')
class ArticleScraper(Resource):
    # Expecting an input URL to be scraped
    @api.expect(request_parser)
    def get(self):
        """ Parses given URL and scrape content out of it. """
        args = request_parser.parse_args(request)
        url = args.get('URL')
        title = extract_title(url)
        try:
            content = extract_content_article(url)
            content = content_cleaner(content)
            if len(str(content)) <= 1000:
                content = cloudscrape(url)
                try:
                    content = h.handle(content)
                    content = content_cleaner(content)
                    return jsonify(url=url, title=title, content=content, error_message='None')
                except AttributeError:
                    content = h.handle(content.text)
                    content = content_cleaner(content.text)
                    return jsonify(url=url, title=title, content=content, error_message='None')
                except:
                    raise Exception('Cannot convert cloudscraper content to text')
            else:
                return jsonify(url=url, title=title, content=content, error_message='None')
        except:
            try:
                content = cloudscrape(url)
                try:
                    content = h.handle(content)
                except AttributeError:
                    content = h.handle(content.text)
                except:
                    raise Exception('Cannot convert cloudscraper content to text')
                content = content_cleaner(content)
                return jsonify(url=url, title=title, content=content, error_message='None')
            except Exception as e:
                return jsonify(url=url, title='None', content='None', error_message=str(e))