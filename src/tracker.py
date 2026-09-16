import telegram as tg
import telegram.ext as tge
import globals
import re

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

        if not isinstance(self.filters, list): raise "Tracker field (filters) should be a list of strings."
        self.filters = []
        for exp in config["filters"]:
            self.filters.append(re.compile(exp))

        self.iftl = 0
        for tag in config["tags"]:
            if tag in Tracker.mapper.keys():
                self.iftl |= Tracker.mapper[tag]
            else:
                globals.do_debug_msg(f"Invalid filter tag: {tag}. Skipping...")

    
    # TODO: Read into it and make it better
    @staticmethod
    def process_input(self: Tracker, update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
        
        pass
        

    def register(self, app: tge.Application):
        app.add_handler(tge.MessageHandler(self.iftl, Tracker.process_input))