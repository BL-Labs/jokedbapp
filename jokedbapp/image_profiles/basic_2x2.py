import cairo

DEFAULT = {'font': 'DejaVu Serif', 'size':20.0, 'style': cairo.FONT_SLANT_NORMAL, 'weight': cairo.FONT_WEIGHT_NORMAL, 'LINEHEIGHT':1}
BOLD = {'font': 'Georgia', 'size':20.0, 'style': cairo.FONT_SLANT_NORMAL, 'weight': cairo.FONT_WEIGHT_BOLD, 'LINEHEIGHT':1}
EMPHASIS = {'font': 'Georgia', 'size':20.0, 'style': cairo.FONT_SLANT_OBLIQUE, 'weight': cairo.FONT_WEIGHT_NORMAL, 'LINEHEIGHT':1}
TITLE = {'font': 'Georgia', 'size':25.0, 'style': cairo.FONT_SLANT_NORMAL, 'weight': cairo.FONT_WEIGHT_BOLD, 'LINEHEIGHT':1}

LAYOUT = {'_SIZE': (2,2), 'DEFAULT': (0,0), 'IMAGE': (1, 0), 'ATTRIB': (0,1)}

BACKGROUND_COLOUR = (0.0, 0.0, 0.0, 1.0)   #RGBA

TEXTS = {'DEFAULT': DEFAULT, 
         'BOLD': BOLD,
         'EMPHASIS': EMPHASIS,
         'TITLE': TITLE,}

PARTS = {'DEFAULT': {'BACKGROUND': (1.0, 1.0, 1.0, 1.0), 'FOREGROUND': (0.0, 0.0, 0.0, 1.0), 
                     'TEXT': TEXTS, 'TEXTWIDTH':30, "MARGIN":(15,50)},
         'IMAGE': {'BACKGROUND': (1.0, 1.0, 1.0, 1.0), 'FOREGROUND': (0.0, 0.0, 0.0, 1.0), 
                   'TEXT': TEXTS, 'TEXTWIDTH':None, "MARGIN":(15,50)},
         'ATTRIB': {'BACKGROUND': (0.5, 0.1, 0.1, 1.0), 'FOREGROUND': (1.0, 1.0, 1.0, 1.0), 
                   'TEXT': TEXTS, 'TEXTWIDTH':15, "MARGIN":(15,50)},}
