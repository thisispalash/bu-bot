from flask import Flask, render_template
from flask import json
from flask import Blueprint
import globals

home = Blueprint("home", __name__)

@home.route("/home/students")
def create_students():
    return

@home.route("/home/courses")
def create_courses():
    return


