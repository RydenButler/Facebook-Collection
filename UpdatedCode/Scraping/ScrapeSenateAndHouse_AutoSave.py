import csv
import re
import sys
sys.path.insert(0, 'Facebook-Project/UpdatedCode/Scraping')

# Collect urls from csv of Senate information
senate_pages = []
with open('Data/SenateData/SenateURLs.csv', 'rb') as urls:
  reader = csv.reader(urls)
  for row in reader:
    senate_pages.extend(row)

# Extract facebook page names for each senator
senate_pages = [re.search('.com/(.*)', page).group(1) for page in senate_pages] # start at 1 b/c 0 is the header

# Collect urls from csv of House information
house_pages = []
with open('Data/HouseData/HouseURLs.csv', 'rb') as urls:
  reader = csv.reader(urls)
  for row in reader:
    house_pages.extend(row)

# Extract facebook page names for each congress-person
house_pages = [re.search('.com/(.*)', page).group(1) for page in house_pages]

# Import the like scraper
from LikeScraper_AutoSave import *

# Running this function requires:
#   1) Navigating to the main project directory in the terminal. For me: cd Dropbox/Facebook
#   2) Reading an app id and app secret from the Graph API into python. This should be stored in the top-level of the Dropbox file.
#   3) Setting the function's arguments ID and SECRET to the correspoding object names of your app id and secret
#   4) Set the name of the database you want to populate. If no database exists, run create_databse() below
# Note that the function returns any pages on which an error occurred. These are stored in bad_pages and can be re-run manually.
bad_pages_S = like_scraper(senate_pages, APP_ID, APP_SECRET, 'Data/Facebook.db')
bad_pages_H = like_scraper(senate_pages, APP_ID, APP_SECRET, 'Data/Facebook.db')

# If no database exists:
#from SQLSaver import *
#create_database('Data/Facebook.db')
