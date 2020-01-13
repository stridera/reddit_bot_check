import os
from dotenv import load_dotenv

from reddit import Reddit
from discord import Discord


def print_details(msg, emb_title, emb_content, emb_url):
    print(f'MSG: {msg}\nEmb Title: {emb_title}\n{emb_content}\nURL: {emb_url}\n\n')


def main():
    load_dotenv()

    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    subreddit = os.getenv('REDDIT_SUBREDDIT')
    reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
    reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")

    discord = Discord(discord_webhook_url)

    # Echo to discord weblink
    reddit = Reddit(subreddit, discord.sendMsg, reddit_client_id, reddit_client_secret)

    # Echo locally to test.
    # reddit = Reddit(print_details, reddit_client_id, reddit_client_secret)

    reddit.run()


if __name__ == '__main__':
    main()
