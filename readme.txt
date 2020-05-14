# Dashboard
## DCHR DashBoard
This is a summary for the setup of Linux Server adn Windows 10 platform. For actual adn detail installations, please refer to the documentation in the installation folder.
This programs are for collecting GoogleRSS news and Twitter data and present in Power BI dashboard :
 1. GoogleRSS News Scrapping by HR Category, Products & Keywords, Preprocessed the text data and creating of datasets for Power BI Dashboard
 2. Twiiter Influencer and keywords Scrapping, Preprocessed the text data and creating of datasets for Power BI Dashboard

## Folders Creation Information under dashbpard folder
 1. Installations - Installations files, instructions & Requirements
 2. DCHR          - Python virtual env for Decode HR for both GoogleNews and Twitters
 3. GoogleNews    - GoogleRSS news scrapping, preprocess and Power BI files
    3.1 data    - to store the excel file created
    3.2 doc     - detail user guide 
    3.3 input   - Storing input text file for user to enter preferred configurations eg keywords to search and stopwords
    3.4 diagram - to store generated bigram/trigram jpg files 
    3.5 log     - logging of codes output
    3.6 topic   - store the output of pyLDvis HTML format
 4. Twitter       - Twitters news scrapping, preprocess and Power BI files
    3.1 data    - to store the excel file created
    3.2 doc     - detail user guide 
    3.3 input   - Storing input text file for user to enter preferred configurations eg keywords to search and stopwords
    3.4 diagram - to store generated bigram/trigram jpg files 
    3.5 log     - logging of codes output

## Installation requirements
 1. Install python - python_venv_Installation.docx (Under Instalation folder)
 2. Install Microsoft Power BI - PBIDesktopSetup_x64.exe (Under Instalation folder)
 
## Installing Python Env
To run in the python env: This is for first time setup.
 1a. Activate the env: (Linux Server platform)
   - Activate the env (Follow the detail Installation guide)
     source /home/dchrahos/virtualenv/DCHR_Dashboard/3.7/bin/activate
   - Go to working folder
     cd /home/dchrahos/dashboard
 1b. Command to create the virtual environment:(Windows platform)
   - Cd "<your path>\dashboard” (Go to the dashboard working folder)
   - python -m venv DCHR (Create virtual env)
   - .\DCHR\Scripts\activate  (Activate the env)
   - For windows platform, need to install Visual Studio C++

 2. Install the library:
   - python -m pip install --upgrade pip (If not upgraded)
   - pip install -r requirements.txt
   - python -m spacy download en_core_web_sm
   - python -m spacy download en_core_web_md
   - python -m spacy download en_core_web_lg 
   - python install_nltk_spacy_package.py (For installing nltk & spacy library)
   - May need to rename the english to English in /home/dchrahos/nltk_data/corpora/stopwords folder

3. Cronjob configuration (Linux Server platform)
   - ## Cron job
   - Recommend to configure once a year schedule for this cronjob (As the actual scheduling of running the programs are in the python codes
   - source /home/dchrahos/virtualenv/DCHR_Dashbaord/3.7/bin/activate && cd /home/dchrahos/dashboard && python Server_schedule_process.py

## GoogleRSS News
Process procedures under GoogleNews folder:
 1. Input - For preferred keywords scrapping and stopwords (Under Input folder)
  - Google_search_Category.txt - Input Category words for scrapping. It must be per category per line
  - Google_search_Keyword.txt  - Input Keyword  words for scrapping. It must be per Keyword per line
  - Google_search_Product.txt  - Input Product  words for scrapping. It must be per Product per line
  - stopwords.txt              - Input Stopwords for scrapping. It must be per word per line
  - spacy_model.txt            - Input only one of the options : (Default in the code is "en_core_web_sm")
                                 a. en_core_web_sm
                                 b. en_core_web_md
                                 c. en_core_web_lg
  - number_of_topics.txt       - Input for the number of topics to test
                               - first  line is the minimum number of topics
                               - second line is the maximum number of topics
 2. GoogleRSS News Scrapping (Output to data folder)
  - python Server_schedule_process.py (running this as cronjob)
  - Steps from below step 3 are automated and scheduled in the above Server_schedule_process.py. Hence is FYIR only
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
    After which from second time onwards just select the "Refresh" button from the menu to get the latest datasets.
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
  - Run Twitter_by_screen_name_Scrape 
    - (Output to DCHR_Twitters_by_topics.xlsx for use by Power BI)
    - (Output to DCHR_Twitters_by_topics.xlsx_[Date].xlsx for log and history reference)
  - Run Twitter_by_screen_name_Scrape 
    - (Output to DCHR_Influencer_tweets.xlsx for use by Power BI)
    - (Output to DCHR_Influencer_tweets.xlsx_[Date].xlsx for log and history reference)
 4. Run Power BI
    For first time setup, may need to go to Transform data and select dataset source to change and point to the respective excel file processed in step 3
    After which from second time onwards just select the "Refresh" button from the menu to get the latest datasets.
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

For process hang we can kill them using following command:(Linux Server Platform)
1. ps -ef | grep python (To check what are the process numbers or pid)
2. kill -9 <pid> (i.e. the pid returned)
3. python -m venv <name> (Remove virtual env)