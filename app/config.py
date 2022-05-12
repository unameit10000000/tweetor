"""
=================================
DISCLAIMER
---------------------------------
This is a basic example that is coded in one go and meant for experimental purposes only. 
The Author and Owner of this repository can not be held liable for any loss resulting from using this example code. 
Use at your own risk.

AUTHOR
---------------------------------
- alias:    LnrCdr
- github:   https://github.com/unameit10000000/
- twitter:  https://twitter.com/unameit10000000

ABOUT
---------------------------------
- 3-legged OAuth example for Twitter using Tweepy
- Auto text completion using OpenAI's GPT-3

DOCS
---------------------------------
- Twitter Docs:   https://developer.twitter.com/en/docs/authentication/oauth-1-0a/obtaining-user-access-tokens
- Tweepy Docs:    https://docs.tweepy.org/en/stable/authentication.html#legged-oauth
- OpenAI API:     https://openai.com/api/
- ApScheduler:    https://viniciuschiele.github.io/flask-apscheduler/
=================================
"""


import os


PORT = os.getenv("PORT")
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
GPT_ORG_ID = os.getenv("GPT_ORG_ID")
GPT_API_KEY = os.getenv("GPT_API_KEY")
