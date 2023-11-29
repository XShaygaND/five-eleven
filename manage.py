import sys

def runbot():
    from bot import bot

    while True:
        try:
            bot.polling()

        except Exception as err:
            print(err)
    

def truncate_db():
    from storage import db

    db.drop_tables()


arg_funcs = {
    'run':  runbot,
    'trunc': truncate_db,
}

args = sys.argv

for arg in args[1:]:
    if arg in arg_funcs:
         arg_funcs[arg]()

    else:
        print('invalid argument: ' + arg)
