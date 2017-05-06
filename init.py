from config import localbase
import models

localbase.connect()


print("do you need import data from old format base? yes/no")
answer = input()
if answer == 'yes':
    print("enter path to old base: ")
    OldBase = input()
elif answer == 'no':
    print('')
else:
    pass
