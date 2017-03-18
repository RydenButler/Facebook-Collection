import facebook
import requests
import json
import ssl
import time

# Input a list of facebook page names; facebook.com/PAGENAME
def like_scraper(page_list, APP_ID, APP_SECRET):
  # Creating a session is necessary to handle some network/server errors
  # Retries are implemented in the scraping function to address other network issues
  sess = requests.Session()
  adapter = requests.adapters.HTTPAdapter(max_retries = 100)
  sess.mount('http://', adapter)

  # Initialize graph object
  graph = facebook.GraphAPI(version='2.2')
  # Generate access token
  my_token = graph.get_app_access_token(app_id = APP_ID, app_secret = APP_SECRET)
  # Pass valid access token to graph object
  graph = facebook.GraphAPI(access_token = my_token, version='2.2')
  # Create empty dictionary to store all scraped data
  # It will be stored hierarchically, with likes nested in comments, nested in facebook pages
  final_data = {}
  # Create tally for user notification
  tally = 0
  # Iterate over facebook pages
  for i in page_list:
    # Update tally for current iteration
    tally += 1
    print 'Scraping senator %d' % tally
    # Find user id
    # A while statement in this format is implemented at each point of scraping throughout the function.
    #   It is implemented because random SSL errors occur sporadically throughout scraping
    #   It is unclear why these occur or how to prevent them, save having python retry the connection
    #   In my experience these errors primarily occur when collecting likes or paginating over likes
    #   In principle, they can occur at any point requiring a network connection, so I implement them at all points to be safe
    while True:
      try:
        user = graph.get_object(i)
      except requests.exceptions.RequestException:
        time.sleep(60)
        continue
      break
    # Get 100 posts given a page id found above
    while True:
      try:
        posts = graph.get_connections(id=user['id'], connection_name='posts', limit = 100)
      except requests.exceptions.RequestException:
        time.sleep(60)
        continue
      break
    # Continue over pages of posts until last post is not dated 2017 or 2016
    # We can remove items post hoc to match desired date, but this is most efficient query method
    while posts['data'][-1]['created_time'][0:4] == '2017' or posts['data'][-1]['created_time'][0:4] == '2016':
      try:
        while True:
          try:
            more_posts = sess.get(posts['paging']['next']).json()
          except requests.exceptions.RequestException:
            time.sleep(60)
            continue
          break
        # Replaces paging info in posts object with latest page info
        posts['paging'] = more_posts['paging']
        # Adds all new posts to list
        posts['data'].extend(more_posts['data'])
      # Breaks if no new page can be found
      except KeyError:
        break
    # Loop over posts, extracting ids for likes query
    for j in posts['data']:
      # Update post tally
      post_tally += 1
      post_total = len(posts['data'])
      # Initial query of like ids 
      while True:
        try:
          likes = graph.get_connections(id = j['id'], connection_name = 'likes', limit = 1000)
        except requests.exceptions.RequestException:
          time.sleep(60)
          continue
        break
      # Loops over pages of likes until no remaining 'next' page
      while True:
        try:
          while True:
            try:
              more_likes = sess.get(likes['paging']['next']).json()
            except requests.exceptions.RequestException:
              time.sleep(60)
              continue
            break
          likes['paging'] = more_likes['paging']
          likes['data'].extend(more_likes['data'])
        except KeyError:
          break
      # Saves all likes in post as dictionary value
      j['likes'] = likes['data']
    # Saves post w/ nested likes as dictionary values w/ facebook page name as key
    final_data[i] = posts['data']
  return(final_data)