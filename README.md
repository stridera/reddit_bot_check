# Show suspected Reddit trolls and bots on Discord.

As a mod for one of the bigger subreddits, we're always working to quickly identify and remove trolls and bots.  My first attempt was to attempt and implement the neural network discussed here on [Towards Data Science](https://towardsdatascience.com/trolls-and-bots-are-disrupting-social-media-heres-how-ai-can-stop-them-d9b969336a06).

The code is based off their code which can be found here:  https://github.com/devspotlight/Reddit-Dashboard-ML

The models and model code is taken directly from them.  You really should read their writeup.

Note:  I did not write/change the model code, nor did I train this the model.  Any questions about that should be directed to the original authors!  

##Installation
To run, create a .env file that looks like the following:

```bash
DISCORD_WEBHOOK_URL=https://discordapp.com/api/webhooks/<UUID>
REDDIT_SUBREDDIT=<SUBREDDIT>
REDDIT_CLIENT_ID=<CLIENT ID>
REDDIT_CLIENT_SECRET=<CLIENT_SECRET>
```

The 	discord webhook url can be grabbed via the settings on your discord channel.
Reddit authentication information found [on the praw site](https://praw.readthedocs.io/en/latest/getting_started/authentication.html).

I will probably create a requirements.txt later, but for now, install modules as required.  :)  (Sorry!)

## Running
```bash
python3 bot.py
```
Should be that easy.