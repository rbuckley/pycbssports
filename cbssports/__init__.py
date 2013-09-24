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
    'league': {
        'owners': [
            ('response_format', str, ['optional'])
        ],
        'teams': [
            ('response_format', str, ['optional'])
        ],
        'dates': [
            ('response_format', str, ['optional'])
        ],
        'details': [
            ('response_format', str, ['optional'])
        ],
        'rules': [
            ('response_format', str, ['optional'])
        ],
        'schedules': [
            ('response_format', str, ['optional'])
        ],
        'rosters': [
            ('response_format', str, ['optional'])
        ],
        'fantasy__points': [
            ('response_format', str, ['optional'])
        ],
        'stats': [
            ('response_format', str, ['optional'])
        ]
    },
    'league_news': {
        'story': [
            ('response_format', str, ['optional'])
        ],
        'headlines': [
            ('response_format', str, ['optional'])
        ]
    },  # league.news
    'league_transaction__list': {
        'add__drops': [
            ('response_format', str, ['optional'])
        ],
        'trades': [
            ('response_format', str, ['optional'])
        ],
        'log': [
            ('response_format', str, ['optional'])
        ]
    },  # league.transaction-list
    'league_transactions': {
        'add__drop': [
            ('response_format', str, ['optional'])
        ],
        'lineup': [
            ('response_format', str, ['optional'])
        ],
        'trade': [
            ('response_format', str, ['optional'])
        ],
        'waiver__order': [
            ('response_format', str, ['optional'])
        ]
    },  # league.transactions
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
    },  # league.scoring
    'league_standings': {
        'breakdown': [
            ('response_format', str, ['optional'])
        ],
        'by__period': [
            ('response_format', str, ['optional'])
        ],
        'overall': [
            ('response_format', str, ['optional'])
        ],
        'power': [
            ('response_format', str, ['optional'])
        ]
    },  # league.standings
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
    },  # league.draft
    # stats methods
    'stats': {
        'defense__vs__position': [
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
        'average__draft__position': [
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
    },  # players
    'players_roster__trends': {
        'most__activated': [
            ('response_format', str, ['optional'])
        ],
        'most__added': [
            ('response_format', str, ['optional'])
        ],
        'most__benched': [
            ('response_format', str, ['optional'])
        ],
        'most__dropped': [
            ('response_format', str, ['optional'])
        ],
        'most__owned': [
            ('response_format', str, ['optional'])
        ],
        'most__started': [
            ('response_format', str, ['optional'])
        ],
        'most__traded': [
            ('response_format', str, ['optional'])
        ],
        'most__viewed': [
            ('response_format', str, ['optional'])
        ]
    },  # players.roster-trends
    'general': {
        'auction__values': [
            ('response_format', str, ['optional'])
        ],
        'stats': [
            ('response_format', str, ['optional']),
            ('timeframe', str, ['allowed', ('YYYY')]),
            ('period', str, ['allowed', ('ytd', '3yr', 'YYYYMMDD')]),
            ('player_id', str, ['optional']),
        ],
        'positions': [
            ('response_format', str, ['optional'])
        ],
        'pro__teams': [
            ('response_format', str, ['optional'])
        ],
        'sports': [
            ('response_format', str, ['optional'])
        ]
    },  # general methods with no group
}


def generate_cbssports_method(namespace, method_name, param_data):
    """
    given the above data parse it into a function that will
    check parameters
    """
    required = []
    for param in param_data:
        if 'optional' not in param[2]:
            required.append(param)
            print param[0] + ' is required'
        if 'allowed' in param[2]:
            print 'allowed values for: ' + param[0] + ': ' + repr(param[2][1:])

    def cbssports_method(self, *args, **kwargs):
        params = {}
        for i, arg in enumerate(args):
            params[param_data[i][0]] = arg
        params.update(kwargs)

        for param in required:
            if param[0] not in params:
                raise TypeError('missing parameter %s' % param[0])

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
        print ('name: ' + name + ' client: ' + repr(client))
        self._client = client
        self._name = name

    def __call__(self, method=None, args=None):
        print ('from %s calling method: %s' % (self._name, method))
        if method is None:
            return self
        return self._client('%s.%s' % (self._name, method), args)


def generate_methods(args):
    # loop over all the groups in the METHODS table
    for namespace in args:
        print namespace
        methods = {}
        # loop over each method in each group and process it
        for method, param_data in args[namespace].iteritems():
            methods[method] = generate_cbssports_method(namespace, method, param_data)
            #print methods[method].__name__

        print('creating new class: %sGroup' % namespace.title())
        # need to add our new functions to the globals so they can be used later
        group = type('%sGroup' % namespace.title(), (Group,), methods)

        globals()[group.__name__] = group

generate_methods(METHODS)

class CBSSportsError(Exception):
    """ Exception class for custom errors """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class API(object):

    def __init__(self, response_format=None, access_token=None):
        """
        Provides access to the CBSSPORTS Development API

        Instance Variables:
            access_token:
                When the app is first opened this will be passed in and must be passed
                with each method call

            default_response:
                Optional, will set the format of responses to either JSON or XML
        """


        self.access_token = access_token
        if response_format == 'JSON' or response_format == 'XML':
            self.default_response = response_format
        else:
            raise ValueError("%s not allowed for default_response, only JSON or XML" % response_format)

        # assign all the functions to this class
        for namespace in METHODS:
            self.__dict__[namespace] = eval('%sGroup(self, \'%s\')' % (namespace.title(), '%s' % namespace))

    def __call__(self, method=None, args=None):
        """Do the actual call to the REST api"""
        if self.access_token is None:
            raise CBSSportsError("access_token must be set before making an API call")

        if method is None:
            return self

        method = self._fix_method_name(method)

        args = self._build_args(args)

        url = self._build_url(method)
        return requests.get(url, params=args)

    def set_access_token(self, access_token):
        """Set the access_token if not already done"""
        self.access_token = access_token

    def _build_args(self, args=None):
        """Attach args that need to be with every query"""
        if args is None:
            args = {}

        response_set = 'response_format' in args.keys()

        for arg in args:
            pass

        args['version'] = CBSSPORTS_API_VERSION
        args['access_token'] = self.access_token

        # if a response format was passed in on initialization use it
        # otherwise we do not pass the argument which results in xml response
        if not response_set and self.default_response == 'JSON':
            args['response_format'] = JSON_RESPONSE_FORMAT

        return args

    def _fix_method_name(self, method):
        """
        Some methods need to be fixed, _s need to be replaced with -s
        Or .s need to be put in
        Or if it starts with general, remove it  all
        """

        return method.replace('__', '-').replace('_', '.').replace('general.', '')

    def _build_url(self, parts):
        """Returns the url with .s replaced by /s"""
        return CBSSPORTS_URL + parts.replace('.', '/')
