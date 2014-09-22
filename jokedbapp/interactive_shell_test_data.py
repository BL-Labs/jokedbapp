from models import *
import sys

from test_data import TRANSCRIPTIONS, USERDATA

def load_db(db_session):
  from datetime import datetime
  # load a db session with the data
  print("Creating {0} users".format(len(USERDATA)))
  # Users:
  users = []
  for item in USERDATA:
    users.append(User(*item))
    db_session.add(users[-1])
  db_session.commit()

  # example transcription data
  transcriptions = []
  for idx, item in enumerate(TRANSCRIPTIONS):
    transcriptions.append(Transcription(idx, item, datetime.now(), users[idx]))
    db_session.add(transcriptions[-1])
  db_session.commit()


if __name__ == "__main__":
  if sys.flags.interactive:
    from database import init_test_db
    db_session = init_test_db()
    load_db(db_session)
    print("All models have been imported, and 'db_session' is the db entrypoint.")
  else:
    print("This will load the data into an inmemory SQLite db. Please open this with an interactive shell.")
    print("Eg 'python -i test_load_test_data.py'")
    print("Quitting.")
