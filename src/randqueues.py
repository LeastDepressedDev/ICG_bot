from clientworks import cmd
import telegram as tg
import telegram.ext as tge
import random
import globals

queues: dict[int, list[str]] = {}
poll_stack: dict[int, list[int]] = {}

def reg(channel: int, pull: str) -> bool:
    if pull in queues[channel]:
        return False
    else:
        queues[channel].append(pull)
        return True

@cmd.general("poll", public=True)
async def poll(update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in [tg.Chat.GROUP, tg.Chat.SUPERGROUP]:
        if update.message.chat_id not in queues:
            queues[update.message.chat_id] = []
            poll_stack[update.message.chat_id] = []
            await update.message.reply_text(globals.get_translation("en", "msg.randq.new_queue"))
            return

        q = queues[update.message.chat_id]
        if len(q)==0:
            await update.message.reply_text(globals.get_translation("en", "msg.randq.null_q"))
        else:
            
            roll = []
            ix = 1
            while len(q)>0:
                i = random.randint(0, len(q)-1)
                roll.append(f"{ix}: {q.pop(i)}")
                ix+=1

            msg: str = globals.get_translation("en", "msg.randq.rolling_for")
            msg = msg.replace("{amount}", str(len(roll))).replace("{nterm_list}", '\n'.join(roll))
            comp = await update.message.reply_text(msg)
            poll_stack[update.message.chat_id].append(comp.id)

    else:
        await update.message.reply_text(globals.get_translation("en", "msg.randq.req_ingroup"))

@cmd.general("pushme", public=True)
async def pushme(update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in [tg.Chat.GROUP, tg.Chat.SUPERGROUP]:
        if update.message.chat_id not in queues:
            await update.message.reply_text(globals.get_translation("en", "msg.randq.noq_there"))
            return

        name = update.effective_sender.name
        if reg(update.message.chat_id, name):
            await update.message.reply_text(globals.get_translation("en", "msg.randq.pushme_success").replace("{name}", name))
        else:
            await update.message.reply_text(globals.get_translation("en", "msg.randq.pushme_fail"))
    else:
        await update.message.reply_text(globals.get_translation("en", "msg.randq.req_ingroup"))


@cmd.admin("test_payload", public=True)
async def test_payload(update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in [tg.Chat.GROUP, tg.Chat.SUPERGROUP]:
        if update.message.chat_id not in queues:
            queues[update.message.chat_id] = []
            poll_stack[update.message.chat_id] = []
            await update.message.reply_text(globals.get_translation("en", "msg.randq.new_queue"))
            return
        
        pval = ["Groalder 1", "Groalder 2", "Groalder 3", "Saske", "YOU CANT RUN", "IceWallowCum"]
        
        results = []
        for p in pval:
            results.append(reg(update.message.chat_id, p))
        await update.message.reply_text(str(results))
    else:
        await update.message.reply_text(globals.get_translation("en", "msg.randq.req_ingroup"))