from models import *
from config import LOCALBASE


localbase = LOCALBASE

print('creation tables')
localbase.create_table(User)

localbase.close()
