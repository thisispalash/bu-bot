from flask import Flask, render_template
from flask import json
import globals

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('login.html', base_url = globals.base_url)

@app.route("/home")
def home():
	return render_template('home.html', base_url = globals.base_url)


