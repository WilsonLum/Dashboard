# Twitter Authenication credential
import pandas as pd
import re
from datetime import datetime
import tweepy
import time
import sys
from collections import Counter
from textblob import TextBlob
import logging
import warnings
import platform

system_type = platform.system()

win_path       = ""
server_path    = "/home/dchrahos/dashboard/twitter/"

if system_type == "Windows":
    dashboard_path = win_path
elif system_type == "Linux":
    dashboard_path = server_path
else:
    print("Platform not supported ... Exiting ...")
    sys.exit(1)

warnings.filterwarnings("ignore")

# Logging information
today = datetime.now()
d = today.strftime("%b-%d-%Y")

logFileName = dashboard_path + 'log/DCHR_Twitter_By_Product.log_' + d + '.log'
logging.basicConfig(filename=logFileName,filemode='a',level=logging.INFO,format='%(asctime)s :: %(levelname)s :: %(message)s')

today = datetime.now()
d = today.strftime("%b-%d-%Y %H:%M:%S")

logging.info("*****************************************************")
logging.info("Scrapping By Product Twitter at " + str(d))
logging.info("*****************************************************")

# Twitter account API credential details
f1 = None
try:
    token_filename= dashboard_path + "input/Twitter_Token.txt"
    print("Reading " + token_filename)
    logging.info("Reading " + token_filename)
    with open(token_filename, 'r') as f:
        token = [line.rstrip('\n') for line in f]

except IOError as e:
    print("I/O error({0}): {1} at ".format(e.errno, e.strerror) + str(d))
    print("Exiting ... \n")
    logging.error("I/O error({0}): {1} at ".format(e.errno, e.strerror) + str(d))
    logging.error("Exiting ... \n")
    sys.exit(1)

finally:
    if f is not None:
        f.close()

consumer_key        = token[0] 
consumer_secret     = token[1]
access_token        = token[2]
access_token_secret = token[3]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.careated_at)

# Read topic list file
today = datetime.now()
d = today.strftime("%b-%d-%Y %H:%M:%S")

lineList = list()
f2 = None
try:
    config_filename = dashboard_path + "input/Twitter By Product.txt"
    print("Reading " + config_filename)
    logging.info("Reading " + config_filename)
    with open(config_filename, 'r') as f2:
        search_query = [line.rstrip('\n') for line in f2]
except IOError as e:
    print("I/O error({0}): {1} at ".format(e.errno, e.strerror) + str(d))
    print("Exiting ... \n")
    logging.error("I/O error({0}): {1} at ".format(e.errno, e.strerror) + str(d))
    logging.error("Exiting ... \n")
    sys.exit(1)

finally:
    if f2 is not None:
        f2.close()
        
maxTweets    = 10000

# Define Functions

# Collect tweets per keyword
# Favorite_count => A tweet that is favorited
#                   The favorite_count provides the number of times the tweet has been favorited. 
#                   In the case of a retweet, favorite_count is the favorite count of the source tweet
# retweet_count  => A Retweet is a re-posting of a Tweet. Twitter's Retweet feature helps you and others quickly share that  
#                   Tweet with all of your followers. You can Retweet your own Tweets or Tweets from someone else. 
#                   Sometimes people type "RT" at the beginning of a Tweet to indicate that they are re-posting 
#                   someone else's content.

def countdown(t, step=1, msg='sleeping'):  # in seconds
    pad_str = ' ' * len('%d' % step)
    for i in range(t, 0, -step):
        print('\r%s for the next %d seconds %s\r' % (msg, i, pad_str),end='\r')
        time.sleep(step)
    print('Done %s for %d seconds! ' % (msg, t))


# Collect tweets per keyword
def collect_tweets(search_query):
    rest         = 900 # if rating error wait for 15 mins - Twitter limit
    my_tweets    = []
    maxTweets    = 10000 # Some arbitrary large number
    tweetsPerQry = 100   # this is the max the API permits
    
    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None
    
    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1
    
    tweetCount = 0
    sentiment = ''
    
    print("Downloading max {0} tweets".format(maxTweets))
    logging.info("Downloading max {0} tweets".format(maxTweets))
    print("Collecting tweets for   :" + str(search_query))
    logging.info("Collecting tweets for   :" + str(search_query))
  
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=search_query, count=tweetsPerQry,lang='en',include_entities=True,tweet_mode='extended')
                else:
                    new_tweets = api.search(q=search_queryy, count=tweetsPerQry,lang='en',since_id=sinceId,
                                            include_entities=True,tweet_mode='extended')
            else:
                if (not sinceId):
                    new_tweets = api.search(q=search_query, count=tweetsPerQry,lang='en',max_id=str(max_id - 1),
                                            include_entities=True,tweet_mode='extended')
                else:
                    new_tweets = api.search(q=search_query, count=tweetsPerQry,lang='en',max_id=str(max_id - 1),
                                            include_entities=True,since_id=sinceId,tweet_mode='extended')
       
            if not new_tweets:
                print("No more tweets found")
                logging.info("No more tweets found")
                break
            
            for tweet in new_tweets:
                my_tweets.append([tweet.created_at, tweet.full_text,tweet.favorite_count,tweet.retweet_count,
                                  tweet.user.url, tweet.user.followers_count,tweet.user.profile_background_image_url,
                                  tweet.user.profile_image_url,tweet.user.screen_name,tweet.entities,search_query,sentiment])
            
            tweetCount += len(new_tweets)
            
            if (tweetCount % 1000==0):
                print("Downloaded {0} tweets".format(tweetCount))
                logging.info("Downloaded {0} tweets".format(tweetCount))
         
            max_id = new_tweets[-1].id
            
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            logging.info("some error : " + str(e))
            print("Sleeping ... for error ... {0}s ...".format(rest))
          
            countdown(rest)
            
            if (tweetCount % 1000==0):
                print("Downloaded {0} tweets".format(tweetCount))
                logging.info("Downloaded {0} tweets".format(tweetCount))

    print ("Downloaded {0} tweets".format(tweetCount))
    logging.info("Downloaded {0} tweets".format(tweetCount))
    
    return my_tweets

# Preprocess the tweets
def pre_process_tweets(my_tweets,search_query):
    processed_tweets = []
    tweets_processed =my_tweets
    print("Preprocessing texts for :" + str(search_query))
    logging.info("Preprocessing texts for :" + str(search_query))
    
    for tweet in range(0, len(my_tweets)):  
    
        # Remove all the http links
        processed_tweet = re.sub(r'http\S+', '', str(my_tweets[tweet][1]))
        
        # Remove all the special characters
        processed_tweet = re.sub(r'\W', ' ', processed_tweet)
 
        # Substituting multiple spaces with single space
        processed_tweet= re.sub(r'\s+', ' ', processed_tweet, flags=re.I)
 
        # Removing prefixed 'b'
        processed_tweet = re.sub(r'^b\s+', '', processed_tweet)
 
        # Converting to Lowercase
        processed_tweet = processed_tweet.lower()
        
        tweets_processed[tweet][1] = processed_tweet
       
    return tweets_processed


def Remove(my_tweets,search_query): 
    
    print("Removing dulpicates texts for :" + str(search_query))
    logging.info("Removing dulpicates texts for :" + str(search_query))

    text = []
    new_list = []
    for tweet in range(0, (len(my_tweets))):  
        if tweet < (len(my_tweets)-1):
            if my_tweets[tweet][1] not in text:
                text.append(my_tweets[tweet][1])
                new_list.append(my_tweets[tweet]) 
            
    return new_list

def GetExpanded_url(tweets):
    tweets_processed =tweets
    
    for i in range(0,len(tweets)):
        if "media" in tweets[i][9]:
            tweets_processed[i][9] = tweets[i][9]['media'][0]['expanded_url']
        else:
            tweets_processed[i][9] = ''

    return tweets_processed

# Add in sentiment analysis using TextBlob per tweet
def get_tweet_sentiment(tweets,search_query):
    print("Getting sentiment for :" + str(search_query))
    logging.info("Getting sentiment for :" + str(search_query))
    ''' 
    Utility function to classify sentiment of passed tweet 
    using textblob's sentiment method 
    '''
    # create TextBlob object of passed tweet text 
    tweets_processed = tweets

    for i in range(0,len(tweets)):
        analysis = TextBlob(tweets[i][1]) 
        # set sentiment 
        if analysis.sentiment.polarity > 0:
            tweets_processed[i][11] = 'Positive'
        elif analysis.sentiment.polarity == 0: 
            tweets_processed[i][11] = 'Neutral'
        else:
            tweets_processed[i][11] = 'Negative'

    return tweets_processed

# Collecting Tweets and Preprocess the data

# List of keywords to collect for tweets
my_tweets_df = [ [0] * maxTweets for _ in range(len(search_query))]
header = ['Date', 'Text','favorite_count', 'retweet_count', 'url', 'followers_count', 'background_image_url',
          'profile_image_url','screen_name', 'entities_url','ticker','sentiment']
all_df = pd.DataFrame()

for i in range (0,len(search_query)):
    my_tweets       = collect_tweets(search_query[i])
    my_tweets_1     = pre_process_tweets(my_tweets,search_query[i])
    my_tweets_2     = Remove(my_tweets_1,search_query[i])
    my_tweets_3     = GetExpanded_url(my_tweets_2)
    my_tweets_4     = get_tweet_sentiment(my_tweets_3,search_query[i])
    
    my_tweets_df[i] = pd.DataFrame(my_tweets_4) 
    
    if not my_tweets_df[i].empty:
        my_tweets_df[i].columns = header
        all_df = pd.concat([all_df,my_tweets_df[i]]) 
        
    print("\n------------------------------------------\n")
    logging.info("\n------------------------------------------\n")

    all_df = pd.DataFrame(all_df)

all_df.columns = header     
print("Done")
logging.info("done\n")

# Display the summary of collections :
tweet_counter = Counter()

for i in range(0,len(my_tweets_df)):
    tweet_counter[search_query[i]] = len(my_tweets_df[i])
    print("Number of tweets for " + search_query[i] + " is " + str(len(my_tweets_df[i])))
    logging.info("Number of tweets for " + search_query[i] + " is " + str(len(my_tweets_df[i])))

tweet_counter.most_common()

# Save the datasets to Excel file
#*******************************************************************************
#                         Save data
#*******************************************************************************

# Month abbreviation, day and year
today = datetime.today()
d = today.strftime("%b-%d-%Y")

# Create a new excel workbook
print("Saving data to DCHR_Twitters_by_product .... ")
logging.info("Saving data to DCHR_Twitters_by_product .... ")

writer1 = pd.ExcelWriter(dashboard_path + 'data/DCHR_Twitters_by_product.xlsx', engine='xlsxwriter')
all_df.to_excel(writer1, sheet_name= 'Products', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer1.save()

end = datetime.now()
d = end.strftime("%b-%d-%Y")

writer2 = pd.ExcelWriter(dashboard_path + 'data/DCHR_Twitters_by_product_' + d + '.xlsx', engine='xlsxwriter')
all_df.to_excel(writer2, sheet_name= 'Products', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer2.save()

end = datetime.now()
e = end.strftime("%b-%d-%Y %H:%M:%S")

print("######################################")
print("  Done saving   " + str(e))
print("######################################\n\n\n")

logging.info("######################################")
logging.info("  Done saving   " + str(e))
logging.info("######################################\n\n\n")
