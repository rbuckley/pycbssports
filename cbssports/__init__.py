#!/usr/bin/env python
#
# pycbssports - Python bindings for the CBSSports Developer API
#
#
#
import requests

VERSION = '0.001a'

CBSSPORTS_URL = 'http://api.cbssports.com/fantasy/'
CBSSPORTS_API_VERSION = '2.0'
JSON_RESPONSE_FORMAT = 'JSON'
XML_RESPONSE_FORMAT = 'XML'


# METHODS follows this
#       'namespace1': {
#           'method1': [
#               (name, klass, [options]),
#               (name, klass, [options])
#           ],
#           'method2: [
#               (name, klass, [options])
#           ]set syntax
#       },
#       'namespace2:{
#       ...
#       ...

METHODS = {
    # league methods
    'league_news': {
        'story': [
            ('response_format', str, ['optional'])
        ],
        'headlines': [
            ('response_format', str, ['optional'])
        ]
    }, # league.news
    'league_transaction_list': {
        'add_drops': [
            ('response_format', str, ['optional'])
        ],
        'trades': [
            ('response_format', str, ['optional'])
        ],
        'log': [
            ('response_format', str, ['optional'])
        ]
    }, # league.transaction-list
    'league_transactions': {
       'add_drop': [
            ('response_format', str, ['optional'])
        ],
        'lineup': [
            ('response_format', str, ['optional'])
        ],
        'trade': [
            ('response_format', str, ['optional'])
        ],
        'waiver_order': [
            ('response_format', str, ['optional'])
        ]
    }, # league.transactions
    'league_scoring': {
        'live': [
            ('response_format', str, ['optional'])
        ],
        'preview': [
            ('response_format', str, ['optional'])
        ],
        'categories': [
            ('response_format', str, ['optional'])
        ],
        'rules': [
            ('response_format', str, ['optional'])
        ]
    }, # league.scoring
    'league_standings': {
       'breakdown': [
            ('response_format', str, ['optional'])
        ],
        'by_period': [
            ('response_format', str, ['optional'])
        ],
        'overall': [
            ('response_format', str, ['optional'])
        ],
        'power': [
            ('response_format', str, ['optional'])
        ]
    }, # league.standings
    'league_draft': {
        'config': [
            ('response_format', str, ['optional'])
        ],
        'order': [
            ('response_format', str, ['optional'])
        ],
        'results': [
            ('response_format', str, ['optional'])
        ]
    }, # league.draft 
    # stats methods
    'stats': {
        'defense_vs_position': [
            ('response_format', str, ['optional'])
        ],
        'situational_stats': [
            ('response_format', str, ['optional'])
        ],
        'categories': [
            ('response_format', str, ['optional'])
        ]
    }, 
    'players': {
        'average_draft_position': [
            ('response_format', str, ['optional'])
        ],
        'gamelog': [
            ('response_format', str, ['optional'])
        ],
        'inactives': [
            ('response_format', str, ['optional'])
        ],
        'injuries': [
            ('response_format', str, ['optional'])
        ],
        'list': [
            ('response_format', str, ['optional'])
        ],
        'outlook': [
            ('response_format', str, ['optional'])
        ],
        'profile': [
            ('response_format', str, ['optional'])
        ],
        'rankings': [
            ('response_format', str, ['optional'])
        ],
        'search': [
            ('response_format', str, ['optional'])
        ],
        'updates': [
            ('response_format', str, ['optional'])
        ]
    }, # players
    'roster_trends': {
        'most_activated': [
            ('response_format', str, ['optional'])
        ],
        'most_added': [
            ('response_format', str, ['optional'])
        ],
        'most_benched': [
            ('response_format', str, ['optional'])
        ],
        'most_dropped': [
            ('response_format', str, ['optional'])
        ],
        'most_owned': [
            ('response_format', str, ['optional'])
        ],
        'most_started': [
            ('response_format', str, ['optional'])
        ],
        'most_traded': [
            ('response_format', str, ['optional'])
        ],
        'most_viewed': [
            ('response_format', str, ['optional'])
        ]
    }, # players.roster-trends
    'general': {
        'auction_values': [
            ('response_format', str, ['optional'])
        ],
        'stats': [
            ('response_format', str, ['optional'])
        ],
        'positions': [
            ('response_format', str, ['optional'])
        ],
        'pro_teams': [
            ('response_format', str, ['optional'])
        ],
        'sports': [
            ('response_format', str, ['optional'])
        ]
    }, # general methods with no group
}


def generate_cbssports_method(namespace, method_name, param_data):
    #print ('Group: ' + namespace + ', method: ' + method_name + ', params: ')

    # a required option does not have 'optional' in the third tuple(options)
    required = [x for x in param_data
                if 'optional' not in x[2]
                ]

    def cbssports_method(self, *args, **kwargs):
        params = {}
        for i, arg in enumerate(args):
            params[param_data[i][0]] = arg
        params.update(kwargs)

        for param in required:
            if param[0] not in params:
                raise TypeError("missing parameter %s" % param[0])

        for name, klass, options in param_data:
            pass

        return self(method_name, params)

    cbssports_method.__name__ = method_name
    cbssports_method.__doc__ = \
        "CBSSports API call. See http://www.developer.cbssports.com/documentation %s:%s" \
        % (namespace, method_name)

    return cbssports_method


class Group(object):
    """Represents a "namespace" of CBSSPORTS API Calls."""

    def __init__(self, client, name):
        print ('name: ' + name)
        self._client = client
        self._name = name

    def __call__(self, method=None, args=None):
        print ('from %s calling method: %s' % (self._name, method))
        if method is None:
            return self
        return self._client('%s.%s' % (self._name, method), args)


def generate_methods():
    # loop over all the groups in the METHODS table
    for namespace in METHODS:
        methods = {}
        # loop over each method in each group and process it
        for method, param_data in METHODS[namespace].iteritems():
            methods[method] = generate_cbssports_method(namespace, method, param_data)
            print methods[method].__name__

        print('creating new class: %sGroup' % namespace.title())
        # need to add our new functions to the globals so they can be used later
        group = type('%sGroup' % namespace.title(), (Group,), methods)

        globals()[group.__name__] = group

generate_methods()


class API(object):

    def __init__(self, access_token=None):
        self.access_token = access_token
        
        # assign all the functions to this class
        for namespace in METHODS:
            self.__dict__[namespace] = eval('%sGroup(self, \'%s\')' % (namespace.title(), '%s' % namespace))

    def __call__(self, method=None, args=None):
        """Do the actual call to the REST api"""
        if method is None:
            return self

        args = self._build_args(method, args)
        
        url = self._build_url(method)
        return requests.get(url, params=args)

    def _build_args(self, method=None, args=None):
        if args is None:
            args = {}

        for arg in args:
            pass

        args['version'] = CBSSPORTS_API_VERSION
        args['access_token'] = self.access_token
        args['response_format'] = JSON_RESPONSE_FORMAT
        return args
    
    def _build_url(self, parts):
        return CBSSPORTS_URL + parts.replace('.', '/')
