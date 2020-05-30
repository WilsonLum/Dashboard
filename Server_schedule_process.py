import subprocess
import schedule
import time
from datetime import datetime
import logging

logFileName = '/home/dchrahos/dashboard/log/schedule_process.log'
logging.basicConfig(filename=logFileName,filemode='a',level=logging.INFO,format='%(asctime)s :: %(levelname)s :: %(message)s')

# This min requires 3-5 min of scrapping depends on the number of keywords
# It can take more than 10 mins if it hits the max request set by twitter which will sleep for 900seconds before continue to scrape
# Min give this job about 20 mins
def twitter_by_topic_scrap():
    print("Start twitter_by_topic_scrap at : ", datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    logging.info("Start twitter_by_topic_scrap at : ")
    subprocess.call('cd /home/dchrahos/dashboard/twitter', shell=True)
    subprocess.call('python /home/dchrahos/dashboard/twitter/DCHR_Twitter_scrap_by_topic_name.py', shell=True)
    logging.info("Finished in scrapping")

# This min requires 3-5 min of scrapping depends on the number of keywords
# It can take more than 10 mins if it hits the max request set by twitter which will sleep for 900seconds before continue to scrape
# Min give this job about 20 mins
def twitter_by_screen_name_scrap():
    print("Start twitter_by_screen_name_scrap at : ", datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    logging.info("Start twitter_by_screen_name_scrap at : ")
    subprocess.call('cd /home/dchrahos/dashboard/twitter', shell=True)
    subprocess.call('python /home/dchrahos/dashboard/twitter/DCHR_Twitter_scrap_by_screen_name.py', shell=True)
    logging.info("Finished in scrapping")

 # This min requires 3-5 min of scrapping depends on the number of keywords
# It can take more than 10 mins if it hits the max request set by twitter which will sleep for 900seconds before continue to scrape
# Min give this job about 20 mins
def twitter_by_product_scrap():
    print("Start twitter_by_product_scrap at : ", datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    logging.info("Start twitter_by_product_scrap at : ")
    subprocess.call('cd /home/dchrahos/dashboard/twitter', shell=True)
    subprocess.call('python /home/dchrahos/dashboard/twitter/DCHR_Twitter_scrap_by_product.py', shell=True)
    logging.info("Finished in scrapping")

# This min requires 60 min of scrapping depends on the number of keywords
# It can take more than 40 mins Min give this job about 50 mins
def GoogleNews_by_Category_scrap():
    print("Start GoogleNews_by_Category_scrap at : ", datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    logging.info("Start GoogleNews_by_Category_scrap at : ")
    subprocess.call('cd /home/dchrahos/dashboard/GoogleNews', shell=True)
    subprocess.call('python /home/dchrahos/dashboard/GoogleNews/googlerss_Category.py', shell=True)
    logging.info("Finished in scrapping")

# This min requires 60 min of scrapping depends on the number of keywords
# It can take more than 40 mins Min give this job about 50 mins
def GoogleNews_by_Keyword_scrap():
    print("Start GoogleNews_by_Keyword_scrap at : ", datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    logging.info("Start GoogleNews_by_Keyword_scrap at : ")
    subprocess.call('cd /home/dchrahos/dashboard/GoogleNews', shell=True)
    subprocess.call('python /home/dchrahos/dashboard/GoogleNews/googlerss_Keyword.py', shell=True)
    logging.info("Finished in scrapping")

# This min requires 60 min of scrapping depends on the number of keywords
# It can take more than 40 mins Min give this job about 50 mins
def GoogleNews_by_Product_scrap():
    print("Start GoogleNews_by_Product_scrap at : ", datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    logging.info("Start GoogleNews_by_Product_scrap at : ")
    subprocess.call('cd /home/dchrahos/dashboard/GoogleNews', shell=True)
    subprocess.call('python /home/dchrahos/dashboard/GoogleNews/googlerss_Product.py', shell=True)
    logging.info("Finished in scrapping")

# This min requires 60 min of scrapping depends on the number of keywords
# It can take more than 40 mins Min give this job about 50 mins
def Create_GoogleNews_Datasets_Category():
    print("Start Create_GoogleNews_Datasets_Category at : ", datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    logging.info("Start Create_GoogleNews_Datasets_Category at : ")
    subprocess.call('cd /home/dchrahos/dashboard/GoogleNews', shell=True)
    subprocess.call('python /home/dchrahos/dashboard/GoogleNews/Google_news_by_Category.py', shell=True)
    logging.info("Finished in Creating excel data files")

# This min requires 60 min of scrapping depends on the number of keywords
# It can take more than 40 mins Min give this job about 50 mins
def Create_GoogleNews_Datasets_Keyword():
    print("Start Create_GoogleNews_Datasets_Keyword at : ", datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    logging.info("Start Create_GoogleNews_Datasets_Keyword : ")
    subprocess.call('cd /home/dchrahos/dashboard/GoogleNews', shell=True)
    subprocess.call('python /home/dchrahos/dashboard/GoogleNews/Google_news_by_Keyword.py', shell=True)
    logging.info("Finished in Creating excel data files")

# This min requires 60 min of scrapping depends on the number of keywords
# It can take more than 40 mins Min give this job about 50 mins
def Create_GoogleNews_Datasets_Product():
    print("Start Create_GoogleNews_Datasets_Product at : ", datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    logging.info("Start Create_GoogleNews_Datasets_Product at : ")
    subprocess.call('cd /home/dchrahos/dashboard/GoogleNews', shell=True)
    subprocess.call('python /home/dchrahos/dashboard/GoogleNews/Google_news_by_Product.py', shell=True)
    logging.info("Finished in Creating excel data files")

def Copy_data_to_download_folder():
    print("Start Copy_data_to_download_folder at : ", datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    logging.info("Start Copy_data_to_download_folder at : ")
    subprocess.call(r'cp /home/dchrahos/dashboard/twitter/data/DCHR_Twitters_by_topics.xlsx /home/dchrahos/public_html/DCHR1/DCHR_Twitters_by_topics.xlsx',shell=True)
    subprocess.call(r'cp /home/dchrahos/dashboard/twitter/data/DCHR_Influencer_tweets.xlsx /home/dchrahos/public_html/DCHR1/DCHR_Influencer_tweets.xlsx',shell=True)
    subprocess.call(r'cp /home/dchrahos/dashboard/twitter/data/DCHR_Twitters_by_product.xlsx /home/dchrahos/public_html/DCHR1/DCHR_Twitters_by_product.xlsx',shell=True)
    subprocess.call(r'cp /home/dchrahos/dashboard/GoogleNews/data/DCHR_Google_Category.xlsx /home/dchrahos/public_html/DCHR1/DCHR_Google_Category.xlsx',shell=True)
    subprocess.call(r'cp /home/dchrahos/dashboard/GoogleNews/data/DCHR_Google_Keyword.xlsx /home/dchrahos/public_html/DCHR1/DCHR_Google_Keyword.xlsx',shell=True)
    subprocess.call(r'cp /home/dchrahos/dashboard/GoogleNews/data/DCHR_Google_Product.xlsx /home/dchrahos/public_html/DCHR1/DCHR_Google_Product.xlsx',shell=True)
    logging.info("Finished in copying")
    logging.info("End:")

def RunTaskPeriodically():
    try:
        # Actuvtae the dashboard python virtual env
        subprocess.call('source /home/dchrahos/virtualenv/DCHR1/3.7/bin/activate', shell=True)
        
        # Start of the twitter scrapping & create datasets jobs
        schedule.every().sunday.at('01:00').do(twitter_by_topic_scrap)
        schedule.every().sunday.at('02:00').do(twitter_by_screen_name_scrap)
        schedule.every().sunday.at('03:00').do(twitter_by_product_scrap)

        # Start of the Google scrapping jobs
        schedule.every().sunday.at('04:00').do(GoogleNews_by_Category_scrap)  
        schedule.every().sunday.at('05:30').do(GoogleNews_by_Keyword_scrap)
        schedule.every().sunday.at('07:00').do(GoogleNews_by_Product_scrap)

        # Start of the Creating of Google dataset jobs
        schedule.every().sunday.at('08:30').do(Create_GoogleNews_Datasets_Category)
        schedule.every().sunday.at('09:00').do(Create_GoogleNews_Datasets_Keyword)
        schedule.every().sunday.at('09:30').do(Create_GoogleNews_Datasets_Product)

        # Start copy created data excel file to public folder for download to windows PC
        schedule.every().sunday.at('10:00').do(Copy_data_to_download_folder)

        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        today = datetime.now()
        d = today.strftime("%b-%d-%Y")

        # Logging information
        print("RunTaskPeriodically: "+str(e)+"/n")
        logging.error("RunTaskPeriodically: "+str(e)+"/n")

print('START:', datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
logging.info('START:')

RunTaskPeriodically()
