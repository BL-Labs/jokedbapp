import cairo
import textwrap
from random import randint
from image_profiles import BASICV as BASIC

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
    return texts

  def markup_text(self, title, text, attrib, partname):
    lines = []
    lines.extend([('TITLE', x) for x in self.break_text(title, partname)])
    lines.extend([('DEFAULT', x) for x in self.break_text(text, partname)])
    #lines.extend([('DEFAULT', "\n"), ('EMPHASIS', attrib)])
    lines.append(("DEFAULT_SMALL", ""))
    return lines

  def markup_attribution_box(self, title, date, page, column_title=None, add_tumblr = True, partname='DEFAULT', source_attrib=None):
    # FIXME: wordwrap may be needed!
    lines = [('BOLD_SMALL', u"From:")]
    lines.extend([('BOLD_SMALL', x) for x in self.break_text(title, partname)])
    if column_title:
      lines.append(('DEFAULT_SMALL', u"Column Title: '{0}'".format(column_title)))
    lines.append(('DEFAULT_SMALL', u"Date: {0}".format(date)))
    lines.append(('DEFAULT_SMALL', u"Page(s): {0}".format(page)))
    if source_attrib:
      lines.append(('DEFAULT_SMALL', u"Attribution: {0}".format(source_attrib)))
    if add_tumblr:
      lines.append(('BOLD_SMALL', "victorianhumour.tumblr.com // @victorianhumour"))
    lines.append(("DEFAULT_SMALL", ""))
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
    # Add margins
    return max_x + (dx * 2), total_y + dy

  def get_surface(self, width, height, partname):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(width), int(height))
    ctx = cairo.Context(surf)
    # ctx.scale(width, height) # 1.0, 1.0 scale
    ctx.set_source_rgba(*self.parts[partname]['BACKGROUND'])
    ctx.paint()
    return surf, ctx

  def paint_lines_to_surface(self, lines, partname, ctx, vert_offset=None, true_width = None, true_height = None):
    # Get background
    width, height = self.get_text_size(lines, partname)

    if true_width:
      width = true_width
    if true_height:
      height = true_height

    if vert_offset and not true_height:
      ctx.rectangle(0,vert_offset,width, height + vert_offset+2)
    else:
      ctx.rectangle(0,0,width, height)
    ctx.set_source_rgba(*self.parts[partname]['BACKGROUND'])
    ctx.fill()
    
    style, line = lines[0]
    self.setup_font_render(ctx, style, partname)
    l,t = self.parts[partname]["MARGIN"]
    if vert_offset:
      ctx.move_to(l, t + vert_offset + (self.lineheight))
    else:
      vert_offset = 0
      ctx.move_to(l, t + (self.lineheight))
    
    vcursor = t + vert_offset + (self.lineheight)

    for idx, (style, line) in enumerate(lines):
      if line != "":
        self.setup_font_render(ctx, style, partname)
        ctx.show_text(line.strip("\n\t"))
      vcursor += self.lineheight
      ctx.move_to(self.parts[partname]["MARGIN"][0], vcursor)
    return vcursor

  def _render_lines_to_file(self, lines, partname, filename):
    # Test wd
    width, height = self.get_text_size(lines, partname)
    surf, ctx = self.get_surface(width, height, partname)
    self.paint_lines_to_surface(lines, partname, ctx)
    surf.write_to_png(filename)

  # Hard code basics
  def render_basic(self, lines, attribution_lines, filename):
    twidth, theight = self.get_text_size(lines, 'DEFAULT')
    awidth, aheight = self.get_text_size(attribution_lines, 'ATTRIB')
    #Use the widest
    if twidth > awidth:
      width = twidth
    else:
      width = awidth

    #Use both heights
    height = aheight + theight

    surf, ctx = self.get_surface(width, height, "DEFAULT")
    voffset = self.paint_lines_to_surface(lines, "DEFAULT", ctx)
    self.paint_lines_to_surface(attribution_lines, "ATTRIB", ctx, vert_offset = voffset, true_width=width)
    surf.write_to_png(filename)

  def paint_img_to_surface(self, imgsurf, ctx, x, y, w=None,h=None, partname="IMAGE"):
    ctx.move_to(0,0)
    if w and h:
      ctx.rectangle(x,y,w,h)
      ctx.set_source_rgba(*self.parts[partname]['BACKGROUND'])
      ctx.fill()
    
    ctx.rectangle(x,y,imgsurf.get_width(),imgsurf.get_height())
    ctx.set_source_surface(imgsurf,x,y)
    ctx.move_to(x,y)
    ctx.fill()

  # Hard code basics
  def render_basic_with_image(self, lines, attribution_lines, filename, jokeid=None, attribution=None):
    twidth, theight = self.get_text_size(lines, 'DEFAULT')
    awidth, aheight = self.get_text_size(attribution_lines, 'ATTRIB')

    if jokeid:
      # get random jokester based on Joke ID:
      jokester = self.parts['IMAGE']['IMAGES'][jokeid % len(self.parts['IMAGE']['IMAGES'])]
    else:
      #random
      jokester = self.parts['IMAGE']['IMAGES'][randint(0, len(self.parts['IMAGE']['IMAGES'])-1)]

    imgsurf = cairo.ImageSurface.create_from_png(jokester)
    imgwidth, imgheight = imgsurf.get_width(), imgsurf.get_height()

    #Use the widest
    if twidth > awidth:
      width = twidth
    else:
      width = awidth

    if jokester:
      width += imgwidth   #add width of image

    if imgheight > theight:
      height = aheight + imgheight
      topheight = imgheight
      initialoffset = imgheight - theight
      imgoffset = 0
    else:
      height = aheight + theight
      topheight = theight
      initialoffset = 0
      imgoffset = theight - imgheight

    surf, ctx = self.get_surface(width, height, "IMAGE")
    voffset = self.paint_lines_to_surface(lines, "DEFAULT", ctx, vert_offset = initialoffset, true_height = topheight)
    self.paint_lines_to_surface(attribution_lines, "ATTRIB", ctx, vert_offset = voffset, true_width=width)
    self.paint_img_to_surface(imgsurf, ctx, x = twidth, y=imgoffset, w=imgwidth, h=topheight)
    surf.write_to_png(filename)

  def render_basic_vertical(self, lines, attribution_lines, filename, jokeid=None):
    twidth, theight = self.get_text_size(lines, 'DEFAULT')
    awidth, aheight = self.get_text_size(attribution_lines, 'ATTRIB')

    if jokeid:
      # get random jokester based on Joke ID:
      jokester = self.parts['IMAGE']['IMAGES'][jokeid % len(self.parts['IMAGE']['IMAGES'])]
    else:
      #random
      jokester = self.parts['IMAGE']['IMAGES'][randint(0, len(self.parts['IMAGE']['IMAGES'])-1)]

    imgsurf = cairo.ImageSurface.create_from_png(jokester)
    imgwidth, imgheight = imgsurf.get_width(), imgsurf.get_height()

    # vertical stack 
    height = theight + imgheight + aheight
    
    # force width to be image width
    width = imgwidth

    surf, ctx = self.get_surface(width, height, "IMAGE")
    voffset = self.paint_lines_to_surface(lines, "DEFAULT", ctx, vert_offset = 0, true_width=width)
    self.paint_img_to_surface(imgsurf, ctx, x = 0, y=theight, w=imgwidth, h=imgheight)
    self.paint_lines_to_surface(attribution_lines, "ATTRIB", ctx, vert_offset = theight + imgheight, true_width=width)
    surf.write_to_png(filename)
