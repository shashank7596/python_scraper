# Scraper

### Description:

This Scraper has the following functionality:

- **RSS scraping :** _Enables user to extract URL's present in the RSS feed. This URl's can be again used to scrape the individual content. It returns json response which contains title, published date, summary, url link for each extracted url and it's feed url._

- **Article Scraping :** _Enables user to scrape the content of the URL provided as input. It returns a json response which contains article title, content and it's url._

- **Google Search :** _Enables user to search any given search string(which follows search operators in https://ahrefs.com/blog/google-advanced-search-operators/ for reference). Based on that search query it search and return some search results of which few are ignored. User can specify that list of domains which should be ignored and number of results to be appeared._

- **PointTag Scraping :** _Enables user to scrape particular tag in the html page. For few of HTML pages Article Scraping doesn't work, in those instances this PointTag scraping comes in picture. Especially for the html pages which is like newsrooms of any website. This gives json response same as RSS feed._


### Envrironment Requirements:

#### Windows:

Set up the environment variable if not exists
```
export PYTHONPATH=/path/to/parent:$PYTHONPATH
```


Run below commands only if you want to run in virtual env otherwise
```
python -m virtualenv venv
source venv/Scripts/activate
```


Installs all the required python packages
```
pip3 install -r requirements.txt
```

Setup the API and required configurations to run web service. develop is the environment name passed as argument to the api to setup the required api environment
```
python setup.py develop
```

Run/Start the server using below command:
```
python rest/app.py
```

#### Linux:

```
export PYTHONPATH=/path/to/parent:$PYTHONPATH   
```

Run below venv commands only if you want to run in virtual environment otherwise ignore
```
virtualenv -p python venv
source venv/bin/activate
```

```
pip3 install -r requirements.txt
python setup.py develop
python rest/app.py
```
