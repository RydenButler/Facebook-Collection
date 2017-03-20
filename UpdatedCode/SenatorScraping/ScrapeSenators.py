import csv
import re

# Collect urls from csv of senator information
senator_pages = []
with open('SenatorURLs.csv', 'rb') as urls:
  reader = csv.reader(urls)
  for row in reader:
    senator_pages.extend(row)

# Extract facebook page names for each senator
senator_pages = [re.search('.com/(.+?)/', page).group(1) for page in senator_pages[1:]]

# Pick one of the below scrapers to use
from SenateLikerVerbose import *
#from SenateLiker import *

# Running this function requires:
#   1) Navigating to the SenatorScraping directory in the terminal.
#   2) Picking one of the above scrapers to user. The verbose one fills your terminal with updates. Otherwise they are identical.
#   3) Reading an app id and app secret from the Graph API into python.
#   4) Setting the function's arguments ID and SECRET to the correspoding object names of you app id and secret
# The first senator, Luther Strange, doesn't work for some reason through the API; this is not an indexing error
data = like_scraper(senator_pages[1:], ID, SECRET)

data['RichardShelby'][1]

from DataSaver import *

make_csv(data)
