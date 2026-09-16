from telegram import *
from telegram.ext import *
import clientworks
import globals
import events


if __name__ == "__main__":
    globals.init()
    globals.load_general_config()


    if globals.SYS_CONFIG["TOKEN"] is None: 
        print("Token was not defined... Probably file path or permission")
        exit(1)


    app = Application.builder().token(globals.SYS_CONFIG["TOKEN"]).build()
    clientworks.registerClientWorker(app)
    events.init(app)

    app.run_polling()