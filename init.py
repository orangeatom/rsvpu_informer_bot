from models import *

localbase = LOCALBASE

print('creation tables')
localbase.create_table(User)

localbase.close()
