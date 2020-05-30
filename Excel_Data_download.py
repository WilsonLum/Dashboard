import logging
from datetime import datetime
import urllib.request as urllib

# Logging information
logFileName = 'log/Excel_data_download.log'
logging.basicConfig(filename=logFileName,filemode='a',level=logging.INFO,format='%(asctime)s :: %(levelname)s :: %(message)s')

# Open file and get source and destionation address
src_dest_filename = "input/src_dest.txt"
f1 = None
try:
	with open(src_dest_filename, 'r') as f1:
		address = [line.rstrip('\n') for line in f1]

except Exception as e:
	today = datetime.now()
	error_time = today.strftime("%b-%d-%Y %H:%M:%S")
	print("Unable to read at row " + src_dest_filename + " Error %s" % (e) + " at " + str(error_time))
	logging.error("Unable to read at row " + src_dest_filename + " Error %s" % (e) + " at " + str(error_time))
	sys.exit(1)

finally:
	if f1 is not None:
		f1.close()

# Open file and get source and destionation address
user_pwd_filename = "input/Cpanel_pwd.txt"
f2 = None
try:
	with open(user_pwd_filename, 'r') as f2:
		user_pwd = [line.rstrip('\n') for line in f2]

except Exception as e:
	today = datetime.now()
	error_time = today.strftime("%b-%d-%Y %H:%M:%S")
	print("Unable to read at row " + user_pwd_filename + " Error %s" % (e) + " at " + str(error_time))
	logging.error("Unable to read at row " + user_pwd_filename + " Error %s" % (e) + " at " + str(error_time))
	sys.exit(1)

finally:
	if f2 is not None:
		f2.close()

# Variable definitions
twitter_outfilename   = ['DCHR_Twitters_by_topics.xlsx','DCHR_Influencer_tweets.xlsx','DCHR_Twitters_by_product.xlsx']
googlerss_outfilename = ['DCHR_Google_Category.xlsx', 'DCHR_Google_Product.xlsx', 'DCHR_Google_Keyword.xlsx']
url_of_file   = address[0]
output_folder = address[1]
twitter_outputFolder   = output_folder + '\\twitter\\data\\'
googlerss_outputFolder = output_folder + '\\GoogleNews\\data\\'

username = user_pwd[0]
password = user_pwd[1]

print('username :\n', username)
print('password :\n', password)

# create a password manager
password_mgr = urllib.HTTPPasswordMgrWithDefaultRealm()

# Add the username and password.
# If we knew the realm, we could use it instead of None.
password_mgr.add_password(None, url_of_file, username, password)

handler = urllib.HTTPBasicAuthHandler(password_mgr)

# create "opener" (OpenerDirector instance)
opener = urllib.build_opener(handler)

# use the opener to fetch a URL
opener.open(url_of_file)

# Install the opener.
# Now all calls to urllib.request.urlopen use our opener.
urllib.install_opener(opener)

today = datetime.now()
d     = today.strftime("%b-%d-%Y")

logging.info("*******************************************************************")
logging.info("Download Excel dataset  at " + str(d))
logging.info("*******************************************************************\n")

for f in twitter_outfilename:
	print("Downloading ", f)
	logging.info("Downloading " + f)
	urllib.urlretrieve(url_of_file+f, twitter_outputFolder+f) 

for f in googlerss_outfilename:
	print("Downloading ", f)
	logging.info("Downloading " + f)
	urllib.urlretrieve(url_of_file+f, googlerss_outputFolder+f) 