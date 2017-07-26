from string import punctuation
from string import maketrans
import re, string
import unicodedata
import twitter


OAUTH_TOKEN =  "enter your token" 
OAUTH_TOKEN_SECRET = "enter your token secret"
CONSUMER_KEY = "enter your consumer key"
CONSUMER_SECRET = "enter your consumer secret"

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)


def process_tweets(target):

	""" 
	takes string as an input and uses it as a search term for 
	tweets. returns an array of cleaned tweets.
	"""

	search_results = twitter_api.search.tweets(q=target, count=100) 
	statuses = search_results['statuses']

	extracted_tweets = [status['text'] for status in statuses]

	
	def format_tweet(string_):
		''' remove emoji,links and non-ascii '''
		tweets = unicodedata.normalize('NFKD', string_).encode('ascii','ignore') 

		remove_punctuation = lambda s: s.translate(string.maketrans("",""), string.punctuation)
		tweet_text = remove_punctuation(tweets)

		tweet_text_list = tweet_text.split()
		no_links = 'http'
		regex_ = re.compile(".*(%s).*" % no_links)
		search_ = [m.group(0) for l in tweet_text_list for m in [regex_.search(l)] if m]
		clean_tweet = [word for word in tweet_text_list if word not in search_]
		
		return ' '.join(clean_tweet)


	return [format_tweet(tweet) for tweet in extracted_tweets]



