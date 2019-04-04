import os, json
import asyncio

from flask import render_template, flash
from werkzeug.utils import secure_filename

from flask import Flask, g, session, redirect, request, url_for, jsonify
from requests_oauthlib import OAuth2Session

import pandas as pd

from helper import DATA_DIR, STUD_FILE, LOG_FILE, DEBUG
# from bots.mgmt import run_command as mgmt_bot
# from bots.reply import run_command as reply_bot

''' Constants '''
BASE_URL = os.environ['URL']
DISCORD_CLIENT_ID = os.environ['CLIENT_ID']
DISCORD_CLIENT_SECRET = os.environ['CLIENT_SECRET']
DISCORD_REDIRECT_URI = BASE_URL + '/callback'
if 'http://' in DISCORD_REDIRECT_URI: os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

API_BASE_URL = 'https://discordapp.com/api'
AUTHORIZATION_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'


ALLOWED_EXTENSIONS = set(['xlsx'])

MSGs = {
    'error': 'Some error accured. Please try again!',
    'success': 'That, somehow worked! Good on you mate!',
    'invite': 'Only xlsx files are allowed. The students will be invited to join the server',
    'add': 'add a new channel to the Server',
    'assign': 'assign a role to someone'
}

''' app consts '''
app = Flask(__name__)
app.debug = DEBUG
app.config['DATA_DIR'] = DATA_DIR
app.config['DATA_FILE'] = STUD_FILE
app.config['SECRET_KEY'] = DISCORD_CLIENT_SECRET


''' Routes '''

@app.route('/')
def main(): 
    # if session.get('oauth2_token'): return redirect(url_for('logged'))
    return render_template('index.html', base_url=BASE_URL)
@app.route('/index')
def base():
    # if session.get('oauth2_token'): return redirect(url_for('logged'))
    return render_template('index.html', base_url=BASE_URL)

@app.route('/logged')
def logged(): return render_template('logged.html', base_url=BASE_URL)

@app.route('/course/<msg>')
def course(msg): return render_template('course.html', base_url=BASE_URL, message=MSGs[msg])

@app.route('/assign_batch/<msg>')
def assign_batch(msg): return render_template('assign_batch.html', base_url=BASE_URL, message=MSGs[msg])

@app.route('/assign_course/<msg>')
def assign_course(msg): return render_template('assign_course.html', base_url=BASE_URL, message=MSGs[msg])

@app.route('/assign_rep/<msg>')
def assign_rep(msg): return render_template('assign_rep.html', base_url=BASE_URL, message=MSGs[msg])

@app.route('/batch/<msg>')
def batch(msg): return render_template('batch.html', base_url=BASE_URL, message=MSGs[msg])

@app.route('/invite/<msg>')
def invite(msg):
    return render_template(
        'invite.html', 
        base_url=BASE_URL, 
        message=MSGs[msg]
    )


''' Form Submits '''

@app.route('/invite_submit', methods=['POST'])
def invite_submit():
    if request.method == 'POST':
        f = request.files['file']
    if '.xlsx' not in f.filename or '.xls' not in f.filename: return redirect(url_for('invite/error'))
    df = pd.read_excel(f.filename,engine='xlrd' )
    data = []
    name,roll,batch,netID,rep,year = df['Name'],df['Roll'],df['Batch'],df['NetID'],df['Rep'],df['Year']
    for i in range(len(name)):
        data.append({
            'name': name[i], 
            'roll': roll[i], 
            'year': int(year[i]), 
            'netID': netID[i], 
            'otp': '', 
            'batch': int(batch[i]), 
            'rep': rep[i], 
            'courses': {
                'past': [],
                'current': []
            },
            'discord_uid': '', 
            'nickname': '', 
            'enrolled': True
        })
    with open(STUD_FILE,'w') as f: json.dump(data,f)
    sent = mgmt_bot('add_to_server') # ERROR: No async-await in flask
    if sent: return redirect(url_for('invite', msg='success'))
    return redirect(url_for('invite', msg='error'))

# TODO
@app.route('/create_course', methods=['POST'])
def create_course():
    channel_name = request.form['channel_name']
    channel_id = request.form['channel_id']
    print('create course is called')
    return 'Channel Created for {} - {} '.format(channel_name, channel_id)

# TODO
@app.route('/assign_students', methods=['POST'])
def assign_students_course():
    if request.method == 'POST':
        f = request.files['file']
    if '.xlsx' not in f.filename or '.xls' not in f.filename:
        return 'Invalid file uploaded'
    count = len(os.listdir(app.config['DATA_DIR']))
    f.save(os.path.join(app.config['DATA_DIR'], str(count)+'.xlsx'))
    xl_file = pd.ExcelFile(app.config['DATA_DIR']+'/{}.xlsx'.format(count))
    dfs = pd.read_excel(xl_file, sheet_name=None)

    print('assign students course is called')

    return 'file uploaded successfully'

# TODO
@app.route('/assign_students_batch', methods=['POST'])
def assign_students_batch():
    if request.method == 'POST':
        f = request.files['file']
    if '.xlsx' not in f.filename or '.xls' not in f.filename:
        return 'Invalid file uploaded'
    count = len(os.listdir(app.config['DATA_DIR']))
    f.save(os.path.join(app.config['DATA_DIR'], str(count)+'.xlsx'))
    xl_file = pd.ExcelFile(app.config['DATA_DIR']+'/{}.xlsx'.format(count))
    dfs = pd.read_excel(xl_file, sheet_name=None)

    print('assign students batch is called')

    return 'file uploaded successfully'

# TODO
@app.route('/assign_student_rep', methods=['POST'])
def assign_students_rep():
    if request.method == 'POST':
        f = request.files['file']
    if '.xlsx' not in f.filename or '.xls' not in f.filename:
        return 'Invalid file uploaded'
    count = len(os.listdir(app.config['DATA_DIR']))
    f.save(os.path.join(app.config['DATA_DIR'], str(count)+'.xlsx'))
    xl_file = pd.ExcelFile(app.config['DATA_DIR']+'/{}.xlsx'.format(count))
    dfs = pd.read_excel(xl_file, sheet_name=None)

    print('assign students rep is called')

    return 'file uploaded successfully'

# TODO
@app.route('/create_batch', methods=['POST'])
def create_batch():
    batch = request.form['batch']
    print(batch)
    return 'success !!!! HAHA !!!!'


''' Discord OAuth2 '''

def token_updater(token): session['oauth2_token'] = token

def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=DISCORD_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=DISCORD_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': DISCORD_CLIENT_ID,
            'client_secret': DISCORD_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)

@app.route('/auth')
def auth():
    scope = request.args.get('scope','identify')
    discord = make_session(scope=scope.split(' '))
    authorization_url, state = discord.authorization_url(AUTHORIZATION_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    if request.values.get('error'): return request.values['error']
    discord = make_session(state=session.get('oauth2_state'))
    token = discord.fetch_token(
        TOKEN_URL,
        client_secret=DISCORD_CLIENT_SECRET,
        authorization_response=request.url
    )
    session['oauth2_token'] = token
    return redirect(url_for('.me'))

@app.route('/me')
def me():
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    guilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()
    connections = discord.get(API_BASE_URL + '/users/@me/connections').json()
    return redirect(url_for('logged'))



if __name__ == '__main__':
    # Start Bots
    # from bots import mgmt, reply
    # mgmt.bot.run(os.environ['BU_MGMT'])
    # reply.bot.run(os.environ['BUHACK_GIFT'])
    
    # Start server
    session.clear()
    app.run(host='127.0.0.1', port=int('5000'))