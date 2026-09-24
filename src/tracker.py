"""
Tracker json object documentation:

{
    "output_channel": [integer, ...] | integer, // Channels to resend message
    "input_channel": [integer, ...] | integer, // Channels to track for messages
    "forward": boolean,  // Use telegram forward instead of raw message text resend
    "filters": [ // List of regex match filters applied on message to determin whether resend it or not
        {
            "case": boolean, // False if it is case irrelevant.
            "pattern": string // regex pattern
        },
        ...
    ],
    "tags": [ // Telegram API tags to determin the message possbile type and attributes
        "*", // All the messages will be tracked
        "text" // Messages with text parts will be tracked
    ]
}
"""

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
    forward: bool

    def __init__(self, config: dict[str]):
        self.out = config["output_channel"]
        self.forward = config["forward"]
        self.inp = config["input_channel"]

        if isinstance(self.inp, int):
            self.inp = [self.inp]
        if isinstance(self.out, int):
            self.out = [self.out]

            
        self.filters = []
        if not isinstance(self.filters, list): raise "Tracker field (filters) should be a list of strings."
        for exp in config["filters"]:
            flags = re.RegexFlag.NOFLAG
            if not exp["case"]: flags |= re.RegexFlag.IGNORECASE
            self.filters.append(re.compile(exp["pattern"], flags))

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
                if tracker.forward:
                    await update.message.forward(oc)
                else:
                    restl = globals.get_translation("en", "msg.resend_msg_response")
                    restl = restl.replace("{user_name}", update.effective_user.name).replace("{text}", update.message.text)
                    await context.bot.send_message(oc, restl)
        
        return process_input
        

    def register(self, app: tge.Application):
        app.add_handler(tge.MessageHandler(self.iftl, Tracker.define_input_processor(self)))