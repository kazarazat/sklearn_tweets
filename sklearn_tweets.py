# grammar
from nltk.corpus import stopwords

# machine learn
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import cross_val_score, KFold
from sklearn.metrics import classification_report

# math
import numpy as np
from scipy.stats import sem

# local
from get_tweets import process_tweets
from get_sentiment import analyze_sentiment

labels = ['lowest','1','2','3','4','5','6','7','8','9',
				'neutral','11','12','13','14','15','16','17','18','19'
				'highest']

def aggregate_tweets(*args):
	tweets = []
	for arg in args:
		tweets.append(process_tweets(arg))
	flatten_tweets = [item for sublist in tweets for item in sublist]
	return flatten_tweets

# get your tweets for whatever keywords you like 
tweets = aggregate_tweets('GameOfThrones','JonSnow','WhiteWalkers')

# analyze those tweets
scores = analyze_sentiment(tweets)


def preproc_data():
	SPLIT_PERC = 0.90
	split_size = int(len(tweets)*SPLIT_PERC)
	a = tweets[:split_size]
	b = tweets[split_size:]
	c = scores[:split_size]
	d = scores[split_size:]
	return a,b,c,d

X_train,X_test,y_train,y_test = preproc_data()

def eval_cross_val(clf_, X, y, K):
	cv = KFold(len(y), K, shuffle=True, random_state=0)
	scores = cross_val_score(clf_, X, y, cv=cv)
	print ("Mean score: {0:.3f} (+/-{1:.3f})") .format (np.mean(scores), sem(scores))

pipeline = Pipeline([
	('vect', TfidfVectorizer(
				set(stopwords.words('english')),
				token_pattern=ur"\b[a-z0-9_\-\.]+[a-z][a-z0-9_\-\.]+\b",
				)),
				('clf', MultinomialNB(alpha=0.1)),
			])

eval_cross_val(pipeline, X_train, y_train, 10)

pipeline.fit(X_train, y_train)
y = pipeline.predict(X_test)

def get_report():
	return (classification_report(y, y_test, target_names=labels))

print get_report()



