import requests

def get_motivational() -> str:
    response = requests.get("https://zenquotes.io/api/random").json()[0]

    return f"*{response['q']}*\n(c) {response['a']}"