from models import *
from database import init_db

dbsession = init_db()

u = User('ben', 'bosteen@gmail.com', 'admin', 'saltypasswordhash')
u2 = User('bob', 'bob@victorianhumour.com', 'admin', 'anactuallyfunnyjoke')
# remember to reset password after bootstrapping and generating a salt

dbsession.add(u)
dbsession.add(u2)
dbsession.commit()
dbsession.close()
