import telegram as tg
import telegram.ext as tge
import globals
import re

# Default https pattern: .*http.{0,1}:\\/\\/.+\\..+

class Tracker:
    mapper: dict[str] = {
        "*": tge.filters.ALL,
        "text": tge.filters.TEXT
    }

    out: list[int]|int
    inp: list[int]|int
    filters: list[re.Pattern]

    def __init__(self, config: dict[str]):
        self.out = config["output_channel"]
        self.inp = config["input_channel"]

        if isinstance(self.inp, int):
            self.inp = [self.inp]
        if isinstance(self.out, int):
            self.out = [self.out]

            
        self.filters = []
        if not isinstance(self.filters, list): raise "Tracker field (filters) should be a list of strings."
        for exp in config["filters"]:
            self.filters.append(re.compile(exp))

        self.iftl = ~tge.filters.ALL
        for tag in config["tags"]:
            if tag in Tracker.mapper.keys():
                self.iftl |= Tracker.mapper[tag]
            else:
                globals.do_debug_msg(f"Invalid filter tag: {tag}. Skipping...")


    @staticmethod
    def define_input_processor(tracker: Tracker):
        async def process_input(update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
            globals.do_debug_msg(f"Got message from: {update.message.chat.id}")
            if update.message.chat.id not in tracker.inp: return
            flag0 = True
            for ftl in tracker.filters:
                if ftl.fullmatch(update.message.text): flag0 = False
            if flag0: return
            
            
            globals.do_debug_msg(f"Approved: Resending to -> {', '.join([str(v) for v in tracker.out])}")
            for oc in tracker.out:
                await context.bot.send_message(oc, f"Imp msg:\n{update.message.text}")
        
        return process_input
        

    def register(self, app: tge.Application):
        app.add_handler(tge.MessageHandler(self.iftl, Tracker.define_input_processor(self)))