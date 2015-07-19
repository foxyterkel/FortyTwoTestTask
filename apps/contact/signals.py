from django.db import connection
from django.utils.timezone import now


def my_receiver(sender, **kargs):
    curs = connection.cursor()
    try:
        if kargs['created']:
            action = 'create'
        else:
            action = 'save'
    except:
        action = 'delete'
    command = "INSERT INTO Loger VALUES ('%s', '%s', '%s');" % \
              (sender._meta.model_name, action, str(now()))
    print(command)
    curs.execute(command)
    # curs.commit()
    curs.close()
