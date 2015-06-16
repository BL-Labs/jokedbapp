from twitter import *
import os
from viccomedian_app_keys import CONSUMER_KEY, CONSUMER_SECRET

TWITTER_CREDS = 'Victorian_comedian_twitter_creds'
if not os.path.exists(TWITTER_CREDS):
  oauth_dance("Post a Joke", CONSUMER_KEY, CONSUMER_SECRET, TWITTER_CREDS)

oauth_token, oauth_secret = read_token_file(TWITTER_CREDS)

twitter = Twitter(auth=OAuth(
            oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

# Now work with Twitter
twitter.statuses.update(status='Testing... 1, 2. 1, 1, 2. Herringbone. Testing. *tap tap tap*. Is this thing on?')
