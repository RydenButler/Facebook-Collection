import facebook
from Secrets import *

# Connect to Graph API
graph = facebook.GraphAPI(version='2.7')
# Generate access token
my_token = graph.get_app_access_token(app_id = APP_ID, app_secret = APP_SECRET)
# Pass valid access token to graph object
graph = facebook.GraphAPI(access_token = my_token, version='2.7')

# Store page id
check_page = __FBID__ #'1103557292'


#Get page data
page_data = graph.get_object(check_page)
# Get all posts
posts = [i for i in graph.get_all_connections(id=page_data['id'], connection_name='posts')]
# Get all likes; insert desired post number if necessary
likes = [j for j in graph.get_all_connections(id=posts[__INSERT_POST_NUMBER_HERE__]['id'], connection_name='likes')]

# Get specific post
post = graph.get_connections(id=page_data['id'], connection_name='posts')
# Get specific likes
like = graph.get_connections(id=post[__INSERT_POST_NUMBER_HERE__], connection_name='likes')


# Push notification to specific user
graph.put_object(parent_object = '10212718692468955', 
	connection_name = 'notifications',
	template = "This is a notification!"
	)



#import facepy
#token_app=facepy.utils.get_application_access_token(application_id=int(APP_ID),application_secret_key=APP_SECRET) 
#graph = facepy.GraphAPI()
#graph.post(path = '1103557292/notifications', template='Test',access_token=token_app)




     