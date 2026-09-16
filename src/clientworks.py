import dmh
import globals
import telegram as tg
import telegram.ext as tge

# Reference command
# async def start(update: Update, 
# context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Fuck you")

_cmds: list[tuple] = []

class cmd:
    @staticmethod
    def _register_cmd(fn, cmd: str, debug: bool, public: bool):
        global _cmds
        _cmds.append((cmd, fn, debug, public))

    @staticmethod
    def admin(command: str, debug: bool = False, public: bool = False):
        def decorator(fn):

            # TODO: Make a factory for subs
            async def sub(update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
                try:
                    if update.effective_user.id in globals.admins:
                        await fn(update, context)
                    else:
                        await update.message.reply_text(globals.get_translation("en", "msg.permission_denied"))
                except Exception as e:
                    print(e)
                    msg = await update.message.reply_text(globals.get_translation("en", "msg.internal_error"))
                    await msg.reply_text(f"Admin log: {e}")

            cmd._register_cmd(sub, command, debug, public)
            return sub
        return decorator

        
    @staticmethod
    def general(command: str, debug: bool = False, public: bool = False):
        def decorator(fn):
            
            # TODO: Make a factory for subs
            async def sub(update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
                try:
                    await fn(update, context)
                except Exception as e:
                    print(e)
                    msg = await update.message.reply_text(globals.get_translation("en", "msg.internal_error"))
                    if update.effective_user.id in globals.admins:
                        await msg.reply_text(f"Admin log: {e}")

            cmd._register_cmd(sub, command, debug, public)
            return sub
        return decorator

    




@cmd.general("start")
async def start(update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
    response = globals.get_translation("en", "msg.start")
    response = response.replace("{user}", update.effective_user.username)
    await update.message.reply_text(response)


@cmd.general("whoami", debug=True)
async def whoami(update: tg.Update, context):
    await update.message.reply_text(
        f"{globals.get_translation('en', 'msg.whoami')}: {update.effective_user.id}"
    )

@cmd.general("whereami", debug=True, public=True)
async def whareami(update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
    response = globals.get_translation("en", "msg.whareami")
    chat = update.effective_chat
    response = response.replace("{chat_name}", str(chat.title)).replace("{chat_id}", str(chat.id))\
        .replace("{chat_type}", str(chat.type))
    await update.message.reply_text(response)


@cmd.admin("test")
async def test(update: tg.Update, context):
    await update.message.reply_text(globals.get_translation("en", "msg.test.1"))




def registerClientWorker(app: tg.Application):
    handle = dmh.DirectMsgHandler(app)

    for pr in _cmds:
        if pr[2] or globals.is_debug(): 
            if pr[3]: handle.registerPublicCommand(pr[0], pr[1])
            else: handle.registerPrivateCommand(pr[0], pr[1])
    