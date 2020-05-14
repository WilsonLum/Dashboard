import subprocess
import schedule
import time
from datetime import datetime
import logging

logFileName = 'schedule_process.log'
logging.basicConfig(filename=logFileName,filemode='a',level=logging.INFO,format='%(asctime)s :: %(levelname)s :: %(message)s')

# This min requires 3-5 min of scrapping depends on the number of keywords
# It can take more than 10 mins if it hits the max request set by twitter which will sleep for 900seconds before continue to scrape
# Min give this job about 20 mins
def twitter_by_topic_scrap():
    print('Twitter by topic:', datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    logging.info('Twitter by topic:')
    subprocess.call(r'C:\dashboard\twitter\Twitter_by_topic_Scrape.bat')

# This min requires 3-5 min of scrapping depends on the number of keywords
# It can take more than 10 mins if it hits the max request set by twitter which will sleep for 900seconds before continue to scrape
# Min give this job about 20 mins
def twitter_by_screen_name_scrap():
    print('Twitter by screen name:', datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    logging.info('Twitter by screen name:')
    subprocess.call(r'C:\dashboard\twitter\Twitter_by_screen_name_Scrape.bat')

# This min requires 60 min of scrapping depends on the number of keywords
# It can take more than 40 mins Min give this job about 50 mins
def GoogleNews_by_Category_scrap():
    print('Google scrap by Category:', datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    logging.info('Google scrap by Category:')
    subprocess.call(r'C:\dashboard\GoogleNews\GoogleRSS_Scrape_Category.bat')

# This min requires 60 min of scrapping depends on the number of keywords
# It can take more than 40 mins Min give this job about 50 mins
def GoogleNews_by_Keyword_scrap():
    print('Google scrap by Keyword:', datetime.now().strftime("%b-%d-%Y %H:%M:%S"))  
    logging.info('Google scrap by Keyword:')  
    subprocess.call(r'C:\dashboard\GoogleNews\GoogleRSS_Scrape_Keyword.bat')

# This min requires 60 min of scrapping depends on the number of keywords
# It can take more than 40 mins Min give this job about 50 mins
def GoogleNews_by_Product_scrap():
    print('Google scrap by Product:', datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    logging.info('Google scrap by Product:')
    subprocess.call(r'C:\dashboard\GoogleNews\GoogleRSS_Scrape_Product.bat')

# This min requires 60 min of scrapping depends on the number of keywords
# It can take more than 40 mins Min give this job about 50 mins
def Create_GoogleNews_Datasets_Category():
    print('Google Dataset by Category:', datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    logging.info('Google Dataset by Category:')
    subprocess.call(r'C:\dashboard\GoogleNews\Create_Google_news_dataset_by_Category.bat')

# This min requires 60 min of scrapping depends on the number of keywords
# It can take more than 40 mins Min give this job about 50 mins
def Create_GoogleNews_Datasets_Keyword():
    print("Google Dataset by Keyword:", datetime.now().strftime("%b-%d-%Y %H:%M:%S")) 
    logging.info('Google Dataset by Keyword:') 
    subprocess.call(r'C:\dashboard\GoogleNews\Create_Google_news_dataset_by_Keyword.bat')

# This min requires 60 min of scrapping depends on the number of keywords
# It can take more than 40 mins Min give this job about 50 mins
def Create_GoogleNews_Datasets_Product():
    print('Google Dataset by Product:', datetime.now().strftime("%b-%d-%Y %H:%M:%S")) 
    logging.info("Google Dataset by Product:") 
    subprocess.call(r'C:\dashboard\GoogleNews\Create_Google_news_dataset_by_Product.bat')
    print('End:', datetime.now().strftime("%b-%d-%Y %H:%M:%S")) 
    logging.info("End:") 

def RunTaskPeriodically():
    try:
        # Start of the twitter scrapping jobs
        schedule.every().day.at('10:46').do(twitter_by_topic_scrap)
        schedule.every().day.at('11:00').do(twitter_by_screen_name_scrap)

        # Start of the Google scrapping jobs
        schedule.every().day.at('11:20').do(GoogleNews_by_Category_scrap)
        schedule.every().day.at('12:20').do(GoogleNews_by_Keyword_scrap)
        schedule.every().day.at('13:00').do(GoogleNews_by_Product_scrap)

        # Start of the Creating of Google dataset jobs
        schedule.every().day.at('14:15').do(Create_GoogleNews_Datasets_Category)
        schedule.every().day.at('15:00').do(Create_GoogleNews_Datasets_Keyword)
        schedule.every().day.at('15:30').do(Create_GoogleNews_Datasets_Product)
        
        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        print("RunTaskPeriodically: "+str(e)+"\n") 

print('START:', datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
logging.info("Start:")
RunTaskPeriodically()
