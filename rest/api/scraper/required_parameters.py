## Add all the required parameters necessary for all end points and can be imported as necessary

# Specify all article/newspaper related parameters.
article_params = {\
					'title_pattern' : '(?<=<title>).+?(?=</title>)'\
				}

# Specify all rss parser related parameters.
rss_params = {\
				'feed_parser_fields' : ['link','title','summary','published','author']\
			}

# Specify all google search related parameters.
google_params = {\
					'default_tbs_lookback' : 'qdr:d',\
					'tbs_look_back' : ['hour','day', 'week', 'month', 'year'],\
					'start' : 0,\
					'stop' : 10,\
					'exclusion' : ['wikipedia','amazon','wiki','wikivoyage','youtube','facebook','instagram','ebay','aliexpress','craigslist']\
				}