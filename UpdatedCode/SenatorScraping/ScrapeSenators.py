import csv
import re
import sys
sys.path.insert(0, 'Facebook-Project/UpdatedCode/SenatorScraping')

# Collect urls from csv of senator information
senator_pages = []
with open('Data/SenateData/Scraping/SenatorURLs.csv', 'rb') as urls:
  reader = csv.reader(urls)
  for row in reader:
    senator_pages.extend(row)

# Extract facebook page names for each senator
senator_pages = [re.search('.com/(.+?)/', page).group(1) for page in senator_pages[1:]]

# Pick one of the below scrapers to use
from SenateLikerVerbose import *
#from SenateLiker import *

# Running this function requires:
#   1) Navigating to the main project directory in the terminal. For me: cd Dropbox/Facebook
#   2) Picking one of the above scrapers to user. The verbose one fills your terminal with updates. 
#      They are otherwise functionally identical.
#   3) Read an app id and app secret from the Graph API into python.
#   4) Setting the function's arguments ID and SECRET to the correspoding object names of you app id and secret
# The first senator, Luther Strange, doesn't work for some reason through the API; this is not an indexing error
results = like_scraper(senator_pages[0:2], APP_ID, APP_SECRET)
data = results['Data']
bad_pages = results['Errors']

# Quickly check that the data looks okay
data['RichardShelby'][1]

# Choose whether to save data as .db or .csv
# For .db (SQL)
from SQLSaver import *

create_database('Likes.db')

populate_database(data, 'Likes.db')

# For .csv
from CSVSaver import *

make_csv(data)
