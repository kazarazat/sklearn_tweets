from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from get_tweets import process_tweets # expects two strings as tweet subjects

def analyze_sentiment(element):
	
	"""
	takes a text string and processes
	the sentiment of each string in the array.
	returns a score enum from lowest to highest
	and 1 - 20 in between. 0 is neutral
	"""

	data = element

	def process(string_):
			vader_A  = SentimentIntensityAnalyzer()
			vs = vader_A.polarity_scores(string_)
			return vs['compound']

	def enumerate(sent_float):

		"""
		takes a sentiment score float
		checks it through a range of scores
		returns a integer that represents where
		the score fell in the range of (1-20) labels
		"""

		sentiment = [round(sent_float,3)]

		poles = (-.999,-.899,-.799,-.699,-.599,-.499,-.399,-.299,
				 -.199,-.099,0.00,.099,.199,.299,.399,.499,.599,
				 .699,.799,.899,.999,1.000)

		intervals = [(poles[i],poles[i+1]) for i in range(len(poles)-1)]

		scores = [list() for _ in range(len(intervals))]

		for out,(start,stop) in zip(scores,intervals):
		    for s in sentiment:
		        if start <= s < stop:
		            out.append(s)

		return [scores.index(item) for item in scores if len(item) != 0][0]


	def get_scores():
		raw_scores = [process(review) for review in data] 
		enumarated_scores = [enumerate(score) for score in raw_scores]
		return enumarated_scores


	return [enumerate(process(item)) for item in data]






