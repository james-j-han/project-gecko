from requests_oauthlib import OAuth1Session

import requests
import base64
import json

consumer_key = 'KJFXNeCaQRrUVxIO4iwp1PZNT'
consumer_secret = 'ayfEzILYnpDtw229msenHJqhF4AybbuwwuNqX7nq5xK3e881Ge'

# params = {
# 	'ids': '1138505981460193280',
# 	'tweet.fields': 'created_at'
# }

params = {
	'screen_name': 'cashapp',
	'count': 6
}

# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
fetch_response = oauth.fetch_request_token(request_token_url)
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')
print("Got OAuth token: %s" % resource_owner_key)

# # Get authorization
base_authorization_url = 'https://api.twitter.com/oauth/authorize'
authorization_url = oauth.authorization_url(base_authorization_url)
print('Please go here and authorize: %s' % authorization_url)
verifier = input('Paste the PIN here: ')

# # Get the access token
access_token_url = 'https://api.twitter.com/oauth/access_token'
oauth = OAuth1Session(consumer_key,
                     client_secret=consumer_secret,
                     resource_owner_key=resource_owner_key,
                     resource_owner_secret=resource_owner_secret,
                     verifier=verifier)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens['oauth_token']
access_token_secret = oauth_tokens['oauth_token_secret']

# Make the request
oauth = OAuth1Session(consumer_key,
                       client_secret=consumer_secret,
                       resource_owner_key=access_token,
                       resource_owner_secret=access_token_secret)
url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
r = oauth.get(url, params = params)
# print("Response status: %s" % response.status_code)
# print("Body: %s" % response.text)
print(r)
data = r.json()

for tweet in data:
	text = tweet['text']
	if 'twitch' in text.lower():
		print(text)