from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship, backref

from database import Base

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
  date_harvested = Column(Date)
  by_user_id = Column(Integer, ForeignKey('users.id'))
  by_user = relationship(User, backref=backref('editor', uselist=False))
  # TODO: Add citation metadata columns

  def __init__(self, from_id=None, text=None, date_harvested=None, by_user = None):
    self.from_id = from_id
    self.text = text
    self.date_harvested = date_harvested
    self.by_user = by_user

  def __repr__(self):
    return '<Transcription: {0} -- "{1}..." by {2}>'.format(self.id, self.text[:15], self.created_by)

class Joke(Base):
  __tablename__ = 'jokes'
  id = Column(Integer, primary_key=True)
  from_transcription_id = Column(Integer, ForeignKey('transcriptions.id'))
  from_transcription = relationship(Transcription, backref=backref('transcriptions', uselist=False))
  transcription_position = Column(Integer)
  text = Column(String)
  published_at = Column(Date)
  tumblr_id = Column(String(30))
  tweet_id = Column(String(30))
  published_by_id = Column(Integer, ForeignKey('users.id'))
  published_by = relationship(User, backref=backref('published', uselist=False))
  
  def __init__(self, transcription = None, transcription_position = None, text = None, \
               published_at = None, tumblr_id = None, tweet_id = None, published_by = None):
   self.from_transcription = transcription
   self.transcription_position = transcription_position
   self.text = text 
   self.published_at = published_at
   self.tumblr_id = tumblr_id
   self.tweet_id = tweet_id
   self.published_by = published_by 

