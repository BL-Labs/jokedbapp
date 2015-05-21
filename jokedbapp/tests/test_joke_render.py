import unittest

from render_joke import ICanHaz

from test_data import JOKES

class TestJokeClass(unittest.TestCase):
  def setUp(self):
    self.renderer = ICanHaz()

  def test_01_init(self):
    self.assertNotEquals(self.renderer, None)
  
  def test_02_break_text_DEFAULT_JOKE1(self):
    # BASIC profile -> DEFAULT
    title, text, attrib = JOKES[0]
    texts = self.renderer.break_text(text, "DEFAULT")
    for line in texts:
      self.assertTrue(len(line) < self.renderer.parts['DEFAULT']['TEXTWIDTH'] + 1)

  def test_03_mark_up_text_JOKE1(self):
    title, text, attrib = JOKES[0]
    lines = self.renderer.markup_text(title, text, attrib, "DEFAULT")
    self.assertEquals(lines[0][0], "TITLE")
    self.assertEquals(lines[0][1], title)

    self.assertEquals(lines[-1][0], "EMPHASIS")
    self.assertEquals(lines[-1][1], attrib)
    
  def test_04_get_size_JOKE1(self):
    title, text, attrib = JOKES[0]
    lines = self.renderer.markup_text(title, text, attrib, "DEFAULT")
    x,y = self.renderer.get_text_size(lines, "DEFAULT")
    self.assertNotEquals(x, 0)
    self.assertNotEquals(y, 0)
    
  def test_05_write_to_test_png_JOKE1(self):
    title, text, attrib = JOKES[0]
    lines = self.renderer.markup_text(title, text, attrib, "DEFAULT")
    self.renderer._render_lines_to_file(lines, "DEFAULT", "/tmp/test_joke1.png")

  def test_06_write_to_test_png_JOKE2(self):
    title, text, attrib = JOKES[1]
    lines = self.renderer.markup_text(title, text, attrib, "DEFAULT")
    self.renderer._render_lines_to_file(lines, "DEFAULT", "/tmp/test_joke2.png")

  def test_07_write_to_test_png_vertical_JOKE1(self):
    title, text, attrib = JOKES[0]
    lines = self.renderer.markup_text(title, text, attrib, "DEFAULT")
    attriblines = self.renderer.markup_attribution_box(title, "1889", "12", "Lloyds funnies", partname = "ATTRIB")
    self.renderer.render_basic_vertical(lines, attriblines, "/tmp/test_joke_v1.png")

  def test_08_write_to_test_png_vertical_JOKE2(self):
    title, text, attrib = JOKES[1]
    lines = self.renderer.markup_text(title, text, attrib, "DEFAULT")
    attriblines = self.renderer.markup_attribution_box(title, "1889", "12", "Lloyds funnies", partname = "ATTRIB")
    self.renderer.render_basic_vertical(lines, attriblines, "/tmp/test_joke_v2.png")


if __name__ == "__main__":
  unittest.main()
