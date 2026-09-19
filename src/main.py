from telegram import *
from telegram.ext import *
import json

import clientworks
import globals
import events
import tracker


if __name__ == "__main__":
    globals.init()
    globals.load_general_config()


    if globals.SYS_CONFIG["TOKEN"] is None: 
        print("Token was not defined... Probably file path or permission")
        exit(1)


    app = Application.builder().token(globals.SYS_CONFIG["TOKEN"]).build()
    clientworks.registerClientWorker(app)

    for tracker_pth in globals.track_paths:
        with open(tracker_pth, 'r') as f:
            cfg: dict[str] = json.loads(f.read())
            t = tracker.Tracker(cfg)
            t.register(app)

    events.init(app)

    app.run_polling()