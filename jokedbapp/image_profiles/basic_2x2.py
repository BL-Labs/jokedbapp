import cairo

DEFAULT = {'font': 'American Typewriter', 'size':16.0, 'style': cairo.FONT_SLANT_NORMAL, 'weight': cairo.FONT_WEIGHT_NORMAL, 'LINEHEIGHT':1.1}
DEFAULT_SMALL = {'font': 'American Typewriter', 'size':2.0, 'style': cairo.FONT_SLANT_NORMAL, 'weight': cairo.FONT_WEIGHT_NORMAL, 'LINEHEIGHT':1.1}
BOLD = {'font': 'American Typewriter', 'size':16.0, 'style': cairo.FONT_SLANT_NORMAL, 'weight': cairo.FONT_WEIGHT_BOLD, 'LINEHEIGHT':1}
BOLD_SMALL = {'font': 'American Typewriter', 'size':12.0, 'style': cairo.FONT_SLANT_NORMAL, 'weight': cairo.FONT_WEIGHT_NORMAL, 'LINEHEIGHT':1}
EMPHASIS = {'font': 'American Typewriter', 'size':16.0, 'style': cairo.FONT_SLANT_OBLIQUE, 'weight': cairo.FONT_WEIGHT_NORMAL, 'LINEHEIGHT':1}
TITLE = {'font': 'American Typewriter', 'size':18.0, 'style': cairo.FONT_SLANT_NORMAL, 'weight': cairo.FONT_WEIGHT_BOLD, 'LINEHEIGHT':1.3}

LAYOUT = {'_SIZE': (2,2), 'DEFAULT': (0,0), 'IMAGE': (1, 0), 'ATTRIB': (0,1)}

BACKGROUND_COLOUR = (0.2, 0.2, 0.2, 1.0)   #RGBA

TEXTS = {'DEFAULT': DEFAULT, 
         'BOLD': BOLD,
         'EMPHASIS': EMPHASIS,
         'TITLE': TITLE,
         'DEFAULT_SMALL': DEFAULT_SMALL,
         'BOLD_SMALL': BOLD_SMALL,}

PARTS = {'DEFAULT': {'BACKGROUND': ((171.0/256.0), (140.0/256.0), (16.0/256.0), 1.0), 'FOREGROUND': (0.0, 0.0, 0.0, 1.0), 
                     'TEXT': TEXTS, 'TEXTWIDTH':70, "MARGIN":(15,10)},
         'IMAGE': {'BACKGROUND': ((158.0/256.0), (11.0/256.0), (15.0/256.0), 1.0), 'FOREGROUND': (0.0, 0.0, 0.0, 1.0), 
                   'TEXT': TEXTS, 'TEXTWIDTH':None, "MARGIN":(5,5),
                   'IMAGES': ["/home/ben/jokedb/jokedbapp/imgs/tophat.png",
                             "/home/ben/jokedb/jokedbapp/imgs/facepalm.png",
                             "/home/ben/jokedb/jokedbapp/imgs/mechcom.png", ]
          },
         'ATTRIB': {'BACKGROUND': ((158.0/256.0), (11.0/256.0), (15.0/256.0), 1.0), 'FOREGROUND': (1.0, 1.0, 1.0, 1.0),
                   'TEXT': TEXTS, 'TEXTWIDTH':40, "MARGIN":(30,5)},}
