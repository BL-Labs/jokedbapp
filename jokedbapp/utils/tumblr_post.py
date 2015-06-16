from photopost import TumblrAPIv2
from tumblrcreds import *
from datetime import datetime
def tumblr_imagepost(joke, filename, tags = [], attribution = [], url=None):
  client = TumblrAPIv2(credentials['consumer_key'], credentials['consumer_secret'], credentials['oauth_token'], credentials['oauth_token_secret']) # CACHE?
  #Creates a photoset post using several local filepaths
  date  = datetime.now()
  
  caption = "<p>" + joke.title.encode('utf-8') + "</p>"
  caption += "<p>" + joke.joketext.encode('utf-8') + "</p>"
  if attribution:
    caption += "<blockquote>"
    for line in attribution:
      caption += line[1].encode('utf-8') + "<br/>"
    caption += "</blockquote>"
  if url:
    caption += "<p><a href='{0}'>{0}</a></p>".format(url)

  post = {
        'type' : 'photo',
        'date' : date.strftime("%Y-%m-%d %H:%M:%S"),
        'data' : filename,
        'tags' : ",".join(tags),
        'caption' : caption
  }

  resp = client.createPhotoPost(blog, post)
  if 'id' in resp:
    joke.published_at = date
    joke.tumblr_id = resp['id']
  return joke
  
