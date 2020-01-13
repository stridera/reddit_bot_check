import requests
import json


class Discord():
    """docstring for Discord"""
    def __init__(self, url, username="Bot"):
        self.url = url
        self.username = username

    def sendMsg(self, msg, emb_title, emb_content, emb_url):
        data = {}
        data["username"] = self.username
        data["content"] = msg
        data["embeds"] = []

        embed = {}
        embed["title"] = emb_title
        embed["description"] = emb_content
        embed['url'] = emb_url
        data["embeds"].append(embed)

        result = requests.post(self.url, data=json.dumps(data), headers={"Content-Type": "application/json"})

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print("Payload delivered successfully, code {}.".format(result.status_code))


# Used to test
def main():
    import os
    from dotenv import load_dotenv

    load_dotenv()

    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    d = Discord(discord_webhook_url)
    d.sendMsg("Test Msg", "Emb Title", "Emb Content", "https://www.reddit.com/")


if __name__ == '__main__':
    main()
