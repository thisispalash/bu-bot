from flask import Flask, render_template
from flask import json
import globals
from home inport home

app = Flask(__name__)

app.register_blueprint(home)

@app.route("/")
def main():
    return render_template('index.html', base_url = globals.base_url)

@app.route("/home")
def home():
	return render_template('index.html', base_url = globals.base_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("80"),debug = True)

