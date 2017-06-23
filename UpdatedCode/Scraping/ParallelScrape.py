import facebook
import time
from SQLSaver import *
import sys
# Change the following for your own Dropbox path
sys.path.insert(0, '/Users/r.butler/Dropbox/Facebook/')
from WUSTLID import *

def scrape_and_save(page, APP_ID, APP_SECRET):
  # Initialize graph object
  graph = facebook.GraphAPI(version='2.7')
  print '''


  Connecting to GraphAPI...


  '''
  # Generate access token
  my_token = graph.get_app_access_token(app_id = APP_ID, app_secret = APP_SECRET)
  # Pass valid access token to graph object
  graph = facebook.GraphAPI(access_token = my_token, version='2.7')
  print 'Established authorized connection to GraphAPI.'
  # Create empty list to store errant pages
  missed_pages = []
  # Try to get page id and name from current link
  # If an API error occurs, add page link to list of errant pages, skip current iteration
  try:
    page_data = graph.get_object(page)
    # Name new database
    new_database = 'Data/IndividualDBS/%s.db' % (page)
    create_database(new_database)
    # Open connection to the database
    conn = create_connection(new_database)
    print '''


    Opened connection to %s


    ''' % (new_database)
  except facebook.GraphAPIError:
    print 'Page error occurred (possibly not public?). Page link added to error list.'
    missed_pages.append(page)
    return missed_pages
  # Insert page information into relevant table
  # Use the database connection while executing the following code
  with conn:
    insert_page(conn, page_data, page)
    conn.commit()
  # Collect posts; the while loop is necessary to catch errors
  while True:
    try:
      # Get all posts for current page; the object is a generator, hence the format
      posts = [i for i in graph.get_all_connections(id=page_data['id'], connection_name='posts')]
    # Put scraper to sleep for a minute if an API error occurs  
    except facebook.GraphAPIError:
      print 'There was an error collecting the posts. Scraper will take a 10 minute break.'
      time.sleep(600)
      continue
    break
  # Iterate over posts to check for empty message keys
  for post in posts:
    # Add page_id to post dictionary
    post['page_id'] = page_data['id']
    # If no message key exists, create one with the story content or enter note of missingness
    if 'message' not in post.keys():
      try:
        post['message'] = post['story'] 
      except KeyError, story:
        post['message'] = 'EMPTY MESSAGE CONTENT'
  # Insert post information into relevant table  
  with conn:
    insert_posts(conn, posts)
    conn.commit()
  # Empty tally for posts
  post_tally = 0
  # Iterate over posts to save likes
  for post in posts:
    post_tally += 1
    # Get all likes for current post
    while True:
      try:
        likes = [j for j in graph.get_all_connections(id=post['id'], connection_name='likes')]
      # Put scraper to sleep for a minute if encountering API error  
      except facebook.GraphAPIError:
        print 'There was an error collecting the likes. Scraper will take a 10 minute break.'
        time.sleep(600)
        continue
      break
    # Iterate over likes to check for empty name keys and add WUSTL IDs
    for like in likes:
      # If no name key exists, create note of missingness
      if 'name' not in like.keys():
        like['name'] = 'EMPTY NAME FIELD'
      # Add WUSTL ID
      like['WUSTLID'] = make_WUSTL_id(like['id'])
      # Add post ID
      like['post_id'] = post['id']
    # Insert users into relevant table
    with conn:
      insert_likes(conn, likes)
      conn.commit()
    print 'Saving %d likes for post %d / %d for %s' % (len(likes), post_tally, len(posts), page)
  conn.close()
  return missed_pages
