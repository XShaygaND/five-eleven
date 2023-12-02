import sys
import settings

def runbot():
    from bot import bot

    while True:
        try:
            bot.polling()

        except Exception as err:
            bot.send_message(settings.OWNER_CID, err)
    

def truncate_db():
    from storage import db

    db.drop_tables()


def truncate_requests():
    from storage import db

    db.drop_table('requests')


arg_funcs = {
    'run':  runbot,
    'trunc': truncate_db,
    'truncreq': truncate_requests,
}

args = sys.argv

for arg in args[1:]:
    if arg in arg_funcs:
         arg_funcs[arg]()

    else:
        print('invalid argument: ' + arg)
