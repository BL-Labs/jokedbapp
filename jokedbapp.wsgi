activate_this = '/home/ben/jokedb/virt/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, '/home/ben/jokedb')

from jokedbapp import jokedbapp as application

