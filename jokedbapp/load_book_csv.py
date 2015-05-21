from utils.handle_csv import BookJokesCSV
from utils.handle_transcript import TranscriptionParser

from models import *
from database import init_db

import sys, os

DEFAULT = '/home/ben/bookjokes.csv'

if __name__ == "__main__":
  
  if len(sys.argv) > 1:
    filename = sys.argv[1]
  else:
    filename = DEFAULT

  if not os.path.exists(filename):
    print("Cannot find file '{0}'...?".format(filename))
    sys.exit(2)

  print("Loading new jokes from '{0}'".format(filename))

  dbsession = init_db()

  bookjokes = BookJokesCSV(filename)
  page_list = {}

  # get Admin user 'ben'
  u = User.query.filter(User.name == "ben").first()

  def create_or_get_bib_record(row):
    bib = Biblio.query.filter(Biblio.title == row['title'])            \
                      .filter(Biblio.date == row['date']).first()
    if bib != None:
      return bib
    else:
      print("Found no matching Biblio record")
      try:
        year = int(row['year'])
      except ValueError as e:
        year = None
      b = Biblio(title=row['title'], date = row['date'], year = year, editor = row['editor'], \
                 country = row['country'], city = row['city'], blshelfmark = row['blshelfmark'], \
                 rights = 'Public Domain', rightsholder = "From the holdings of the British Library", \
                 itemtype = 'book', record_creator = u)
      dbsession.add(b)
      dbsession.commit()
      return b

  def create_or_get_Transcription(row):
    b = create_or_get_bib_record(row)
    transc = Transcription.query.filter(Transcription.biblio == b)                   \
                                .filter(Transcription.pagestart == row['pagestart'])           \
                                .filter(Transcription.pageend == row['pageend']).first()
    if transc != None:
      print("Found existing Transcription record id {0} - reusing".format(transc.id))
      return transc
    else:
      t = Transcription(by_user = u, parsed = 1, biblio = b, pagestart = row['pagestart'], pageend = row['pageend'])
      dbsession.add(t)
      dbsession.commit()
      return t

  def get_page_position(tid, row):
    if page_list.get(tid) != None:
      page_list[tid] += 1
    else:
      page_list[tid] = 1

    return page_list[tid]
      

  for idx, item in enumerate(bookjokes):
    # get/create bib records
    t = create_or_get_Transcription(item)
    pos = get_page_position(t.id, item)
    TP = TranscriptionParser()
    TP.fromstring(item['joke'])
    joke = TP.jokelist[0]
    j = Joke(transcription = t, text = item['joke'], transcription_position = pos, title=joke.title, attribution=joke.attribution, joketext=joke.text)
    dbsession.add(j)
    dbsession.commit()
    print("Added Joke #{0} from {1}({2})".format(str(idx+1), item['title'][:30], item['year']))
  dbsession.close()
