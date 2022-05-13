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


import os, hashlib, json, datetime, config, tweetor, openai
from flask import Flask, request, jsonify, redirect, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from flask_apscheduler.auth import HTTPBasicAuth


"""
=================================
APScheduler Config
=================================
"""
class Config:
    JOBS = []
    SCHEDULER_API_ENABLED = True
    SCHEDULER_AUTH = HTTPBasicAuth()

app = Flask(__name__)
app.secret_key = 'NOT_SO_GOOD_SECRET_KEY'
app.config.from_object(Config())


"""
=================================
SQLAlchemy Config
=================================
"""
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


"""
=================================
SQLAlchemy DB
=================================
"""
class StoreAccess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    callback = db.Column(db.String(100), nullable=True)
    oauth_token = db.Column(db.String(100), nullable=True)
    oauth_verifier = db.Column(db.String(100), nullable=True)
    oauth_access_key = db.Column(db.String(100), nullable=True)
    oauth_access_key_secret = db.Column(db.String(100), nullable=True)
    request_token = db.Column(db.String(100), nullable=True)
    request_token_secret = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<StoreAccess {self.id}>'


"""
=================================
Func: Get Stored Access Data
---------------------------------
Always returns the last record
=================================
"""
def get_stored_access_data():
    if len(StoreAccess.query.all()) > 0:
        access = db.session.query(StoreAccess).order_by(StoreAccess.id.desc()).first()
        if access:
            return True, access
    return False, 0


"""
=================================
Func: Store Access Data
=================================
"""
def store_access_data(request_token=None,request_token_secret=None):
    ok, access = get_stored_access_data()
    
    # If a record already exists update
    if ok:
        access.request_token = request_token
        access.request_token_secret = request_token_secret
    # Else create a new record
    else:
        access = StoreAccess(
            request_token=request_token, 
            request_token_secret=request_token_secret, 
        )
    db.session.add(access)
    db.session.commit()
    return access


"""
=================================
Job: Tweetor Countdown Example
=================================
"""
def tweetor_countdown(arg, message, end_date):

    ok, access = get_stored_access_data()
    if not ok:
        print("Error: Could not perform Tweetor job, No access data found. Twitter Authorization required!")
        return
        
    dt = datetime.datetime.now()
    tweet = f"[ auto tweet 🐦 : {dt}  ]\n\n"

    # Countdown -----------------
    today = datetime.date.today()
    yy, mm, dd = end_date.split(' ')[0].split('-')
    future = datetime.date(int(yy),int(mm), int(dd))
    daysleft = (future - today).days
    # Countdown -----------------

    tweet = f"{tweet}{daysleft} {message}"
    ok, result = tweetor.tweet(access, tweet)
    print(arg, (ok, result))


"""
=================================
Job: Tweetor Default Example
=================================
"""
def tweetor_default(arg, message, gpt_use, gpt_prompt, gpt_prompt_topic):
    ok, access = get_stored_access_data()
    if not ok:
        print("Error: Could not perform Tweetor job, No access data found. Twitter Authorization required!")
        return
        
    dt = datetime.datetime.now()
    tweet = f"[ auto tweet 🐦 : {dt}  ]\n\n"
    gpt_msg = ""
    
    # GPT-3 -----------------
    if gpt_use:
        openai.api_key = config.GPT_API_KEY
        engines = openai.Engine.list()
        completion = openai.Completion.create(engine="text-davinci-002", prompt=gpt_prompt)
        gpt_msg = f"\n[ gpt-3 👾 generated message - topic: {gpt_prompt_topic[:12]}.. ]\n\n..."+(completion.choices[0].text).replace('\n',' ')+" ..."
    # GPT-3 -----------------        
    
    tweet = tweet+message+gpt_msg
    ok, result = tweetor.tweet(access, tweet)
    print(arg, (ok, result))


"""
=================================
Endpoint: Help
=================================
"""
@app.route('/help/<string:setting>', methods=['GET'])
def help(setting):
    if setting == 'date':
        settings = [{'date':['run_date', 'timezone']}]
    elif setting == 'interval':
        settings = [{'interval':['weeks', 'days', 'hours', 'minutes', 'seconds', 'start_date', 'end_date', 'timezone']}]
    elif setting == 'cron':
        settings = [{'cron':['year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second', 'start_date', 'end_date', 'timezone']}]
    else:
        return jsonify(success=False, error=f"Setting: '{setting}' is not supported. Use: 'date', 'interval' or 'cron'.")
    return jsonify(success=True, settings=settings)


"""
=================================
Endpoint: Remove all Tweetors
=================================
"""
@app.route('/remove_all', methods=['GET'])
def remove_all():
    try:
        scheduler.remove_all_jobs()
    except:
        return jsonify(success=False, error=f"Could not remove Tweetors. Does any exist?")
    return jsonify(success=True, message="Successfully removed all Tweetors.")


"""
=================================
Endpoint: Remove Tweetor
=================================
"""
@app.route('/remove_tweetor/<string:id>', methods=['GET'])
def remove_tweetor(id):
    try:
        scheduler.remove_job(id)
    except:
        return jsonify(success=False, error=f"Could not remove Tweetor with id '{id}'. Does it exist?")
    return jsonify(success=True, message=f"Successfully removed Tweetor with id '{id}'.")


"""
=================================
Endpoint: List Current Tweetors
=================================
"""
@app.route('/list_tweetors', methods=['GET'])
def list_tweetors():
    tweetors = []
    for tweetor in scheduler.get_jobs():
        tweetors.append({
            "tweetor_name": tweetor.id,
            "tweetor_message": tweetor.args[1]
        })
    if len(tweetors) <= 0:
        return jsonify(success=False, tweetors=[])
    return jsonify(success=True, tweetors=tweetors)


"""
=================================
Endpoint: Create Tweetor
=================================
"""
@app.route('/create_tweetor', methods=['POST'])
def create_tweetor():
    # Check if access data exist
    ok, _ = get_stored_access_data()
    if not ok:
        return jsonify(success=ok, error="No access data found. Twitter Authorization required!")
    
    if not request.is_json:
        return jsonify(success=False, error="Expected json body.")

    # Get Tweetor data from POST
    args = request.json
    interval = args['interval']

    gpt_use = args['gpt_use']
    gpt_prompt = args['gpt_prompt']
    gpt_prompt_topic = args['gpt_prompt_topic']

    ttype = args['tweetor_type']
    tname = args['tweetor_name']
    tmessage = args['tweetor_message']
    print(interval['days'],interval['hours'],interval['minutes'],interval['seconds'])

    try:
        # Default Tweetor Job
        if ttype == 0:

            # Handle errs here before passing job data
            # ...

            # Create
            tweetor = scheduler.add_job(
                    func=tweetor_default,
                    seconds=interval['seconds'],
                    minutes=interval['minutes'],
                    hours=interval['hours'],
                    days=interval['days'],
                    trigger="interval",
                    id=tname,
                    replace_existing=False,
                    args=("tweet", tmessage, gpt_use, gpt_prompt, gpt_prompt_topic)
            )
        # Custom Tweetor Job
        else:

            # Handle errs here before passing job data
            start_date = interval['start_date']
            end_date = interval['end_date']
            if len(start_date) < 19:
                raise Exception(f"Invalid start_date format '{start_date}'")
            if len(end_date) < 19:
                raise Exception(f"Invalid end_date format '{end_date}'")

            # Create
            tweetor = scheduler.add_job(
                    func=tweetor_countdown,
                    start_date=interval['start_date'],
                    end_date=interval['end_date'],
                    seconds=interval['seconds'],
                    minutes=interval['minutes'],
                    hours=interval['hours'],
                    days=interval['days'],
                    trigger="interval",
                    id=tname,
                    replace_existing=False,
                    args=("tweet", tmessage, interval['end_date'])
            )            
    except Exception as e:
        return jsonify(
            success=False, error=f"Could not create Tweetor with id '{tname}'. Details: {e}")
    return jsonify(success=True, new_tweetor=tweetor.name)


"""
=================================
Endpoint: Authenticate
=================================
"""
@app.route("/authenticate/", methods=['GET'])
def authenticate():
    args = request.args
    token = args.get('oauth_token')
    verifier = args.get('oauth_verifier')

    # Check if access data exist
    ok, access = get_stored_access_data()
    if not ok:
        return jsonify(success=ok, error="No access data found. Twitter Authorization required!")
    
    # Reinit Tweetors OAuth1UserHandler    
    ok, result = tweetor.reinit_tweetor(verifier, access)
    if not ok:
        return jsonify(success=ok, error=str(result))

    # Update record with new access tokens
    access.oauth_verifier = verifier
    access.oauth_access_key=result[0]           # access_token
    access.oauth_access_key_secret=result[1]    # access_token_secret
    db.session.add(access)
    db.session.commit()

    return jsonify(success=True, message="Successfully Authorized App.")


"""
=================================
Endpoint: Authorize App
=================================
"""
@app.route("/authorize", methods=['POST', 'GET'])
def authorize():
    ok, access = get_stored_access_data()
    if not ok:
        return redirect("/")
    
    # Init Tweetors OAuth1UserHandler with provided callback url
    ok, result, handler = tweetor.init_tweetor(access.callback)
    if not ok:
        return jsonify(success=ok, error=str(result))
    else:
        # Store these for use during authentication
        request_token = handler.request_token["oauth_token"]
        request_token_secret = handler.request_token["oauth_token_secret"]
        access = store_access_data(request_token, request_token_secret)

        return redirect(result)


"""
=================================
Endpoint: Start Page
=================================
"""
@app.route('/start_page', methods=['POST','GET'])
def start_page():
    if request.method == 'POST':
        # Get Akash uri
        callback = request.form['callback']
        
        # No records yet, so create a new record 
        # and only store Akash uri for now
        access = store_access_data()
        access.callback = str(callback)
        db.session.add(access)
        db.session.commit()
        return redirect('/authorize')

    if request.method == 'GET':
        return render_template("index.html")


"""
=================================
Endpoint: Home
=================================
"""
@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    return redirect('/start_page')


"""
=================================
Endpoint: App Entrypoint
=================================
"""
if __name__ == "__main__":
    db.create_all()
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=False, host="0.0.0.0", port=config.PORT)