#!/usr/bin/env python

from flask import Flask, request
from cbssports import API

app = Flask(__name__)

@app.route('/')
def test():
    access_token = request.get('access_token')

    api = API(access_token)

    r = api.players.list()

    print r.json.dumps(indent=4, separators=(',',':'))
