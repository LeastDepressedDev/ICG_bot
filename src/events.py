import globals
import tracker
import telegram as tg
import telegram.ext as tge

trackers: list[tracker.Tracker] = []

async def got_message(update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):

    

    # Working with trackers(Lowest prio)
    for track in trackers:
        await track.process_input(update, context)
    pass

def init(app: tge.Application):
    # Message events
    app.add_handler(tge.MessageHandler(tge.filters.TEXT, got_message)) 