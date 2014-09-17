from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from database import Base

from datetime import datetime

ADMINROLE = 0
TRANSCRIBERROLE = 1
PUBLISHERROLE = 2

MAPPING = {0: "admin", 1:"Transcriber", 2:"Publisher"}

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  name = Column(String(50), unique=True)
  email = Column(String(120), unique=True)
  pw_hash = Column(String)
  role = Column(Integer)

  def __init__(self, name=None, email=None, role=TRANSCRIBERROLE, pw_hash = pw_hash):
    self.name = name
    self.email = email
    self.role = role
    self.pw_hash = pw_hash

  def is_admin(self):
    if self.role == 0:
      return True
    else:
      return False

  def __repr__(self):
    return '<User {0}, role={1}>'.format(self.name, MAPPING[self.role])

class Transcription(Base):
  __tablename__ = 'transcriptions'
  id = Column(Integer, primary_key=True)
  from_id = Column(Integer)
  text = Column(String)
  date_harvested = Column(DateTime)
  created_at = Column(DateTime)
  by_user_id = Column(Integer, ForeignKey('users.id'))
  by_user = relationship(User, backref=backref('editor', uselist=True))
  # TODO: Add citation metadata columns

  def __init__(self, from_id=None, text=None, date_harvested=None, by_user = None):
    self.from_id = from_id
    self.text = text
    self.date_harvested = date_harvested
    self.by_user = by_user
    self.by_user_id = by_user.id
    self.created_at = datetime.now()

  def __repr__(self):
    return '<Transcription: {0} -- "{1}..." by {2}>'.format(self.id, self.text[:15], self.by_user)

class Joke(Base):
  __tablename__ = 'jokes'
  id = Column(Integer, primary_key=True)
  from_transcription_id = Column(Integer, ForeignKey('transcriptions.id'))
  from_transcription = relationship(Transcription, backref=backref('transcription_src', uselist=False))
  transcription_position = Column(Integer)
  text = Column(String)
  #image_id = Column(Integer, ForeignKey('pictures.id'))
  #image = relationship(Picture, backref=backref('images', uselist=False))
  created_at = Column(DateTime, nullable=False)
  
  def __init__(self, transcription = None, transcription_position = None, text = None, \
               published_at = None, tumblr_id = None, tweet_id = None, published_by = None):
    self.from_transcription = transcription
    self.transcription_position = transcription_position
    self.text = text 
    self.created_at = datetime.now()

  def __repr__(self):
    return '<Joke: {0} -- "{1}..." by "{2}">'.format(self.id, self.text[:15], self.published_by)

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

