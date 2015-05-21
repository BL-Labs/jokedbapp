from xml.etree import ElementTree as ET

def om(tag):
  return "{http://omeka.org/schemas/omeka-xml/v5}" + tag

class Parser(object):
  def __init__(self):
    self._parse_item = ItemParser()
  
  def read(self, text):
    doc = ET.fromstring(text)
    for item in doc.findall(om("item")):
      itemid, pkt = self._parse_item(item)


class ItemParser(object):
  def __init__(self):
    pass

	
