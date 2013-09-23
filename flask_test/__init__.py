#!/usr/bin/env python

from flask import Flask
from cbssports import API

app = Flask(__name__, template_folder='templates')
api = API(response_format='JSON')

from flask_test import views
