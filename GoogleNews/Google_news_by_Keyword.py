# Import Library
# General System Util
import sys
import os
from datetime import datetime
# !{sys.executable} -m spacy download en
import re, numpy as np, pandas as pd
from pprint import pprint
import json

# Wordcloud
from wordcloud import WordCloud,ImageColorGenerator ,STOPWORDS
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PIL import Image
import base64


# Gensim
import gensim, spacy, logging, warnings
import gensim.corpora as corpora
from gensim.utils import lemmatize, simple_preprocess
from gensim.models import CoherenceModel
import matplotlib.pyplot as plt
#import pyLDAvis.gensim

# NLTK Stop words
import nltk
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords

# Vectoriser
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
from datetime import datetime


today = datetime.now()
d = today.strftime("%b-%d-%Y")

# Logging information
logFileName = 'log\DCHR_Google_new_by_Keyword_' + d + '.log'
logging.basicConfig(filename=logFileName,filemode='a',level=logging.INFO,format='%(asctime)s :: %(levelname)s :: %(message)s')
current_path = os.getcwd()

today = datetime.now()
d = today.strftime("%b-%d-%Y %H:%M:%S")

logging.info("**********************************************************************")
logging.info("Creating Google RSS News dataset by Keyword at " + str(d))
logging.info("**********************************************************************\n")

gensim_logger = logging.getLogger('gensim')
gensim_logger.setLevel(logging.CRITICAL)

#%matplotlib inline
#warnings.filterwarnings("ignore",category=DeprecationWarning)
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

#---------------------------------------------------------
# Variable definitions
nltk.download('stopwords')
stopword_filename = "input\stopwords.txt"
with open(stopword_filename, 'r') as f:
    mystopwords = [line.rstrip('\n') for line in f]
stopword = stopwords.words("English")
stopword.extend(mystopwords)

corpus = []
data = []
df = []

#---------------------------------------------------------
## Read config file for Keyword
lineList = list()
config_filename = "input\Google_search_Keyword.txt"
print("Reading " + config_filename)
logging.info("Reading " + config_filename)
lineList = [line.rstrip('\n') for line in open(config_filename)]

#---------------------------------------------------------
# Function Definition

# reading in the json topic files
def read_file(topic,i):
	print("\n---------------------------------------------------\n")
	json_filename =  "data\\Keyword\\" + topic + ".json"
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

# Display wordcloud and save as jpg
def WordCloud_Display(count_vectorizer,count_data,name):

    count_vectorizer.vocabulary_
    sum_words = count_data.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in count_vectorizer.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    
    #Generating wordcloud and saving as jpg image
    words_dict = dict(words_freq)
    WC_height = 240
    WC_width = 360
    WC_max_words = 80
    wordCloud = WordCloud(max_words=WC_max_words, height=WC_height, width=WC_width,stopwords=mystopwords)
    wordCloud.generate_from_frequencies(words_dict)

    #plt.figure(figsize=(20,10))
    #plt.title('Most frequently occurring ' + name + ' connected by same colour and font size')
    #plt.imshow(wordCloud, interpolation='bilinear')
    #plt.axis("off")
    #plt.show()
    filename = 'diagram\WordCloud_' + name + '.jpg'
    wordCloud.to_file(filename)
    logging.info(filename)
    return filename

# Tokenize Sentences and Clean
def sent_to_words(sentences):
    for sent in sentences:
        sent = re.sub('\S*@\S*\s?', '', sent)  # remove emails
        sent = re.sub('\s+', ' ', sent)  # remove newline chars
        sent = re.sub("\'", "", sent)  # remove single quotes
        sent = gensim.utils.simple_preprocess(str(sent), deacc=True) 
        yield(sent)  

# !python3 -m spacy download en  # run in terminal once
# or do
# !conda install -c conda-forge spacy-model-en_core_web_md 
# and use nlp=spacy.load('en_core_web_sm') instead in below function.
def process_words(texts, stop_words=stopword, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
   
    """Remove Stopwords, Form Bigrams, Trigrams and Lemmatization"""
    texts = [[word for word in simple_preprocess(str(doc)) if word not in stopword] for doc in texts]
    texts = [bigram_mod[doc] for doc in texts]
    texts = [trigram_mod[bigram_mod[doc]] for doc in texts]
    texts_out = []
    nlp=spacy.load('en_core_web_lg')
   
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    # remove stopwords once more after lemmatization
    texts_out = [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts_out]    
    return texts_out

def format_topics_sentences(ldamodel=None, corpus=corpus, texts=data,df=df):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row_list in enumerate(ldamodel[corpus]):
        row = row_list[0] if ldamodel.per_word_topics else row_list            
        # print(row)
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
 
    sent_topics_df = pd.concat([sent_topics_df, contents,df], axis=1)
    return(sent_topics_df)

def topics_per_document(model, corpus, start=0, end=1):
    corpus_sel = corpus[start:end]
    dominant_topics = []
    topic_percentages = []
    for i, corp in enumerate(corpus_sel):
        topic_percs, wordid_topics, wordid_phivalues = model[corp]
        dominant_topic = sorted(topic_percs, key = lambda x: x[1], reverse=True)[0][0]
        dominant_topics.append((i, dominant_topic))
        topic_percentages.append(topic_percs)
    return(dominant_topics, topic_percentages)


def ConvertImagetoBase64(ImageFileName):

	with open(ImageFileName, "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read())

	base64_image_code = b"".join([b'data:image/jpeg;base64, ', encoded_string])

	return base64_image_code


#**********************************************************
# Start of the main program
#**********************************************************

all_df = pd.DataFrame()
all_diagram_df = pd.DataFrame()

for i in range (0,len(lineList)):
	df = pd.DataFrame()
	diagram_df = pd.DataFrame()
	topic = lineList[i]
	df = read_file(lineList[i],i)

	if df.empty == True: # Error reading file
		continue

	df_new = pre_process_text(df)
	df["new"] = df_new
	df['topic'] = str(lineList[i])

	# ------------------------------------------------------
	# Vectoriser
	# ------------------------------------------------------
	# Bigram
	# Initialise the count vectorizer with the English stop words
	print("Vectorising Bigram for " + topic)
	count_vectorizer_Bigram = CountVectorizer(stop_words='english', ngram_range=(2,2))
	# Fit and transform the processed titles
	count_data_bi   = count_vectorizer_Bigram.fit_transform(df.new)
	Bigram_fileName = WordCloud_Display(count_vectorizer_Bigram,count_data_bi,"DCHR_Bigram_"+topic)
	Bigram_base64   = ConvertImagetoBase64(Bigram_fileName)

	# Trigram
	# Initialise the count vectorizer with the English stop words
	print("Vectorising Trigram for " + topic)
	count_vectorizer_Trigram = CountVectorizer(stop_words='english', ngram_range=(3,3))
	# Fit and transform the processed titles
	count_data_tri = count_vectorizer_Trigram.fit_transform(df.new)
	Trigram_fileName = WordCloud_Display(count_vectorizer_Trigram,count_data_tri,"DCHR_Trigram_"+topic)
	Trigram_base64   = ConvertImagetoBase64(Trigram_fileName)

	diagram_df = diagram_df.append({'topic' : topic, 
		                            'bigram': Bigram_base64,
		                            'trigram': Trigram_base64},
		                            ignore_index=True)

	# ------------------------------------------------------
	# Removing the emails, new line characters, single quotes and finally split the sentence into a list of words
	# using gensim’s simple_preprocess(). Setting the deacc=True option removes punctuations.
	# ------------------------------------------------------
	# Convert to List
	data = df.new.values.tolist()
	data_words = list(sent_to_words(data))

	# ------------------------------------------------------
	# Build the Bigram, Trigram Models and Lemmatize
	# Let’s form the bigram and trigrams using the Phrases model. 
	# This is passed to Phraser() for efficiency in speed of execution.
	# Next, lemmatize each word to its root form, keeping only nouns, adjectives, verbs and adverbs.
	# We keep only these POS tags because they are the ones contributing the most to the meaning of the sentences. 
	# Here, we use spacy for lemmatization.
	# ------------------------------------------------------

	# Build the bigram and trigram models
	print("Building Bigram & Trigram models for " + topic)
	bigram      = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
	trigram     = gensim.models.Phrases(bigram[data_words], threshold=100) 
	bigram_mod  = gensim.models.phrases.Phraser(bigram)
	trigram_mod = gensim.models.phrases.Phraser(trigram)

	data_ready  = process_words(data_words)  # processed Text Data!

	# ------------------------------------------------------
	# To build the LDA topic model using LdaModel(), we need the corpus and the dictionary. 
	# The trained topics (keywords and weights) are printed below as well.
	# ------------------------------------------------------

	# Create Dictionary
	id2word = corpora.Dictionary(data_ready)

	# Create Corpus: Term Document Frequency
	corpus = [id2word.doc2bow(text) for text in data_ready]

	# Build LDA model
	lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,id2word=id2word,num_topics=3, random_state=100,
		                                        update_every=1,chunksize=10,passes=10,alpha='symmetric',
		                                        iterations=100,per_word_topics=True)

	# ------------------------------------------------------
	# Dominant topic and its percentage contribution in each document
	# ------------------------------------------------------

	df_topic_sents_keywords = format_topics_sentences(ldamodel=lda_model, corpus=corpus, texts=data_ready, df=df)

	# Format
	df_dominant_topic = df_topic_sents_keywords.reset_index()
	df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 
	                             'Text','item','link','description','body','pubdate','new','topic']

	all_df = all_df.append(df_dominant_topic)
	all_diagram_df = all_diagram_df.append(diagram_df)


#*******************************************************************************
#                         Save topic data
#*******************************************************************************


# Create a new excel workbook
writer1 = pd.ExcelWriter('data\DCHR_Google_Keyword.xlsx', engine='xlsxwriter')
all_df.to_excel(writer1, sheet_name='Topics', index=False)
all_diagram_df.to_excel(writer1, sheet_name='Image', index=False)


# Close the Pandas Excel writer and output the Excel file.
writer1.save()

today = datetime.now()
d = today.strftime("%b-%d-%Y")

# Create a new excel workbook
writer2 = pd.ExcelWriter('data\DCHR_Google_Keyword_' + d + '.xlsx', engine='xlsxwriter')
all_df.to_excel(writer2, sheet_name='Topics', index=False)
all_diagram_df.to_excel(writer2, sheet_name='Image', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer2.save()


print("Saving All topics to excel")
print("---------------------------------------------------\n")
logging.info("Saving All topics to excel")

print("Saving All topics image file path to excel")
print("---------------------------------------------------\n")
logging.info("Saving All topics image file path to excel")

end = datetime.now()
e = end.strftime("%b-%d-%Y %H:%M:%S")

print("######################################")
print("  Done saving   " + str(e))
print("######################################\n\n\n")

logging.info("######################################")
logging.info("  Done saving   " + str(e))
logging.info("######################################\n\n\n")







