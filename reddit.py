import praw
import difflib
import pickle
from textblob import TextBlob
from datetime import datetime
from model import RFModel


class Reddit():
    """docstring for Reddit"""
    def __init__(self, subreddit_name, callback, client_id, client_secret, redirect_url='http://localhost:8080', user_agent='scraper'):
        self.callback = callback
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  redirect_uri=redirect_url,
                                  user_agent=user_agent)

        self.subreddit = self.reddit.subreddit(subreddit_name)

        whitelist_usernames = []
        self.whitelist = []
        for username in whitelist_usernames:
            self.whitelist.append(self.reddit.redditor(username).id)

        self.accepted_users = []
        self.denied_users = []

        self.model = RFModel()

        clf_path = 'lib/models/DecisionTreeClassifier.pkl'
        with open(clf_path, 'rb') as f:
            self.model.clf = pickle.load(f)

        clean_data_path = 'lib/models/CleanData.pkl'
        with open(clean_data_path, 'rb') as f:
            self.model.vectorizer = pickle.load(f)

    def prepare_nn_data(self, comment):
        def diff_ratio(_a, _b):
            return difflib.SequenceMatcher(a=_a, b=_b).ratio()

        no_follow = comment.submission.no_follow
        author_verified = comment.author.verified
        author_comment_karma = comment.author.comment_karma
        author_link_karma = comment.author.link_karma
        over_18 = comment.submission.over_18
        is_submitter = comment.is_submitter

        num_comments = 0
        num_last_30_days = 0
        rec_no_follow = 0
        gilded = 0
        responses = 0
        neg_score_count = 0
        score = 0
        min_score = 0
        controversiality = 0
        ups = 0
        diff_ratio_count = 0
        max_diff_ratio = 0
        sentiment_polarity = 0
        min_sentiment_polarity = 0

        month_ago = datetime.now().timestamp() - 60*60*24*30  # 30 days
        body = comment.body.replace("\r", "").replace("\n", "")[:256]
        for c in comment.author.comments.new(limit=25):
            num_comments += 1
            num_last_30_days += 1 if c.created_utc < month_ago else 0
            rec_no_follow += 1 if c.no_follow else 0
            gilded += 1 if c.gilded else 0
            responses += c.num_comments
            neg_score_count += 1 if c.score < 0 else 0
            score += c.score
            min_score = min(min_score, c.score)
            controversiality += c.controversiality
            ups += c.ups
            dr = diff_ratio(body, c.body.replace("\r", "").replace("\n", "")[:256])
            diff_ratio_count += dr
            max_diff_ratio = max(max_diff_ratio, dr)
            sp = TextBlob(c.body).sentiment.polarity
            sentiment_polarity += sp
            min_sentiment_polarity = min(min_sentiment_polarity, sp)

        return([
            no_follow,
            author_verified,
            author_comment_karma,
            author_link_karma,
            over_18,
            is_submitter,
            num_comments,
            num_last_30_days,
            rec_no_follow / num_comments,  # avg_no_follow,
            gilded / num_comments,  # avg_gilded,
            responses / num_comments,  # avg_responses,
            (neg_score_count / num_comments) * 100,  # percent_neg_score,
            score / num_comments,  # avg_score,
            min_score,  # min_score,
            controversiality / num_comments,  # avg_controversiality,
            ups / num_comments,  # avg_ups,
            diff_ratio_count / num_comments,  # avg_diff_ratio,
            max_diff_ratio,  # max_diff_ratio,
            sentiment_polarity / num_comments,  # avg_sentiment_polarity,
            min_sentiment_polarity  # min_sentiment_polarity,
        ])

    def check_user(self, comment):
        author = comment.author.id

        # User in whitelist, they can do whatever they want.
        if author in self.whitelist:
            return False, "In whitelist."

        # Approved before.... let them pass
        if author in self.accepted_users:
            return False, "User already approved."

        # User has already been denied
        if author in self.denied_users:
            return True, "User previously denied."

        prediction = self.model.predict([self.prepare_nn_data(comment)])
        if prediction == 'normal':
            pass  # 'normal user'
        elif prediction == 'bot':
            return True, 'possible bot'
        elif prediction == 'troll':
            return True, 'possible troll'
        else:
            return False, 'Classification error'

        # All checks complete.  Mark them as good
        self.accepted_users.append(author)
        return False, "Passed checks."

    def run(self):
        for comment in self.subreddit.stream.comments():
            problem, reason = self.check_user(comment)
            if problem:
                self.callback(
                    f"/u/{comment.author.name}: {reason}",
                    comment.submission.title,
                    comment.body,
                    comment.link_url
                )
