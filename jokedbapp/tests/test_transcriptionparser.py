import unittest

from utils.handle_transcript import TranscriptionParser, OmekaXML

from test_data import TRANSCRIPTIONS

OMEKA_COLLECTION = "test_omeka_collection.xml"

# User, Transcription, Joke, Picture

class TestTranscriptionParse(unittest.TestCase):
  def setUp(self):
    self.TP = TranscriptionParser()

  def test_01_load_transcription(self):
    self.TP.fromstring(TRANSCRIPTIONS[0])
    self.assertEquals(self.TP.parsed(), True)
    
  def test_02_load_transcription(self):
    self.TP.fromstring(TRANSCRIPTIONS[1])
    self.assertEquals(self.TP.parsed(), True)
  
  def test_03_load_garbage(self):
    self.TP.fromstring("This is a crappy <asdasdasdas><qweqweqweqwe <!--- failed thing that doesn't look like a set of jokes")
    self.assertEquals(self.TP.parsed(), False)
  
  def test_04_joke_count(self):
    self.TP.fromstring(TRANSCRIPTIONS[0])
    self.assertEquals(len(self.TP), 12)

  def test_05_joke_plain_text(self):
    self.TP.fromstring(TRANSCRIPTIONS[0])
    if self.TP.parsed():
      joke = self.TP.joke(2)
      self.assertEquals(joke.title.strip(" "), "AGREED.")
      joke = self.TP.joke(4)
      self.assertEquals(joke.title.strip(" "), "OVER ON BUSINESS.")
      joke = self.TP.joke(8)
      self.assertEquals(joke.title.strip(" "), "A 'STOCK' ACTOR.")
      joke = self.TP.joke(9)
      self.assertEquals(joke.title.strip(" "), "\"AND A GOOD JUDGE, TOO\".")
      joke = self.TP.joke(11)
      self.assertEquals(joke.title.strip(" "), "\"O'SHEA-MEFUL")
    else:
      raise Exception

  def test_06_iterate_over_jokes(self):
    self.TP.fromstring(TRANSCRIPTIONS[0])
    for idx, joke in enumerate(self.TP):
      pass
    self.assertEquals(idx, 11)
    
  def test_07_parse_book_jokes(self):
    self.TP.fromstring(TRANSCRIPTIONS[2])
    for idx, joke in enumerate(self.TP):
      pass
    self.assertEquals(idx, 0)
    
  def test_07_parse_book_jokes(self):
    self.TP.fromstring(TRANSCRIPTIONS[2])
    joke = self.TP.jokelist[0]
    self.assertEquals(joke.title.strip(" "), "A Paradox.")
    self.assertEquals(joke.attribution.strip(" "), "Unknown")
    self.assertEquals(joke.text.strip(" "), 'Two friends were discussing that interesting event in French history, the VendeanRevolt, and the character of the Vendeanhero,Henri Larochejaquelein. "What bravefellows those poor Vendean peasants were," said one. " Yes," enjoined his friend, "but yet the greater portion of themwere cow-herds."')
    
class TestOmekaXML(unittest.TestCase):
  def setUp(self):
    self.o = OmekaXML()

  def test_01_load_xml_from_file(self):
    with open(OMEKA_COLLECTION, "r") as inp:
      self.o = OmekaXML(inp.read())

if __name__ == "__main__":
  unittest.main()


