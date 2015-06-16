from utils.handle_transcript import TranscriptionParser, OmekaXML

from models import *
from database import init_db

import sys, os

DEFAULT = 'omeka.xml'

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

  # get Admin user 'ben'
  u = User.query.filter(User.name == "ben").first()

  def create_or_get_bib_record(row):
    bib = Biblio.query.filter(Biblio.title == row['periodical_title'])            \
                      .filter(Biblio.date == row['date']).first()
    if bib != None:
      return bib
    else:
      print("Found no matching Biblio record")
      try:
        year = int(row['year'])
      except ValueError as e:
        year = None
      b = Biblio(title=row['periodical_title'], date = row['date'], year = year, \
                 gale = row['gale'], periodical_freq = row['periodical_freq'], itemtype = 'periodical', \
                 citation = row['citation'], record_creator = u)
      dbsession.add(b)
      dbsession.commit()
      return b

  def create_or_get_Transcription(row):
    b = create_or_get_bib_record(row)
    transc = Transcription.query.filter(Transcription.biblio == b)                   \
                                .filter(Transcription.article_title == row['article_title']).first()
    if transc != None:
      print("Found existing Transcription record id {0} - reusing".format(transc.id))
      return transc
    else:
      t = Transcription(by_user = u, parsed = 1, biblio = b, article_title = row['article_title'], \
                         pagestart = row['page'], raw = row['raw'])
      dbsession.add(t)
      dbsession.commit()
      return t

  with open(filename, "r") as inp:
    o = OmekaXML(inp.read())
    o.parse()
    # get/create bib records
  for idx, item in o.metadata.iteritems():
    t = create_or_get_Transcription(item)
  dbsession.close()
