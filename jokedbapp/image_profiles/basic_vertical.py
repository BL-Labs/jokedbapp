import cairo

DEFAULT = {'font': 'American Typewriter', 'size':32.0, 'style': cairo.FONT_SLANT_NORMAL, 'weight': cairo.FONT_WEIGHT_NORMAL, 'LINEHEIGHT':1.1}
DEFAULT_SMALL = {'font': 'American Typewriter', 'size':22.0, 'style': cairo.FONT_SLANT_NORMAL, 'weight': cairo.FONT_WEIGHT_NORMAL, 'LINEHEIGHT':1.1}
BOLD = {'font': 'American Typewriter', 'size':32.0, 'style': cairo.FONT_SLANT_NORMAL, 'weight': cairo.FONT_WEIGHT_BOLD, 'LINEHEIGHT':1}
BOLD_SMALL = {'font': 'American Typewriter', 'size':22.0, 'style': cairo.FONT_SLANT_NORMAL, 'weight': cairo.FONT_WEIGHT_NORMAL, 'LINEHEIGHT':1}
EMPHASIS = {'font': 'American Typewriter', 'size':32.0, 'style': cairo.FONT_SLANT_OBLIQUE, 'weight': cairo.FONT_WEIGHT_NORMAL, 'LINEHEIGHT':1}
TITLE = {'font': 'American Typewriter', 'size':32.0, 'style': cairo.FONT_SLANT_NORMAL, 'weight': cairo.FONT_WEIGHT_BOLD, 'LINEHEIGHT':1.3}

LAYOUT = {'_SIZE': (2,2), 'DEFAULT': (0,0), 'IMAGE': (1, 0), 'ATTRIB': (0,1)}

BACKGROUND_COLOUR = (0.2, 0.2, 0.2, 1.0)   #RGBA

TEXTS = {'DEFAULT': DEFAULT, 
         'BOLD': BOLD,
         'EMPHASIS': EMPHASIS,
         'TITLE': TITLE,
         'DEFAULT_SMALL': DEFAULT_SMALL,
         'BOLD_SMALL': BOLD_SMALL,}

PARTS = {'DEFAULT': {'BACKGROUND': ((171.0/256.0), (140.0/256.0), (16.0/256.0), 1.0), 'FOREGROUND': (0.0, 0.0, 0.0, 1.0), 
                     'TEXT': TEXTS, 'TEXTWIDTH':46, "MARGIN":(30,0)},
         'IMAGE': {'BACKGROUND': ((171.0/256.0), (140.0/256.0), (16.0/256.0), 1.0), 'FOREGROUND': (0.0, 0.0, 0.0, 1.0), 
                   'TEXT': TEXTS, 'TEXTWIDTH':None, "MARGIN":(0,0),
                   'IMAGES': ["/home/ben/jokedb/jokedbapp/imgs/01.png",
                              "/home/ben/jokedb/jokedbapp/imgs/02.png",
                              "/home/ben/jokedb/jokedbapp/imgs/03.png",
                              "/home/ben/jokedb/jokedbapp/imgs/04.png",
                              "/home/ben/jokedb/jokedbapp/imgs/05.png",
                              "/home/ben/jokedb/jokedbapp/imgs/06.png",
                              "/home/ben/jokedb/jokedbapp/imgs/07.png",
                              "/home/ben/jokedb/jokedbapp/imgs/08.png",
                              "/home/ben/jokedb/jokedbapp/imgs/09.png",
                              "/home/ben/jokedb/jokedbapp/imgs/10.png",
                              "/home/ben/jokedb/jokedbapp/imgs/11.png",
                              "/home/ben/jokedb/jokedbapp/imgs/12.png",
                              "/home/ben/jokedb/jokedbapp/imgs/13.png",
                              "/home/ben/jokedb/jokedbapp/imgs/14.png",
                              "/home/ben/jokedb/jokedbapp/imgs/15.png",
                              "/home/ben/jokedb/jokedbapp/imgs/16.png",
                              "/home/ben/jokedb/jokedbapp/imgs/17.png",
                              "/home/ben/jokedb/jokedbapp/imgs/18.png",
                              "/home/ben/jokedb/jokedbapp/imgs/19.png",
                              "/home/ben/jokedb/jokedbapp/imgs/20.png",
                              "/home/ben/jokedb/jokedbapp/imgs/21.png",
                              "/home/ben/jokedb/jokedbapp/imgs/22.png",
                              "/home/ben/jokedb/jokedbapp/imgs/23.png",
                              "/home/ben/jokedb/jokedbapp/imgs/24.png",
                              "/home/ben/jokedb/jokedbapp/imgs/25.png",
                              "/home/ben/jokedb/jokedbapp/imgs/26.png",
                              "/home/ben/jokedb/jokedbapp/imgs/27.png",
                              "/home/ben/jokedb/jokedbapp/imgs/28.png",
                              "/home/ben/jokedb/jokedbapp/imgs/29.png",
                              "/home/ben/jokedb/jokedbapp/imgs/30.png",
                              "/home/ben/jokedb/jokedbapp/imgs/31.png",
                              "/home/ben/jokedb/jokedbapp/imgs/32.png",
                              "/home/ben/jokedb/jokedbapp/imgs/33.png",
                              "/home/ben/jokedb/jokedbapp/imgs/34.png",
                              "/home/ben/jokedb/jokedbapp/imgs/35.png",
                              "/home/ben/jokedb/jokedbapp/imgs/36.png",
                              "/home/ben/jokedb/jokedbapp/imgs/37.png",
                              "/home/ben/jokedb/jokedbapp/imgs/38.png",
                              "/home/ben/jokedb/jokedbapp/imgs/39.png",
                              "/home/ben/jokedb/jokedbapp/imgs/40.png",
                              "/home/ben/jokedb/jokedbapp/imgs/41.png",
                              "/home/ben/jokedb/jokedbapp/imgs/42.png",
                              "/home/ben/jokedb/jokedbapp/imgs/43.png",
                              "/home/ben/jokedb/jokedbapp/imgs/44.png",
                              "/home/ben/jokedb/jokedbapp/imgs/45.png",
                              "/home/ben/jokedb/jokedbapp/imgs/46.png",
                              "/home/ben/jokedb/jokedbapp/imgs/47.png",
                              "/home/ben/jokedb/jokedbapp/imgs/48.png",
                              "/home/ben/jokedb/jokedbapp/imgs/49.png",
                              "/home/ben/jokedb/jokedbapp/imgs/50.png"]
          },
         'ATTRIB': {'BACKGROUND': ((158.0/256.0), (11.0/256.0), (15.0/256.0), 1.0), 'FOREGROUND': (1.0, 1.0, 1.0, 1.0),
                   'TEXT': TEXTS, 'TEXTWIDTH':40, "MARGIN":(50,0)},}
