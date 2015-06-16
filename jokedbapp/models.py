from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, backref

from database import Base

from datetime import datetime

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  name = Column(String(50), unique=True)
  email = Column(String(120), unique=True)
  pw_hash = Column(String)
  role = Column(Enum('admin','transcriber', 'publisher', name='role_types'))
  transcriptions = relationship("Transcription", backref="edited", cascade="delete")
  biblio_records = relationship("Biblio", backref="creator", cascade="delete")
  joke_records = relationship("Joke", backref="publisher", cascade="delete")

  def __init__(self, name=None, email=None, role='transcriber', pw_hash = pw_hash):
    self.name = name
    self.email = email
    self.role = role
    self.pw_hash = pw_hash

  def is_admin(self):
    if self.role == 'admin':
      return True
    else:
      return False

  def __repr__(self):
    return '<User {0}, role={1}>'.format(self.name, self.role)

class Biblio(Base):
  __tablename__ = 'biblio'
  id = Column(Integer, primary_key=True)
  title = Column(String(70))
  date = Column(String(20))
  year = Column(Integer)
  author = Column(String(30))
  editor = Column(String(30))
  publisher = Column(String(30))
  city = Column(String(30))
  country = Column(String(30))
  gale = Column(String(30))
  blshelfmark = Column(String(30))
  shownby = Column(String(200))  # URL direct link perhaps?
  rights = Column(String(60))
  rightsholder= Column(String(60))
  citation = Column(String)
  itemtype = Column(Enum('periodical', 'book', name='pub_type'))
  periodical_freq = Column(Enum('weekly', 'daily', 'fortnightly', 'monthly', 'annually', "NA", name='publication_rate'))
  created_at = Column(DateTime)
  creator_id = Column(Integer, ForeignKey('users.id'))
  #creator = relationship(User, backref=backref('biblio_author', uselist=True))
  transcription_sections = relationship("Transcription", backref="biblio")
  
  def __init__(self, title=None, date=None, year=0, author=None, editor=None, publisher=None, city=None, \
                     country=None, gale=None, blshelfmark=None, shownby=None, rights=None, \
                     rightsholder=None, itemtype=None, periodical_freq="NA", citation=None, record_creator = None):
    self.title = title
    self.date = date
    self.year = year
    self.author = author
    self.editor = editor
    self.publisher = publisher
    self.city = city
    self.country = country
    self.gale = gale
    self.blshelfmark = blshelfmark
    self.shownby = shownby
    self.rights = rights
    self.rightsholder = rightsholder
    self.itemtype = itemtype
    self.periodical_freq = periodical_freq
    self.citation = citation
    #self.creator = record_creator
    if record_creator:
      self.creator_id = record_creator.id
    self.created_at = datetime.now()

  def __repl__(self):
    return '<Biblio {0}({1}) shelfmark:{2}>'.format(self.title, self.date, self.blshelfmark)
  

class Transcription(Base):
  __tablename__ = 'transcriptions'
  id = Column(Integer, primary_key=True)
  from_id = Column(Integer)
  raw = Column(String)
  text = Column(String)
  date_harvested = Column(DateTime)
  parsed = Column(Integer)
  created_at = Column(DateTime)
  edited_id = Column(Integer, ForeignKey('users.id'))
  #by_user = relationship(User, backref=backref('editor', uselist=True))
  # TODO: Add citation metadata columns
  pagestart = Column(Integer)
  pageend = Column(Integer)
  volume = Column(String(20))
  article_title = Column(String(70))
  biblio_id = Column(Integer, ForeignKey('biblio.id'))  
  #biblio  = relationship(Biblio, backref=backref('transcriptions', uselist=True))
  joke_children = relationship("Joke", backref="from_transcription")

  def __init__(self, from_id=None, text=None, date_harvested=None, by_user = None, raw = None, parsed = 0, \
                     biblio = None, article_title = None, volume = None, pagestart = 0, pageend = 0):
    self.from_id = from_id
    self.text = text
    self.date_harvested = date_harvested
    #self.by_user = by_user

    if by_user:
      self.edited_id = by_user.id
    else:
      self.edited_id = None

    if biblio:
      self.biblio_id = biblio.id
    else:
      self.biblio_id = None

    self.raw = raw
    self.parsed = parsed
    self.created_at = datetime.now()
    self.article_title = article_title
    self.volume = volume
    self.pagestart = pagestart
    self.pageend = pageend    

  def __repr__(self):
    if self.text:
      return '<Transcription: {0} -- "{1}..." from {3}({4}) by {2}>'.format(self.id, self.text[:15], self.edited, self.article_title, self.biblio.date)
    return '<Transcription: {0} -- from {2}({3}) by {1}>'.format(self.id, self.edited, self.article_title, self.biblio.date)

class Joke(Base):
  __tablename__ = 'jokes'
  id = Column(Integer, primary_key=True)
  from_transcription_id = Column(Integer, ForeignKey('transcriptions.id'))
  #from_transcription = relationship(Transcription, backref=backref('transcription_src', uselist=False))
  transcription_position = Column(Integer)
  text = Column(String)
  title = Column(String)
  tumblr_id = Column(String)
  tweet_id = Column(String)
  attribution = Column(String)
  joketext = Column(String)
  #image_id = Column(Integer, ForeignKey('pictures.id'))
  #image = relationship(Picture, backref=backref('images', uselist=False))
  created_at = Column(DateTime, nullable=False)
  published_at = Column(DateTime)
  publisher_id = Column(Integer, ForeignKey('users.id'))
  #published_by = relationship(User, backref=backref('publisher', uselist=True))
  
  def __init__(self, transcription = None, transcription_position = None, text = None, \
               published_at = None, tumblr_id = None, tweet_id = None, published_by = None, \
               title = None, attribution = None, joketext = None):
    #self.from_transcription = transcription
    if transcription != None:
      self.from_transcription_id = transcription.id
    self.transcription_position = transcription_position
    self.text = text 
    self.title = title 
    self.attribution = attribution 
    self.joketext = joketext
    self.created_at = datetime.now()
    self.published_at = published_at
    if published_by:
      #self.published_by = published_by
      self.published_by_id = published_by.id
    self.tweet_id = tweet_id
    self.tumblr_id = tumblr_id

  def __repr__(self):
    if self.tumblr_id:
      return '<Joke: {0} -- "{1}..." On tumblr: "{2}">'.format(self.id, self.text[:15], self.tumblr_id)
    return '<Joke: {0} -- "{1}..." -- not published on web>'.format(self.id, self.text[:15])

class Picture(Base):
  __tablename__ = 'pictures'
  id = Column(Integer, primary_key = True)
  created_at = Column(DateTime, nullable=False)
  rendered_at = Column(DateTime, nullable=False)
  status = Column(Integer)    # 0 - in progress/queued, 1 - ready to view, 2 - uploaded remotely
  path = Column(String(50))
  tumblr_id = Column(String(30))
  tweet_id = Column(String(30))
  profile = Column(String(20))
  joke_id = Column(Integer, ForeignKey('jokes.id'))
  joke = relationship(Joke, backref=backref('renderings'))
  published_at = Column(DateTime)
  published_by_id = Column(Integer, ForeignKey('users.id'))
  published_by = relationship(User, backref=backref('published', uselist=True))
  
  def __init__(self, status, joke, \
               tumblr_id = None, tweet_id = None, published_by = None, published_at = None):
    self.status = status
    self.joke = joke
    self.tumblr_id = tumblr_id
    self.tweet_id = tweet_id
    self.joke_id = joke.id
    self.created_at = datetime.now()
    self.published_at = published_at
    self.published_by = published_by 
    self.published_by_id = published_by_id
  
  def __repr__(self):
    return '<Picture: {0}, status:{1} -- from joke id {2}>'.format(self.id, self.status, self.joke_id)

