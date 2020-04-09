# Import Library
# General System Util
import sys
import os
from datetime import datetime
# !{sys.executable} -m spacy download en
import re, numpy as np, pandas as pd
import json

# NLTK Stop words
import nltk
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords

# Vectoriser
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
import pyLDAvis
from pyLDAvis import sklearn as sklearn_lda
import pickle 

import logging
import warnings

warnings.filterwarnings("ignore")

# Variables definitions
default_min_topic = 3
default_max_topic = 5
corpus = []
data = []
df = []

# Logging information
today = datetime.now()
d = today.strftime("%b-%d-%Y")

logFileName = 'log\DCHR_Google_Number_of_topics' + d + '.log'
logging.basicConfig(filename=logFileName,filemode='a',level=logging.INFO,format='%(asctime)s :: %(levelname)s :: %(message)s')

today = datetime.now()
d = today.strftime("%b-%d-%Y %H:%M:%S")

logging.info("***********************************************************")
logging.info("Testing on Google RSS News Number of Topics " + str(d))
logging.info("***********************************************************\n")


#---------------------------------------------------------
# Reading files
#---------------------------------------------------------

# Read in customised stopwords
try:
	stopword_filename = "input\\stopwords.txt"
	with open(stopword_filename, 'r') as f1:
		mystopwords = [line.rstrip('\n') for line in f1]
	stopword = stopwords.words("English")
	stopword.extend(mystopwords)
except IOError as e:
	print("I/O error({0}): {1} at ".format(e.errno, e.strerror) + str(d))
	print("Will be using the default stopwords ... \n")
	logging.error("I/O error({0}): {1} at ".format(e.errno, e.strerror) + str(d))
	logging.error("Will be using the default stopwords ... \n")
	stopword = stopwords.words("English")

# Read in number of topics desired
try:
	topic_filename = "input\\number_of_topics.txt"
	with open(topic_filename, 'r') as f2:
		topic_no = [line.rstrip('\n') for line in f2]
	min_topic = int(topic_no[0])
	max_topic = int(topic_no[1])
except IOError as e:
	print("I/O error({0}): {1} at ".format(e.errno, e.strerror) + str(d))
	print("Will be using the default 3 to 8 number of topics ... \n")
	logging.error("I/O error({0}): {1} at ".format(e.errno, e.strerror) + str(d))
	logging.error("Will be using the default 3 to 8 number of topics ... \n")
	min_topic = default_min_topic
	max_topic = default_max_topic

lineList = list()

# Read in number of topics desired
try:
	config_filename = "input\Google_search_Keyword.txt"
	print("Reading " + config_filename)
	logging.info("Reading " + config_filename)
	with open(config_filename, 'r') as f3:
		lineList = [line.rstrip('\n') for line in f3]
except IOError as e:
	print("I/O error({0}): {1} at ".format(e.errno, e.strerror) + str(d))
	print("Exiting ... \n")
	logging.error("I/O error({0}): {1} at ".format(e.errno, e.strerror) + str(d))
	logging.error("Exiting ... \n")
	sys.exit(1)


#---------------------------------------------------------
# Function Definition
#---------------------------------------------------------

# reading in the json topic files
def read_file(topic,i):
	print("---------------------------------------------------")
	json_filename =  "data\\" + topic + ".json"
	df = pd.DataFrame()
	print("Reading " + json_filename)
	try:
		with open(json_filename) as json_file:
			data = json.load(json_file)

		df = pd.DataFrame(data)
		df = df[["item","link","description","body","pubdate"]]

	except Exception as e:
		today = datetime.now()
		error_time = today.strftime("%b-%d-%Y %H:%M:%S")
		print("Unable to read at row " + str(i+1) + " of " + config_filename + " Error %s" % (e) + " at " + str(error_time))
		logging.info("Unable to read at row " + str(i+1) + " of " + config_filename + " Error %s" % (e) + " at " + str(error_time))

	return df

# Preprocess the tweets
def processing_parts(text, stopword):
    text = re.sub(r'\[.*?\]', '', text)           # Remove all [*]
    text = re.sub(r'http\S+', '', text)           # Remove all the http links
    text = text.lower()
    text = re.sub(r'\W', ' ', text)               # Remove all the special characters
    text = re.sub(r'\s+', ' ', text, flags=re.I)  # Substituting multiple spaces with single space
    text = re.sub(" \d+", " ", text)              # Remove all the digits
    text = text.replace("_", "")
    text = text.replace("0", "")
    tokens = nltk.word_tokenize(text)
    tokens = [ t for t in tokens if t not in stopword]
    text_after_stopwords =" ".join(tokens)
    
    return text_after_stopwords
     
def pre_process_text(text):
    
    print ("Preprocessing texts ... ")
    
    text_processed = [processing_parts(i, stopword) for i in text.body]
               
    return text_processed

# Helper function
def print_topics(model, count_vectorizer, n_top_words):
    words = count_vectorizer.get_feature_names()
    for topic_idx, topic in enumerate(model.components_):
        print("\nTopic #%d:" % topic_idx)
        print(" ".join([words[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))

#**********************************************************
# Start of the main program
#**********************************************************

all_df = pd.DataFrame()

# read in all topics
for i in range (0,len(lineList)):
	df = pd.DataFrame()
	topic = lineList[i]
	df = read_file(lineList[i],i)

	if df.empty == True: # Error reading file
		continue

	df_new = pre_process_text(df)
	df["new"] = df_new
	df['topic'] = str(lineList[i])

	all_df = all_df.append(df)


# ------------------------------------------------------
# Vectoriser
# ------------------------------------------------------

for topic in range(min_topic,max_topic+1):

	# Bigram
	# Initialise the count vectorizer with the English stop words
	print("---------------------------------------------------\n")
	print("Vectorising Bi_tri_gram for number of topics " + str(topic))
	logging.info("Vectorising Bi_tri_gram for number of topics " + str(topic))
	count_vectorizer_Bigram = CountVectorizer(stop_words='english', ngram_range=(3,3))
	# Fit and transform the processed titles
	count_data_bi = count_vectorizer_Bigram.fit_transform(all_df.new)

	# ------------------------------------------------------
	# Build the bigram and trigram LDA models
	# ------------------------------------------------------
	print("Building Bi_tri_gram LDA models for number of topics " + str(topic))
	print("Will take quite a while ...")
	logging.info("Building Bi_tri_gram LDA models for number of topics " + str(topic))
	logging.info("Will take quite a while ... estimted 2.5 hours per topic ...")
	lda_bi = LDA(n_components=topic, n_jobs=-1)
	lda_bi.fit(count_data_bi)

	# this is a bit time consuming
	LDAvis_prepared_bi        = sklearn_lda.prepare(lda_bi,count_data_bi, count_vectorizer_Bigram)

	# Save LDAvis and output of Topics
	save = datetime.now()
	e = save.strftime("%b-%d-%Y %H:%M:%S")
	print("Saving to HTML format ... at " + str(save) + "\n")
	print("************************************************************************\n")
	logging.info("Saving to HTML format ... at " + str(save) + "\n")
	logging.info("************************************************************************\n")

	pyLDAvis.save_html(LDAvis_prepared_bi, 'topic/GoogleNews_topic_no_' + str(topic) + '.html')


end = datetime.now()
e = end.strftime("%b-%d-%Y %H:%M:%S")

print("######################################")
print("  Done saving   " + str(e))
print("######################################\n\n\n")

logging.info("######################################")
logging.info("  Done saving   " + str(e))
logging.info("######################################\n\n\n")







