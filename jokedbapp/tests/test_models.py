import unittest

from models import *

# User, Transcription, Joke, Picture

class TestUserClass(unittest.TestCase):
  def setUp(self):
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

class TestBiblioClass(unittest.TestCase):
  def setUp(self):
    from database import init_test_db
    self.db_session = init_test_db()
    self.biblio = Biblio("Lloyd's Weekly Newspaper (London, England), Sunday, December 27, 1891", date="27/12/1891", \
                         gale="Y3206278766", itemtype='periodical', periodical_freq="weekly", year=1891)
    self.biblio2 = Biblio("Lloyd's Not so Weekly Newspaper (London, England)", date="27/12/1899", \
                         gale="someothernumber", itemtype='periodical', periodical_freq="daily", year=1899)
    self.db_session.add(self.biblio)
    self.db_session.add(self.biblio2)
    self.db_session.commit()

  def test_b01_make_sure_setup_works(self):
    pass
    
  def test_b02_find_a_weekly(self):
    # there's only one...
    weekly = Biblio.query.filter(Biblio.periodical_freq == "weekly").first()
    self.assertEquals(weekly.gale, "Y3206278766")

  def tearDown(self):
    self.db_session.remove()

class TestTranscriptionClass(unittest.TestCase):
  def setUp(self):
    from database import init_test_db
    self.db_session = init_test_db()
    self.u = User('admin', 'admin@localhost', 'admin', 'saltypasswordhash')
    self.db_session.add(self.u)
    self.db_session.commit()

  def test_t01_create_basic_transcription(self):
    # from a fake Omeka id of '42'
    from datetime import datetime
    t = Transcription(42, "<j>I spilled Spot remover on my dog. Now he's gone.</j>", datetime.now(), self.u)
    self.db_session.add(t)
    self.db_session.commit()

  def test_t02_create_basic_transcription_nulls(self):
    t = Transcription(42, "<j>I went to a general store, but they wouldn't let me buy anything specific.</j>", None, self.u)
    self.db_session.add(t)
    self.db_session.commit()

  def test_t03_create_basic_transcription_null_user(self):
    t = Transcription(42, "<j>I have a hobby. I have the world's largest collection of sea shells. I keep it scattered on beaches all over the world. Maybe you've seen some of it.</j>")
    self.db_session.add(t)
    self.db_session.commit()

  def test_t04_get_user_from_transcription(self):
    t = Transcription(45, "<j>I just got skylights put in my place. The people who live above me are furious.</j>", by_user=self.u)
    self.db_session.add(t)
    self.db_session.commit()
    # Now query for it and get the email of the submitter
    trans = Transcription.query.filter(Transcription.from_id == 45).first()
    self.assertEquals(trans.edited.name, 'admin')

  def tearDown(self):
    self.db_session.remove()

if __name__ == "__main__":
  unittest.main()


