import os
# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/uday/Ontologies/twitter-sentiment-analysis/twitterstreamer/TwitterStreamer/gcp_nlp_key.json'

# Instantiates a client
client = language.LanguageServiceClient()

def sentiment_score(text):
	# The text to analyze
	print text
	document = types.Document(
		content=text,
		type=enums.Document.Type.PLAIN_TEXT
	)
	# Detects the sentiment of the text
	try:
		sentiment = client.analyze_sentiment(document=document).document_sentiment
		# print "\n",'Text: {}'.format(text)
		print 'Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude),"\n"
		return sentiment.score
	except Exception as e:
		print str(e)
		return 0
