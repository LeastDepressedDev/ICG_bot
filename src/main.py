from telegram import *
from telegram.ext import *
import clientworks
import dmh
import globals


async def onMsg(update: tg.Update, 
context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You aare pidoras\n{update.message.text}")

if __name__ == "__main__":
    globals.init()
    globals.load_general_config()


    if globals.SYS_CONFIG["TOKEN"] is None: 
        print("Token was not defined... Probably file path or permission")
        exit(1)


    app = Application.builder().token(globals.SYS_CONFIG["TOKEN"]).build()
    clientworks.registerClientWorker(app)

    app.add_handler(MessageHandler(filters.TEXT, onMsg))

    app.run_polling()