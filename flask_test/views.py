#!/usr/bin/env python
import json
from inspect import getmembers

from flask import request, render_template

from flask_test import app, api
from cbssports import CBSSportsError


@app.route('/test')
def index():
    print 'projections 2013'
    r = api.general.stats(period='projections', timeframe='2013', player_id='1616817')
    print json.dumps(r.json(), indent=4, separators=(', ', '; '))

    print 'projections, 4'
    r = api.general.stats(period='projections', timeframe='2013', player_id='1616817')
    print json.dumps(r.json(), indent=4, separators=(', ', '; '))

    print 'ytd'
    r = api.general.stats(period='ytd', timeframe='2013', player_id='1616817')
    print json.dumps(r.json(), indent=4, separators=(', ', '; '))
    return render_template('test.html')


@app.route('/test2')
def index2():
    try:
        players = ['1616817']
        r = api.league.stats(player_id=players)
    except CBSSportsError as inst:
        print inst
    else:
        print r
        print r.url

        #turns the json response into a python object
        decoder = json.JSONDecoder()
        league_details = decoder.decode(r.text)
        print league_details.keys()

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

    url_methods = [x.replace('__', '-').replace('_', '.').replace('.', '/') for x in methods]
    return render_template('list_methods.html', methods=url_methods)
