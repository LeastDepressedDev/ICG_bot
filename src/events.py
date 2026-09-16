import globals
import telegram as tg
import telegram.ext as tge


# async def onMsg(update: Update, 
# context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(f"Message: \n{update.message.text}")

async def got_message(update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
    pass

def init(app: tge.Application):
    app.add_handler(tge.MessageHandler(tge.filters.TEXT, got_message))