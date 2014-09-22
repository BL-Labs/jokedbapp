import cairo
import textwrap

from image_profiles import BASIC

class ICanHaz(object):
  def __init__(self, profile=BASIC):
    self.background, self.parts, self.layout = profile
    self._testsurf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
    self._testctx = cairo.Context(self._testsurf)
    self.setup_font_render(self._testctx, "DEFAULT", "DEFAULT")

  def break_text(self, text, partname):
    texts = []
    tw = self.parts[partname]['TEXTWIDTH']
    for line in text.split("\n"):
      if line:
        splitlines = textwrap.wrap(line, tw)
        if splitlines != None:
          texts.extend(splitlines)
      texts.append(u"")
    return texts

  def markup_text(self, title, text, attrib, partname):
    lines = [('TITLE', title), ('DEFAULT', "\n")]
    lines.extend([('DEFAULT', x) for x in self.break_text(text, partname)])
    lines.append(('EMPHASIS', attrib))
    return lines

  def setup_font_render(self, ctx, style, partname):
    ctx.set_source_rgba(*self.parts[partname]['FOREGROUND'])
    s = self.parts[partname]['TEXT'][style]
    ctx.select_font_face(s['font'], s['style'], s['weight'])
    ctx.set_font_size(s['size'])
    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    self.lineheight = fheight * self.parts[partname]['TEXT'][style]['LINEHEIGHT']

  def get_text_size(self, lines, partname):
    # Dry-run
    dx, dy = self.parts[partname]['MARGIN']
    max_x = 0
    total_y = dy
    for style, line in lines:
      self.setup_font_render(self._testctx, style, partname)
      lh = self.lineheight
      xbearing, ybearing, width, height, xadvance, yadvance = self._testctx.text_extents(line)
      if width > max_x:
        max_x = width
      total_y += lh
    return max_x + (dx * 2), total_y

  def get_surface(self, width, height, partname):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(width), int(height))
    ctx = cairo.Context(surf)
    # ctx.scale(width, height) # 1.0, 1.0 scale
    ctx.set_source_rgba(*self.parts[partname]['BACKGROUND'])
    ctx.paint()
    return surf, ctx

  def paint_lines_to_surface(self, lines, partname, ctx):
    ctx.move_to(*self.parts[partname]["MARGIN"])
    for idx, (style, line) in enumerate(lines):
      if line:
        self.setup_font_render(ctx, style, partname)
        ctx.show_text(line.strip("\n\t"))
      ctx.move_to(self.parts[partname]["MARGIN"][0], 
                  ((idx + 1) * self.lineheight) + self.parts[partname]["MARGIN"][1])

  def _render_lines_to_file(self, lines, partname, filename):
    # Test wd
    width, height = self.get_text_size(lines, partname)
    surf, ctx = self.get_surface(width, height, partname)
    self.paint_lines_to_surface(lines, partname, ctx)
    surf.write_to_png(filename)
