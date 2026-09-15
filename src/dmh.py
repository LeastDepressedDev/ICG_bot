import telegram as tg
import telegram.ext as tge
import globals

class DirectMsgHandler:
    def __init__(self, app: tge.Application): 
        self.app = app

    def registerCommand(self, cmd: str, exec: tge.ContextTypes.DEFAULT_TYPE):
        async def upper(update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
            if update.effective_chat.type == tg.Chat.PRIVATE:
                globals.do_debug_msg(f"Executing private command: {cmd}")
                await exec(update, context)
            else:
                globals.do_debug_msg(f"Tried to execute command in non-private chat: {cmd}(type: {update.effective_chat.type})")
        self.app.add_handler(tge.CommandHandler(cmd, upper))

    


