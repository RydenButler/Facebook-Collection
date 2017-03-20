import csv

# This is a simple function that replicate a list of one item that is the same length as a second object
# This is useful when creating a csv where, for instance, multiple observations correspond w/ a single id
# The first argument can be any object
# The second object must have length as a property
def replicator(replicate_this, comparison):
  rep = []
  for i in range(len(comparison)):
    rep.append(replicate_this)
  return rep


# Saves nested dictionaries into a csv file
# Requires an input of likes nested within posts, nested within page names
def make_csv(giant_tree):
  # Create empty lists for storage
  all_like_names = []
  all_like_ids = []  
  all_post_ids = []
  all_post_times = []
  all_post_messages = []
  all_senators = []
  # Iterate over facebook page names
  for page in giant_tree.keys():
    # Iterate over posts on a facebook page
    for post in giant_tree[page]:
      # Create empty lists for storage
      current_like_names = []
      current_like_ids = []
      # Iterate over individual likes on a post
      for liker in post['likes']:
        try:
          # Store name and id of liker
          current_like_names.append(liker['name'])
        except KeyError, name:
          # If no name field, record placeholder
          current_like_names.append('NO NAME FIELD')
        current_like_ids.append(liker['id'])
      # Create lists of post ids and times of equal length to the number of likers
      expanded_post_ids = replicator(post['id'], current_like_ids)
      expanded_post_times = replicator(post['created_time'], current_like_ids)
      # Not all posts have messages. Some have stories, and some are blank (maybe photos?)
      #   These nested tries first look for a message, then a story, then input a string
      try:
        expanded_post_messages = replicator(post['message'], current_like_ids)
      except KeyError, message:
        try:
          expanded_post_messages = replicator(post['story'], current_like_ids)
        except KeyError, story:
          expanded_post_messages = replicator('NO MESSAGE CONTENT', current_like_ids)
      # Create list of repeated facebook page names of equal length to likers
      expanded_senator_name = replicator(page, current_like_ids)
      # Extend lists containing all final data
      all_like_names.extend(current_like_names)
      all_like_ids.extend(current_like_ids)
      all_post_ids.extend(expanded_post_ids)
      all_post_times.extend(expanded_post_times)
      all_post_messages.extend(expanded_post_messages)
      all_senators.extend(expanded_senator_name)
  # Open csv called Output for storing data
  with open('Output.csv', 'wb') as f:
    # Name variables for header in csv
    my_writer = csv.DictWriter(f, fieldnames=("Page", "PostID", "PostTime", "PostMessage", "Username", "UserID"))
    my_writer.writeheader()
    # Iterate over each element of each list of data
    for i in range(len(all_like_ids)):
      # Save each data point in the corresponding row (by iteration) and column (by fieldname)
      my_writer.writerow({"Page":all_senators[i].encode('utf-8'), "PostID":all_post_ids[i].encode('utf-8'), "PostTime":all_post_times[i].encode('utf-8'), "PostMessage":all_post_messages[i].encode('utf-8'), "Username":all_like_names[i].encode('utf-8'), "UserID":all_like_ids[i].encode('utf-8')})
  return "Saved csv. Saved %d observations." % len(all_like_ids)
