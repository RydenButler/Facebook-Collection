import facebook
import requests
import json
import csv
import re

# initialize graph object
graph = facebook.GraphAPI(version='2.2')
# generate access token
my_token = graph.get_app_access_token(app_id = APP_ID, app_secret = APP_SECRET)
# pass valid access token to graph object
graph = facebook.GraphAPI(access_token = my_token, version='2.2')

# collect urls from csv
senator_pages = []
with open('SenatorURLs.csv', 'rb') as urls:
  reader = csv.reader(urls)
  for row in reader:
  	senator_pages.extend(row)
# extract username
senator_pages = [re.search('.com/(.+?)/', page).group(1) for page in senator_pages[1:]]

# generate list of likers
likers = []
# the first senator doesn't work for some reason through the API
for i in senator_pages[1:]:
  # find user id
  user = graph.get_object(i)
  # get 100 posts given a page id
  # continues to collect posts by the 100 until year is 2015
  # we can remove items post hoc to match desired date, but this is most efficient query
  posts = graph.get_connections(id=user['id'], connection_name='posts', limit = 100)
  # continue over pages until last post is dated 2015
  # !!! need to add exceptions
  while posts['data'][-1]['created_time'][0:4] != '2015':
    # requests next page of posts from API
    more_posts = requests.get(posts['paging']['next']).json()
    # replaces paging info in posts object with latest page info
    posts['paging'] = more_posts['paging']
    # adds all new posts to list
    posts['data'].extend(more_posts['data'])
  # extract list of post ids
  post_ids = []
  for i in posts['data']:
    post_ids.append(i['id'])
  for j in post_ids:
    # initial query of like ids 
    likes = graph.get_connections(id = j, connection_name = 'likes', limit = 1000)
    # loops over pages until no remaining 'next' page
    while True:
      try:
        more_likes = requests.get(likes['paging']['next']).json()
        likes['paging'] = more_likes['paging']
        likes['data'].extend(more_likes['data'])
      except KeyError:
        break
    likers.extend(likes['data'])

