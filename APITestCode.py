import facebook

# initialize graph object
graph = facebook.GraphAPI(version='2.2')
# generate access token
my_token = graph.get_app_access_token(app_id = APP_ID, app_secret = APP_SECRET)
# pass valid access token to graph object
graph = facebook.GraphAPI(access_token = my_token, version='2.2')

# this is just useful to test if id leads to valid node
node = graph.get_object(id='11052154359_10155018255819360')

# need to find some automated way of getting politicians' page ids

# get 100 posts given page id
# !!! figure out how to move over multiple pages
# the first element of posts might help with this
# !!! figure out how to set date range
posts = graph.get_connections(id='11052154359', connection_name='posts', limit = 100)

# generate list of post ids
post_ids = []
for i in posts[u'data']:
	post_ids.append(i[u'id'])

# generate list of likers
# so far there seems to be no limit on likes, but this can't be right
likers = []
for j in post_ids:
  likes = graph.get_connections(id=j, connection_name = 'likes', limit = 100000000000)
  likers.append(likes)


# keep this handy to test the de facto limit on likes
len(likes[u'data'])
