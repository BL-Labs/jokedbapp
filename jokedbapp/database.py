from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dbconfig import DATABASE_PATH

Base = declarative_base()

def init_db():
  # Use a local SQLite for now.
  engine = create_engine('sqlite:///{0}'.format(DATABASE_PATH), convert_unicode=True)
  db_session = scoped_session(sessionmaker(autocommit=False,
                                           autoflush=False,
                                           bind=engine))
  import models
  Base.query = db_session.query_property()
  Base.metadata.create_all(bind=engine)
  return db_session

def init_test_db():
  # Use a local SQLite for now.
  engine = create_engine('sqlite:///:memory:'.format(DATABASE_PATH), convert_unicode=True)
  db_session = scoped_session(sessionmaker(autocommit=False,
                                           autoflush=False,
                                           bind=engine))
  import models
  Base.query = db_session.query_property()
  Base.metadata.create_all(bind=engine)
  return db_session

