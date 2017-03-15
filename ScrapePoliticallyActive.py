import facebook
import requests
import json

# initialize graph object
graph = facebook.GraphAPI(version='2.2')
# generate access token
my_token = graph.get_app_access_token(app_id = APP_ID, app_secret = APP_SECRET)
# pass valid access token to graph object
graph = facebook.GraphAPI(access_token = my_token, version='2.2')


# get 100 posts given a page id
# continues to collect posts by the 100 until year is 2015
# we can remove items post hoc to match desired date, but this is most efficient query
user = graph.get_object('DonaldTrump')
posts = graph.get_connections(id=user['id'], connection_name='posts', limit = 100)
while posts['data'][-1]['created_time'][0:4] != '2015':
  more_posts = requests.get(posts['paging']['next']).json()
  posts['paging'].update(more_posts['paging'])
  posts['data'].extend(more_posts['data'])
  posts['data'][-1]['created_time'][0:4]

# extract list of post ids
post_ids = []
for i in posts['data']:
	post_ids.append(i['id'])

# generate list of likers
# so far there seems to be no limit on likes, but this can't be right
likers = []
for j in post_ids:
  likes = graph.get_connections(id = j, connection_name = 'likes', limit = 1000)
  likers.append(likes)

test1 = graph.get_connections(id = post_ids[0], connection_name = 'likes', limit = 1000)


testlist = []
for k in likers:
	test = graph.get_connections(id = '10208651780993543', connection_name = 'friends')

graph.get_object(id = 'me', fields = 'about')

10208651780993543

648249232025906
10208446361865933
# keep this handy to test the de facto limit on likes
len(likes[u'data'])
