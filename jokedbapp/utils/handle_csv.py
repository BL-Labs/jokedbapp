import csv

"""
raw dict csv:
{'Publisher': 'Ballantine Press,BALLANTINE,HANSON AND CO.', 'Page Number End (Original)': 'B', 'Book Title': 'The Book of Humour, Wit & Wisdom. A manual of table-talk. [By L. C. Gent?]]', 'Joke': 'Two naval officers were disputing as to the importance\nof Lord Nelson\'s victories. They wereunable\nto agree in opinion, when one of them appealing to the\nother said, " At all events there can be nodoubt which\nof his Lordship\'s victories yielded the least important\nresults." " " Which do you mean?" said the other. "Why of course from its name," was the rejoinder, the victory of the Nihil."', 'Page Number Start (Original)': 'B', 'City': 'London,Edinburgh', 'Shelf Mark': 'British Library HMNTS 11609.f.10.', 'Page Number Start (PDF)': '13', 'Review for content': '', 'Country': 'England,Scotland', 'Joke Atttribution': 'Unknown', 'Date': '1880', 'Joke Title': 'The Battle of the Nile.', 'Book Author / Editor': 'GENT, L. C.', 'Page Number End (PDF)': '13'}
"""

import re

class BookJokesCSV(object):
  def __init__(self, localfile):
    self.csvfile = localfile
    self.rownum = 0
    self._filehandle = None
    self._rows = None

  def __iter__(self):
    return self

  def _openfile(self):
    if self._filehandle != None:
      # attempting a close action to be safe
      try:
        self._filehandle.close()
      except AttributeError as e:
        pass

    self._filehandle = open(self.csvfile, "r")
    self._rows = csv.DictReader(self._filehandle, dialect="excel")    
  
  def parse_line(self, row):
    text = u" ".join( row['Joke'].decode("cp1250").split("\n\r"))
    return {'joke': u"<j> <t>{0}</t> {1} <a> {2} </a> </j>".format(row['Joke Title'].decode("cp1250"), text, row['Joke Atttribution'].decode("cp1250")),
            'title': row['Book Title'].decode("cp1250"),
            'editor': row['Book Author / Editor'].decode("cp1250"),
            'year': row['Date'].decode("cp1250"),
            'date': row['Date'].decode("cp1250"),
            'publisher': row['Publisher'].decode("cp1250"),
            'pagestart': row['Page Number Start (PDF)'].decode("cp1250"),
            'pageend': row['Page Number End (PDF)'].decode("cp1250"),
            'originalpagestart': row['Page Number Start (Original)'].decode("cp1250"),
            'originalpageend': row['Page Number End (Original)'].decode("cp1250"),
            'city': row['City'].decode("cp1250"),
            'country': row['Country'].decode("cp1250"),
            'blshelfmark': row['Shelf Mark'].decode("cp1250"),}
            
  def next(self):
    if self._filehandle == None:
      self._openfile()
    try:
      row = self._rows.next()
    except StopIteration as e:
      # should close file and propagate the exception
      self._filehandle.close()
      self._rows = None
      raise StopIteration
    return self.parse_line(row)
