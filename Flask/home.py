from flask import Flask, g, session, redirect, request, url_for, jsonify, render_template, flash
from requests_oauthlib import OAuth2Session
import globals
import os
import pandas as pd
from werkzeug.utils import secure_filename


app = Flask(__name__)


UPLOAD_FOLDER = 'data_files'
ALLOWED_EXTENSIONS = set(['xlsx'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def main():
    return render_template('index.html', base_url=globals.base_url)


@app.route("/index")
def base():
	return render_template('index.html', base_url=globals.base_url)


@app.route("/course")
def course():
	return render_template('course.html', base_url=globals.base_url)


@app.route("/assign_batch")
def assign_batch():
	return render_template('assign_batch.html', base_url=globals.base_url)


@app.route("/assign_course")
def assign_course():
	return render_template('assign_course.html', base_url=globals.base_url)


@app.route("/assign_rep")
def assign_rep():
	return render_template('assign_rep.html', base_url=globals.base_url)


@app.route("/batch")
def batch():
	return render_template('batch.html', base_url=globals.base_url)


@app.route("/invite")
def invite():
	return render_template('invite.html', base_url=globals.base_url)


@app.route("/invite_submit", methods=['POST'])
def invite_submit():
    if request.method == 'POST':
        f = request.files['file']
    if ".xlsx" not in f.filename or ".xls" not in f.filename:
        return "Invalid file uploaded"
    count = len(os.listdir(app.config['UPLOAD_FOLDER']))
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], str(count)+".xlsx"))
    xl_file = pd.ExcelFile(app.config["UPLOAD_FOLDER"]+"/{}.xlsx".format(count))
    dfs = pd.read_excel(xl_file, sheet_name=None)

    print(dfs)

    return 'file uploaded successfully'

@app.route("/create_course", methods=["POST"])
def create_course():
    channel_name = request.form["channel_name"]
    channel_id = request.form["channel_id"]

    return "Channel Created for {} - {} ".format(channel_name, channel_id)

@app.route("/assign_students", methods=["POST"])
def assign_students_course():
    if request.method == 'POST':
        f = request.files['file']
    if ".xlsx" not in f.filename or ".xls" not in f.filename:
        return "Invalid file uploaded"
    count = len(os.listdir(app.config['UPLOAD_FOLDER']))
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], str(count)+".xlsx"))
    xl_file = pd.ExcelFile(app.config["UPLOAD_FOLDER"]+"/{}.xlsx".format(count))
    dfs = pd.read_excel(xl_file, sheet_name=None)

    print(dfs)

    return 'file uploaded successfully'


OAUTH2_CLIENT_ID = globals.OAUTH2_CLIENT_ID
OAUTH2_CLIENT_SECRET = globals.OAUTH2_CLIENT_SECRET
OAUTH2_REDIRECT_URI = 'http://10.12.4.147/index'

API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'

app.debug = True
app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET

if 'http://' in OAUTH2_REDIRECT_URI:
    globals.OAUTHLIB_INSECURE_TRANSPORT = 'true'


def token_updater(token):
    session['oauth2_token'] = token


def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': OAUTH2_CLIENT_ID,
            'client_secret': OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)


@app.route('/auth')
def index():
    scope = request.args.get(
        'scope',
        'identify email connections guilds guilds.join')
    discord = make_session(scope=scope.split(' '))
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    if request.values.get('error'):
        return request.values['error']
    discord = make_session(state=session.get('oauth2_state'))
    token = discord.fetch_token(
        TOKEN_URL,
        client_secret=OAUTH2_CLIENT_SECRET,
        authorization_response=request.url)
    session['oauth2_token'] = token
    return redirect(url_for('.me'))


@app.route('/me')
def me():
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    guilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()
    connections = discord.get(API_BASE_URL + '/users/@me/connections').json()
    return jsonify(user=user, guilds=guilds, connections=connections)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("80"),debug = True)
