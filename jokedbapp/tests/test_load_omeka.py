import unittest

from models import *

from utils.handle_transcript import TranscriptionParser, OmekaXML, om

from test_data import TRANSCRIPTIONS

OMEKA_COLLECTION = "test_omeka_collection.xml"

# User, Transcription, Joke, Picture

class TestUserClass(unittest.TestCase):
  def setUp(self):
    self.TP = TranscriptionParser()
    self.o = OmekaXML()
    from database import init_test_db
    self.db_session = init_test_db()
    self.u = User('admin', 'admin@localhost', 'admin', 'saltypasswordhash') 
    self.db_session.add(self.u)
    self.db_session.commit()

  def test_u01_user_create_regular(self):
    u = User('ben', 'regular@localhost', 'transcriber', 'saltypasswordhash') 
    self.db_session.add(u)
    self.db_session.commit()

  def test_u02_user_create_publisher(self):
    u = User('bob', 'bob@localhost', 'publisher', 'saltypasswordhash')
    self.db_session.add(u)
    self.db_session.commit()

  def test_u03_find_an_admin(self):
    admin = User.query.filter(User.role == 'admin').first()
    self.assertEquals(admin.name, 'admin')

  def test_u04_test_is_admin(self):
    admin = User.query.filter(User.role == 'admin').first()
    self.assertEquals(admin.is_admin(), True)

  def test_u05_user_alter_email(self):
    self.u.email = 'newadminemail'
    self.db_session.add(self.u)
    self.db_session.commit()
    # now query for it
    email_match = User.query.filter(User.email == "newadminemail").first()
    self.assertEquals(email_match.name, 'admin')

  def tearDown(self):
    self.db_session.remove()

