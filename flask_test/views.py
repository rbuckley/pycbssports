#!/usr/bin/env python
import json
from inspect import getmembers

from flask import request, render_template

from flask_test import app, api


@app.route('/test')
def index():
    r = api.general.stats(period='ytd', timeframe='2013')
    print r
    print r.url

    #print json.dumps(r.json(), indent=4, separators=(', ', '; '))
    return render_template('test.html')


@app.route('/test2')
def index2():
    r = api.league.stats(player_id='12345')
    print r
    print r.url

    # turns the json response into a python object
    decoder = json.JSONDecoder()
    league_details = decoder.decode(r.text)
    #print league_details.keys()


    print json.dumps(r.json(), indent=4, separators=(', ', '; '))
    return render_template('test.html')


@app.route('/')
def home():
    if api.access_token is None:
        access_token = request.args.get('access_token')
        api.set_access_token(access_token)
    methods = []
    members = [x for x in getmembers(api)]
    groups = [group for group in members if repr(group[1]).count("Group") and group[0] is not '__dict__']
    for group in groups:
        methods += ['%s.%s' % (group[0], x[0]) for x in getmembers(group[1]) if not x[0].startswith('_')]

    return render_template('list_methods.html', methods=methods)
