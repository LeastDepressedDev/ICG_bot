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
    def _register_cmd(fn, cmd: str, debug: bool):
        global _cmds
        _cmds.append((cmd, fn, [0, 1][debug]))

    @staticmethod
    def admin(command: str, debug: bool = False):
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
                    await update.message.reply_text(globals.get_translation("en", "msg.internal_error"))
                    await update.message.reply_text(f"Adming log: {e}")

            cmd._register_cmd(sub, command, debug)
            return sub
        return decorator

        
    @staticmethod
    def general(command: str, debug: bool = False):
        def decorator(fn):
            
            # TODO: Make a factory for subs
            async def sub(update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
                try:
                    await fn(update, context)
                except Exception as e:
                    print(e)
                    await update.message.reply_text(globals.get_translation("en", "msg.internal_error"))
                    if update.effective_user.id in globals.admins:
                        await update.message.reply_text(f"Adming log: {e}")

            cmd._register_cmd(fn, command, debug)
            return fn
        return decorator

    




@cmd.general("start")
async def start(update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
    response = globals.get_translation("en", "msg.start");
    response = response.replace("{user}", update.effective_user.username)
    await update.message.reply_text(response)


@cmd.general("whoami", debug=True)
async def whoami(update: tg.Update, context):
    await update.message.reply_text(
        f"{globals.get_translation('en', 'msg.whoami')}: {update.effective_user.id}"
    )


@cmd.admin("test")
async def test(update: tg.Update, context):
    await update.message.reply_text(globals.get_translation("en", "msg.test.1"))




def registerClientWorker(app: tg.Application):
    handle = dmh.DirectMsgHandler(app)

    for pr in _cmds:
        if pr[2] or globals.is_debug(): handle.registerCommand(pr[0], pr[1])
    