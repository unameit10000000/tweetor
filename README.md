<p align="center">
  <img src="./app/static/tweetor.png">
</p>

# Tweetor
Basic Twitterbot Manager to create automated Tweets. Uses OpenAI's GPT-3 to randomize messages. Hosted on Akash Decentralized Cloud.
This example is tested on Ubuntu.
### Example
MetaBrainz active Twitterbot is based on this example! See <code><a href="https://twitter.com/metabrainz_io/status/1524751303343104004">Tweet</a></code>
## NOTE
Do not share your public domain (Akash uri) when using this example template! This is a basic example that is coded hastily in one go and meant for experimental purposes only. The Author and Owner of this repository can not be held liable for any loss resulting from using this code. It is rumored that using GPT-3 for twitter goes against OpenAI's TOS. Use at your own risk.
## Requirements
#### Minimum:
 -  <code><a href="https://docs.docker.com/engine/install/">Docker</a></code>
 -  <code><a href="https://developer.twitter.com">Twitter Developer Account</a></code>
 -  <code><a href="https://openai.com/api/">OpenAI API Account</a></code>
#### Only needed when hosting on Akash:
 -  <code><a href="https://docs.akash.network/guides/deploy/akashlytics-deploy-installation">Akashlythics</a></code>
 -  <code><a href="https://akash.network/token">AKT Token</a></code>

## Preparation
1. Setup/Configure Developer accounts
2. Get the required keys for the environment variables:
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_BEARER_TOKEN`
- `GPT_ORG_ID`
- `GPT_API_KEY`
3. Set callback urls in Twitters Developer Portal:
-  For Local: `http://127.0.0.1:5500/authenticate`
-  For Akash: See section <code><a href="https://github.com/unameit10000000/testsite/edit/main/README.md#test-on-akash">Test On Akash</a></code>
## Test Locally
Make sure to replace the above mentioned environment variables in `.localtest` file.
### CLI
```
sudo make build
```
```
sudo make up
```
### Once running
1. Go to: `http://127.0.0.1:5500/`
2. Insert callback url `http://127.0.0.1:5500/authenticate/`
3. Authorize using Twitter
4. Call some endpoints (using curl, postman, etc)
## Test On Akash
Get started with Akash <code><a href="https://docs.akash.network/">Docs</a></code> 
### Build & Push Docker Image
Edit the `Makefile` and replace: `<dckr_username>/<image-tag:version>`
#### CLI
```
sudo make push
```
### Create deployment
Once the image has been pushed to dockerhub:
1. Edit the `deploy.yml` file.
2. Create a new deployment with Akashlytics. 
3. Select 'empty' and paste `deploy.yml` contents.
### deploy.yml
Make sure to replace the above mentioned environment variables in `deploy.yml` file.
Additionally replace the `image` value.
### Once deployed:
1. Go to Akash uri, for example: `http://your-akash-uri.eu-west01-akash.provider.com`
2. Insert callback uri, for example: `http://your-akash-uri.eu-west01-akash.provider.com/authenticate/`
3. Authorize using Twitter
4. Call some endpoints (using curl, postman, etc)
5. NOTE: Do not share your public domain (Akash uri) when using this example template!

## Endpoints
- `/create_tweetor`
- `/list_tweetors`
- `/remove_tweetor`
- `/remove_all`
#### [POST] /create_tweetor
```
http://127.0.0.1:5500/create_tweetor
```
```json
{
    "interval": {
        "days":0,"hours":0, "minutes": 5, "seconds":0,
        "start_date":"", "end_date":"","timezone":""
    },
    "gpt_use": 1,
    "gpt_prompt": "Tweet something awesome about Elon Musk",
    "gpt_prompt_topic": "@elonmusk",
    "tweetor_type": 0,    
    "tweetor_name": "mytweetor",
    "tweetor_message": ""
}
```
#### [GET] /list_tweetors
```
http://127.0.0.1:5500/list_tweetors
```
#### [GET] /remove_tweetor/tweetor_name
```
http://127.0.0.1:5500/remove_tweetor/mytweetor
```
#### [GET] /remove_all
```
http://127.0.0.1:5500/remove_all
```
## DISCLAIMER
Do not share your public domain (Akash uri) when using this example template! This is a basic example that is coded hastily in one go and meant for experimental purposes only. The Author and Owner of this repository can not be held liable for any loss resulting from using this code. It is rumored that using GPT-3 for twitter goes against OpenAI's TOS. Use at your own risk.
