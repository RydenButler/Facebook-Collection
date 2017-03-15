import facebook
import requests
import json

# initialize graph object
graph = facebook.GraphAPI(version='2.2')
# generate access token
my_token = graph.get_app_access_token(app_id = APP_ID, app_secret = APP_SECRET)
# pass valid access token to graph object
graph = facebook.GraphAPI(access_token = my_token, version='2.2')

user = graph.get_object('BillGates')
posts = graph.get_connections(user['id'], 'posts', limit = 100)

print json.dumps(posts, indent = 1)
len(posts['data'])

more_posts = requests.get(posts['paging']['next']).json()

while True:
	try:
		[print(post=post) for post in posts['data']]
		posts = requests.get(posts['paging']['next']).json()
	except KeyError:
		break

# need to find some automated way of getting politicians' page ids


print json.dumps(graph.get_connections(id='11052154359', connection_name='posts', limit = 100), indent = 1)






