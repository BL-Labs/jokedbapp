import os
from twitter import *
from tumblrcreds import blog_url
from random import randint

# load joke starters globally
import json

with open("/home/ben/jokedb/jokedbapp/utils/joke_openers.json", "r") as x:
  LINES = json.load(x)

def twitter_imagepost(joke, filename, tags=['#victorianhumour'], tumblr_id=None, url=None):
  # try to get a twitter connection, fail otherwise:
  from viccomedian_app_keys import CONSUMER_KEY, CONSUMER_SECRET
  o_token, o_secret = read_token_file("/home/ben/jokedb/jokedbapp/utils/Victorian_comedian_twitter_creds")
  t = Twitter(auth= OAuth(o_token, o_secret, CONSUMER_KEY, CONSUMER_SECRET))

  tweet_text = LINES[randint(0,len(LINES)-1)]
  tumblr_url = blog_url + unicode(tumblr_id)
  htags = u" #".join(tags)
  title = u"\"" + joke.title + u"\""
  year = u" (" + unicode(joke.from_transcription.biblio.year) + u") "

  tweet = tweet_text + title + year + tumblr_url + htags
  spill = 125 - len(tweet)
  if spill > 0:
    tweet = tweet_text + title[:spill] + year + tumblr_url + htags

  enc_tweet = tweet.encode("utf-8")
  with open(filename, "rb") as imagefile:
    params = {"media[]": imagefile.read(), "status": enc_tweet}
    resp = t.statuses.update_with_media(**params)

  return tweet, resp

