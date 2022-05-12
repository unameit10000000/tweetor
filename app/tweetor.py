"""
=================================
DISCLAIMER
---------------------------------
Do not share your public domain (Akash uri) when using this example template! 
This is a basic example that is coded in one go and meant for experimental purposes only. 
The Author and Owner of this repository can not be held liable for any loss resulting from using this example code. Use at your own risk.

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


import os, json, time, requests, config, tweepy


"""
=================================
Func: Init Tweetor
---------------------------------
Create tweepy instance to fetch 
twitter authorization url
=================================
"""
def init_tweetor(uri):
    oauth1_user_handler = tweepy.OAuth1UserHandler(
        consumer_key=config.API_KEY,
        consumer_secret=config.API_SECRET,
        callback=uri
    )
    try:
        auth_url = oauth1_user_handler.get_authorization_url()
        return True, auth_url, oauth1_user_handler
    except tweepy.errors.TweepyException as e:
        return False, e, None


"""
=================================
Func: Re-init Tweetor
---------------------------------
Reinit tweepy instance to get 
access tokens
=================================
"""
def reinit_tweetor(oauth_verifier, access):
    # Reinitialize
    oauth1_user_handler = tweepy.OAuth1UserHandler(
        consumer_key=config.API_KEY,
        consumer_secret=config.API_SECRET,
        callback=access.callback
    )    

    # Using previously provided request tokens
    oauth1_user_handler.request_token = {
        "oauth_token": access.request_token,
        "oauth_token_secret": access.request_token_secret
    }

    # Get the access keys
    if oauth1_user_handler:
        try:
            access_token, access_token_secret = (
                oauth1_user_handler.get_access_token(verifier=oauth_verifier)
            )
            return True, (access_token, access_token_secret)
        except tweepy.errors.TweepyException as e:
            return False, e
    else:
        return False, "OAuth1UserHandler not initialized."


"""
=================================
Func: Execute Tweet
=================================
"""
def tweet(access, message):
    oauth1_user_handler = tweepy.OAuth1UserHandler(
        consumer_key=config.API_KEY,
        consumer_secret=config.API_SECRET,
        access_token=access.oauth_access_key,
        access_token_secret=access.oauth_access_key_secret
    )

    try:
        client = tweepy.Client(
            consumer_key=config.API_KEY,
            consumer_secret=config.API_SECRET,
            access_token=access.oauth_access_key,
            access_token_secret=access.oauth_access_key_secret,
            bearer_token=config.BEARER_TOKEN)
        response = client.create_tweet(text=message)
        return True, response
    except tweepy.errors.TweepyException as e:
        return False, e