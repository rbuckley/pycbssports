#!/usr/bin/env python
#
# pycbssports - Python bindings for the CBSSports Developer API
#
#
#
import requests

VERSION = '0.001a'

CBSSPORTS_URL = 'http://api.cbssports.com/fantasy'
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
    'league': {
        'news': {
            'story': [
            ],
            'headlines': [
            ]
        }, # league.news
        'transaction_list': {
            'add_drops': [
            ],
            'trades': [
            ],
            'log': [
            ]
        }, # league.transaction-list
        'transactions': {
            'add_drop': [
            ],
            'lineup': [
            ],
            'trade': [
            ],
            'waiver_order': [
            ]
        }, # league.transactions
        'scoring': {
            'live': [
            ],
            'preview': [
            ],
            'categories': [
            ],
            'rules': [
            ]
        }, # league.scoring
        'standings': {
            'breakdown': [
            ],
            'by_period': [
            ],
            'overall': [
            ],
            'power': [
            ]
        }, # league.standings
        'draft': {
            'config': [
            ],
            'order': [
            ],
            'results': [
            ]
        } # league.draft 
    }, # end of the league methods
    # stats methods
    'stats': {
        'defense_vs_position': [
        ],
        'situational_stats': [
        ],
        'categories': [
        ]
    }, 
    'players': {
        'average_draft_position': [
        ],
        'gamelog': [
        ],
        'inactives': [
        ],
        'injuries': [
        ],
        'list': [
        ],
        'outlook': [
        ],
        'profile': [
        ],
        'rankings': [
        ],
        'search': [
        ],
        'updates': [
        ]
    }, # players
    'roster_trends': {
        'most_activated': [
        ],
        'most_added': [
        ],
        'most_benched': [
        ],
        'most_dropped': [
        ],
        'most_owned': [
        ],
        'most_started': [
        ],
        'most_traded': [
        ],
        'most_viewed': [
        ]
    }, # players.roster-trends
    'general': {
        'auction_values': [
        ],
        'stats': [
        ],
        'positions': [
        ],
        'pro_teams': [
        ],
        'sports': [
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

        args['access_token'] = self.access_token
        args['version'] = CBSSPORTS_API_VERSION
        args['format'] = JSON_RESPONSE_FORMAT
        return args
    
    def _build_url(self, parts):
        return CBSSPORTS_URL + parts.replace('.', '/')
