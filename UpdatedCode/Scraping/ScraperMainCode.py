# Import system path modifier
import sys
# Set system path to view scraper
sys.path.insert(0, 'Facebook-Project/UpdatedCode/Scraping')
# Import parallelization tools
from joblib import Parallel, delayed
import multiprocessing
# Set number of cores
num_cores = multiprocessing.cpu_count()
# Import csv reader
import csv
# Import regular expression handler
import re
# Import the app id and secret
from Secrets import *
# Import the like scraper
from ParallelScrape import *
# Make lists of APP IDs and APP SECRETs
APP_ID_LIST = [APP_ID_1, APP_ID_2, APP_ID_3, APP_ID_4, APP_ID_5]
APP_SECRET_LIST = [APP_SECRET_1, APP_SECRET_2, APP_SECRET_3, APP_SECRET_4, APP_SECRET_5]

# The basic scraper takes the form:
bad_pages = scrape_and_save('__Facebook__page__extension__', APP_ID_LIST, APP_SECRET_LIST, 'Data/__Save_to_Folder__', __start__post__number__)

# For parallel scraping, use:
bad_pages = Parallel(n_jobs = num_cores) (delayed(scrape_and_save) (page, APP_ID_LIST, APP_SECRET_LIST, 'Data/__Save_to_Folder__') for page in __List__of_Page__Extensions__)





##############################
### Scraping in the Senate ###
##############################

# Collect urls from csv of Senate information
senate_pages = []
with open('Data/SenateData/SenateFBIDs.csv', 'rb') as urls:
  reader = csv.reader(urls)
  for row in reader:
    senate_pages.extend(row)

# Scrape pages
bad_pages = Parallel(n_jobs = num_cores) (delayed(scrape_and_save) (page, APP_ID_LIST, APP_SECRET_LIST, 'Data/SenateDBs') for page in senate_pages[0:76]) # split senate_pages on sanders [76]
bad_pages = Parallel(n_jobs = num_cores) (delayed(scrape_and_save) (page, APP_ID_LIST, APP_SECRET_LIST, 'Data/SenateDBs') for page in senate_pages[76:100])

# Could not run 'MarkRWarner', 'toomey', 'SenatorRisch', 'SenatorWicker'

# Thad-Cochran/112579789754326 is an about page, without posts
# Manually collected 'wicker', 'patricktoomey'

# (3) Risch, Warner, and Cochran remain un-collected





# Collect urls from csv of Senate challenger information
senate_challengers = []
with open('Data/SenateData/SenateChallengerFBIDs.csv', 'rb') as urls:
  reader = csv.reader(urls)
  for row in reader:
    senate_challengers.extend(row)

# Scrape pages
bad_pages = Parallel(n_jobs = num_cores) (delayed(scrape_and_save) (page, APP_ID_LIST, APP_SECRET_LIST, 'Data/SenateDBs') for page in senate_challengers)

# Could not run 'KirkpatrickForArizona', 'Mike-Crapo-For-US-Senate-286049384763373', 'charles.nana.549?hc_ref=PAGES_TIMELINE&fref=nf', 
#     'KeyserforColorado', 'Gottschalk-for-US-Senate-from-Hawaii-976398255789229', 'Napoleon-Harris-For-Illinois-802138363224253', 
#     'Monique-Singh-Bey-for-Senate-1014687671910923', 'Elect-Robert-Mack-196762574017716', 'voteswinton'
# Encountered errors on grant4KY post 145/400 and 155/400
# KirkpatrickForArizona and voteswintonis unavailable (expired)
# charles.nana.549 is a personal account
# Manually collected 'Mike-Crapo-For-US-Senate-286049384763373' (286049384763373), 'Napoleon-Harris-For-Illinois-802138363224253'(802138363224253), 
#     'Gottschalk-for-US-Senate-from-Hawaii-976398255789229' (976398255789229), 'Monique-Singh-Bey-for-Senate-1014687671910923' (1014687671910923)

#(2) KeyserforColorado and Elect-Robert-Mack-196762574017716 remain un-collected


#############################
### Scraping in the House ###
#############################

# Collect urls from csv of House information
house_pages = []
with open('Data/HouseData/HouseFBIDs.csv', 'rb') as urls:
  reader = csv.reader(urls)
  for row in reader:
    house_pages.extend(row)

# Scrape pages
bad_pages = Parallel(n_jobs = num_cores) (delayed(scrape_and_save) (page, APP_ID_LIST, APP_SECRET_LIST, 'Data/HouseDBs') for page in house_pages)

# Could not run 'RepBarbaraComstock', 'congressman-Tom-Garrett-1835767753333490', 'CongressmanGarrettGraves', 'CongressmanKevinMcCarthy',
#     'RepStephMurphy', 'RepSteveWomack', 'RepKenCalvert', 'RepPaulCook', 'johnculberson', 'RepVirginiaFox', 'repalgreen', 'FrankLoBiondo',
#     'Rep-Billy-Long', 'Rep.PeteOlson', 'bill.posey15', 'CongressmanMikeDRogers', 'RepSensenbrenner', 'CongresswomanSinema', 'WalzforGovernor'
# Encountered error on DondaldNorcrossNJ post 2978/4415
# RepSteveWomack is unavailable (expired)
# Tim Waltz has no official Facebook page; WalzforGovernor is neither official, nor explicitly related to his congressional career
# Manually collected '1835767753333490' ('congressman-Tom-Garrett-1835767753333490'), '280117065340803' ('billposeycampaign'),
#     '159964696102' ('kevinomccarthy'), 'CongressmanCulberson', 'garretngraves', 'CharimanMikeRogers', 'ksinemaaz'

# (12) Comstock, Murphy, Womack, Calvert, Cook, Foxx, Green, LoBiondo, Long, Olson, Sensenbrenner, Waltz remain un-collected





##########################
### Scraping Governors ###
##########################

# Collect urls from csv of Senate information
governor_pages = []
with open('Data/GovernorData/GovernorFBIDs.csv', 'rU') as urls:
  reader = csv.reader(urls, dialect=csv.excel_tab)
  for row in reader:
    governor_pages.extend(row)

# Scrape pages
bad_pages = Parallel(n_jobs = num_cores) (delayed(scrape_and_save) (page, APP_ID_LIST, APP_SECRET_LIST, 'Data/GovernorDBs') for page in governor_pages)

# Could not run 'MikeForUtah', 'marchandforNH: post 78', 'BruceCuffForGovernorOfOregon', 'Bob-Niemeyer-for-Governor-of-Oregon-1611492885780732',
#     'LismanForVermont', 'Draft-Booth-Goodwin-2016-912804338811477'
# Encountered error on marchandforNH post 78/597.
# MikeForUtah is unavailable (expired)
# Manually collected Bob-Niemeyer-for-Governor-of-Oregon-1611492885780732 (1611492885780732) and Draft-Booth-Goodwin-2016-912804338811477 (912804338811477)

# (2) BruceCuffForGovernorOfOregon, LismanForVermont remain un-collected




############################
### Scraping Think Tanks ###
############################

# Collect urls from csv of Think Tank information
thinktank_pages = []
with open('Data/ThinkTankData/ThinkTankPages.csv', 'rb') as urls:
  reader = csv.reader(urls)
  for row in reader:
    thinktank_pages.extend(row)

# Replace UTF-8 characters with dash
thinktank_pages = [page.replace('\xc2\xad', '-') for page in thinktank_pages]

bad_pages = Parallel(n_jobs = num_cores) (delayed(scrape_and_save) (page, APP_ID_LIST, APP_SECRET_LIST, 'Data/ThinkTankDBs') for page in thinktank_pages)

# Could not run '108322432522707', '351457957011', 'progressivepolicyinstitute'
# The two numeric ids had missing numbers from the .csv import
# Manually collected '351457957011'

# (2) Project for the New American Century and Progressive Policy Institute remain un-collected





########################################
### Scraping Presidential Candidates ###
########################################

# Scrape pages
bad_pages = Parallel(n_jobs = num_cores) (delayed(scrape_and_save) (page, APP_ID_LIST, APP_SECRET_LIST, 'Data/PresidentDBs') for page in ['DonaldTrump', 'hillaryclinton', 'barackobama'])

# Scrape pages
bad_pages = Parallel(n_jobs = num_cores) (delayed(scrape_and_save) ('DonaldTrump', APP_ID_LIST, APP_SECRET_LIST, 'Data/PresidentDBs', start) for start in [0, 1500, 3000, 4500])

