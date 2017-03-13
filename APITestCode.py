import facebook

# Use this link to get a fresh access token:
# https://developers.facebook.com/tools/accesstoken/

graph = facebook.GraphAPI(access_token = my_token, version='2.2')
my_token = graph.get_app_access_token(app_id = APP_ID, app_secret = APP_SECRET)

post = graph.get_object(id='11052154359')
print(post['message'])

posts = graph.get_all_connections(id='11052154359', connection_name='posts')