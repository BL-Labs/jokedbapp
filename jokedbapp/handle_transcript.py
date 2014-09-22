from bs4 import BeautifulSoup
import re

class JokeInterchange(object):
  def __init__(self, text, title = u"", attribution = u"", parsed = False):
    self.title = title
    self.text = text
    self.attribution = attribution
    self.parsed = True

class TranscriptionParser(object):
  def __init__(self):
    self.parsed_correctly = False
    self.jokelist = []
    self.inputtext = u""
    self.p = "\s?<{0}>(.*?)</{0}>\s?"
    self.basic = "\s?(<t>(?P<title>.*?)</t>)?\s?(?P<text>.*?)(<a>(?P<attribution>.*?)</a>\s?)?"

  def _parse(self):
    if not self.inputtext:
      return

    jokes = re.findall(self.p.format("j"), self.inputtext, re.MULTILINE|re.DOTALL)
    if jokes != None:
      for joke in jokes:
        try:
          parsed = re.match(self.basic, joke, re.MULTILINE|re.DOTALL)
          if parsed != None:
            data = parsed.groupdict()
            title, attrib = None, None
            if data.get("title"):
              title = data['title']

            if data.get("attribution"):
              attrib = parsed.group('attribution')

            if title == None and attrib == None:
              text = joke
            else:
              text = data['text']

            self.jokelist.append(JokeInterchange(text, title=title, attribution = attrib, parsed = True))
          else:
            self.jokelist.append(JokeInterchange(joke))
        except IndexError as e:
          # failed to parse it
          self.jokelist.append(JokeInterchange(joke))
    if len(self.jokelist) > 0:
      self.parsed_correctly = True

  def parsed(self):
    return self.parsed_correctly

  def __len__(self):
    return len(self.jokelist)

  def __iter__(self):
    if len(self.jokelist) > 0:
      def iter(jokelist):
        for item in jokelist:
          yield item
      return iter(self.jokelist)

  def joke(self, index):
    if index < len(self.jokelist) and index > -1:
      return self.jokelist[index]
    else:
      raise IndexError

  def fromstring(self, inputtext):
    self.inputtext = inputtext
    self._parse()

