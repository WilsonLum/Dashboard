# Dashboard
## DCHR DashBoard
This repo is for collecting GoogleRSS news and Twitter data and present in Power BI dashboard :
 1. GoogleRSS News Scrapping by HR Category, Products & Keywords, Preprocessed the text data and creating of datasets for Power BI Dashboard
 2. Twiiter Influencer and keywords Scrapping, Preprocessed the text data and creating of datasets for Power BI Dashboard

## Folders Information
 1. Installations - Installations files, instructions & Requirements
 2. DCHR          - Python virtual env for Decode HR for both GoogleNews and Twitters
 3. GoogleNews    - GoogleRSS news scrapping, preprocess and Power BI files
 4. Twitter       - Twitters news scrapping, preprocess and Power BI files

## Installation requirements
 1. Install python - python-3.8.2-amd64.exe (Under Instalation folder)
 2. Install Microsoft Power BI - PBIDesktopSetup_x64.exe (Under Instalation folder)
 
## Python Env
To run in the python env: (But this is not required as the batch file has cater to run into the DCHR env),. This is for first time setup.
 1. Activate the env:
   - Create virtual env:
     python -m venv "<your path>\dashboard\DCHR"
   - Activate the env
     .\DCHR\Scripts\activate
 2. Install the library:
   - pip install -r requirements.txt
   - python -m spacy download en_core_web_lg 

## GoogleRSS News
Process procedures under GoogleNews folder:
 1. Input - For preferred keywords scrapping and stopwords (Under Input folder)
  - Google_search_Category.txt - Input Category words for scrapping. It must be per category per line
  - Google_search_Keyword.txt  - Input Keyword  words for scrapping. It must be per Keyword per line
  - Google_search_Product.txt  - Input Product  words for scrapping. It must be per Product per line
  - stopwords.txt              - Input Stopwords for scrapping. It must be per word per line
 2. GoogleRSS News Scrapping (Output to data folder)
  - Run GoogleRSS_Scrape_Category.bat - For Category keyword scrapping (Output to data/Category/<Category>.json)
  - Run GoogleRSS_Scrape_Keyword.bat  - For Keyword  keyword scrapping (Output to data/Keyword/<Keyword>.json)
  - Run GoogleRSS_Scrape_Product.bat  - For Product  keyword scrapping (Output to data/Product/<Product>.json)
 3. Create Dataset in excel format (Output to data)
  - Run Create_Google_news_dataset_by_Category.bat 
    - (Output to DCHR_Google_Category.xlsx for use by Power BI)
    - (Output to DCHR_Google_Category_[Date].xlsx for log and history reference)
  - Run Create_Google_news_dataset_by_Keyword.bat  
    - (Output to DCHR_Google_Keyword.xlsx for use by Power BI)
    - (Output to DCHR_Google_Keyword_[Date].xlsx for log and history reference)
  - Run Create_Google_news_dataset_by_Product.bat
    - (Output to DCHR_Google_Product.xlsx for use by Power BI)
    - (Output to DCHR_Google_Product_[Date].xlsx for log and history reference)
 4. Run Power BI
    For first time setup, may need to go to Transform data and select dataset source to change and point to the respective excel file processed in step 3
    - DCHR-GoogleNews_by_Category.pbix
    - DCHR-GoogleNews_by_Keyword.pbix
    - DCHR-GoogleNews_by_Product.pbix
 
## Twitter
Process procedures under Twitter folder:
 1. Input - For preferred keywords scrapping and stopwords (Under Input folder)
  - Twitter_Token.txt          - Twitter authenication and access tokens
  - Twitter By Topic List.txt  - Input Topic keywords for scrapping. It must be per topic per line
  - Twitter Infuencer List.txt - Input Keyword  words for scrapping. It must be per influecener screen name per line
 2. Create Dataset in excel format (Output to data)
  - Run Twitter_by_topic_Scrape.bat 
    - (Output to DCHR_Twitters_by_topics.xlsx for use by Power BI)
    - (Output to DCHR_Twitters_by_topics.xlsx_[Date].xlsx for log and history reference)
  - Run Twitter_by_screen_name_Scrape.bat  
    - (Output to DCHR_Influencer_tweets.xlsx for use by Power BI)
    - (Output to DCHR_Influencer_tweets.xlsx_[Date].xlsx for log and history reference)
 4. Run Power BI
    For first time setup, may need to go to Transform data and select dataset source to change and point to the respective excel file processed in step 3
    - Twttier_by_topic.pbix
    - Twttier_influencer.pbix

## Log and Documentation files
Logging and documentation data are save into the respective folders:
1. GoogleRSS News:
  - googleNews/log
  - googleNews/doc
2. Twitter:
  - twitter/log
  - twitter/doc
  
