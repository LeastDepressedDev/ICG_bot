import json
import os

SYS_CONFIG = {
    "debug": True,
    "tknpth": "./token.tkn",
    "global_cfg": "./icg_config.json",
    "TOKEN": None,
    "json_indent": 4
}

__default_global_config = {
    "lang": [
        {
            "name": "en",
            "path": "lang/en"
        }
    ],
    "def_lang": "en",
    "admin_user_ids": []
}

langs: dict[str, dict[str, str]] = None
admins: set[int] = None

def init():
    with open(SYS_CONFIG["tknpth"], 'r') as f:
        SYS_CONFIG["TOKEN"] = f.read()
        do_debug_msg(f"Got token: {SYS_CONFIG['TOKEN']}")

def pretty_dump(cfg: dict) -> str: return json.dumps(cfg, indent=SYS_CONFIG["json_indent"])


# TODO: Maybe make it recursive synchro later, but for now this will work just fine
def synchro_configs(cfg: dict[str]):
    flag0 = False
    for k in __default_global_config.keys():
        if k not in cfg.keys():
            flag0 = True
            cfg[k] = __default_global_config[k]
    
    if flag0:
        with open(SYS_CONFIG["global_cfg"], 'w') as f:
            f.write(pretty_dump(cfg))



def load_general_config():
    global langs, admins
    if not os.path.exists(SYS_CONFIG["global_cfg"]):
        print("No global config found... Creating new one")
        with open(SYS_CONFIG["global_cfg"], 'w') as f:
            f.write(pretty_dump(__default_global_config))

    
    with open(SYS_CONFIG["global_cfg"], 'r') as f:
        cfg: dict[str] = json.loads(f.read())
        synchro_configs(cfg)
        
        langs = {}
        for slg in cfg["lang"]:
            with open(f"{slg['path']}.json", 'r') as f:
                langs[slg["name"]] = json.loads(f.read())

        admins = set(cfg["admin_user_ids"])        
        

def get_translation(lang: str, key: str) -> str:
    if lang is None: raise "No lang is given..."
    if key is None: raise "No key is given..."

    if lang in langs.keys(): 
        if key in langs[lang].keys(): return langs[lang][key]
        else: return key
    else: return key

def is_debug() -> bool: return SYS_CONFIG["debug"]

def do_debug_msg(msg: str):
    if is_debug(): print(msg)