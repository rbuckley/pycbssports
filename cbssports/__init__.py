#!/usr/bin/env python
#
# pycbssports - Python bindings for the CBSSports Developer API
#
#
#
import requests
import datetime

VERSION = '0.001a'

CBSSPORTS_URL = 'http://api.cbssports.com/fantasy/'
CBSSPORTS_API_VERSION = '2.0'
JSON_RESPONSE_FORMAT = 'JSON'
XML_RESPONSE_FORMAT = 'XML'

ALLOWED_TIMEFRAME = ('season', 'weekly')
ALLOWED_SOURCE = ('cbs', 'dave_richard', 'jamey_eisenberg', 'nathan_zegura')
ALLOWED_TYPE = ('by_pos', 'overall')
ALLOWED_TEAM_TYPE = ('roster', 'scout')
ALLOWED_UPDATE_TYPE = ('hot', 'cold', 'normal')
ALLOWED_PLAYER_STATUS = ('all', 'free_agents', 'owned')
ALLOWED_POSITIONS = ('QB', 'RB', 'WR', 'TE', 'K', 'DST', 'all')
ALLOWED_VIEW = ('playerbreakdown', 'teambreakdown')
ALLOWED_STATS_TYPE = ('stats', 'projections', 'redzone')
ALLOWED_SITUATIONS = ('win-loss', 'home-road', 'venue', 'conf', 'div', 'playing-surface', 'overall', 'vs-opponent', 'postseason')
ALLOWED_TX_FILTERS = ('trades', 'lineup', 'add_drops', 'waivers', 'billable', 'custom', 'all_but_lineup', 'all')


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
            ('response_format', str, ['optional']),
            ('period', str, ['optional']),
            ('team_id', int, ['optional']),
        ],
        'rosters': [
            ('response_format', str, ['optional']),
            ('team_id', int, ['optional']),
            ('point', int, ['optional']),
            ('period', int, ['optional']),
        ],
        'fantasy__points': [
            ('response_format', str, ['optional']),
            ('timeframe', str, []),
            ('period', str, []),
            ('player_id', int, ['optional']),
        ],
        'stats': [
            ('response_format', str, ['optional']),
            ('limit', int, ['optional']),
            ('offset', int, ['optional']),
            ('player_id', int, ['optional']),
            ('player_status', str, ['optional']),
            ('position', str, ['optional']),
            ('timeframe', str, ['optional']),
            ('period', str, ['optional']),
            ('stats_type', str, ['optional']),
            ('source', str, ['optional']),
            ('team_id', int, ['optional']),
            ('team_type', str, ['optional']),
            ('pro_or_fantasy', str, ['optional']),
        ]
    },
    'league_fantasy__points': {
        'weekly__scoring': [
            ('response_format', str, ['optional']),
            ('timeframe', str, ['optional']),
            ('player_id', int, ['optional']),
            ('team_id', int, ['optional']),
            ('team_type', str, ['optional']),
            ('player_status', str, ['optional']),
            ('position', str, ['optional']),
        ],
    },
    'league_transaction__list': {
        'add__drops': [
            ('response_format', str, ['optional'])
        ],
        'trades': [
            ('response_format', str, ['optional'])
        ],
        'log': [
            ('response_format', str, ['optional']),
            ('filter', str, ['optional']),
            ('team_id', int, ['optional']),
        ]
    },
    # these methods can make changes to the league, might require special
    # groups
    'league_transactions': {
        'add__drop': [
            ('response_format', str, ['optional']),
            ('id', str, ['optional']),
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
            ('response_format', str, ['optional']),
            ('team_id', int, ['optional']),
            ('period', str, ['optional']),
            ('no_players', bool, ['optional']),
        ],
        'preview': [
            ('response_format', str, ['optional']),
            ('matchup_id', str, ['optional']),
            ('team_id', int, ['optional']),
            ('period', str, ['optional']),
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
            ('response_format', str, ['optional']),
            ('period', int, ['optional']),
        ],
        'by__period': [
            ('response_format', str, ['optional']),
            ('period', int, ['optional']),
        ],
        'overall': [
            ('response_format', str, ['optional']),
            ('period', int, ['optional']),
        ],
        'power': [
            ('response_format', str, ['optional']),
            ('period', str, ['optional']),
        ]
    },  # league.standings
    'league_draft': {
        'results': [
            ('response_format', str, ['optional']),
            ('round', int, ['optional']),
            ('limit', int, ['optional']),
            ('offset', int, ['optional']),
            ('suppress_player_data', int, ['optional', ('allowed', 1)]),
            ('suppress_team_data', int, ['optional', ('allowed', 1)]),
            ('suppress_round_data', int, ['optional', ('allowed', 1)]),
            ('minimum_data', int, ['optional', ('allowed', 1)]),
        ],
        'order': [
            ('response_format', str, ['optional'])
        ],
        'config': [
            ('response_format', str, ['optional'])
        ]
    },  # league.draft
    # stats methods
    'stats': {
        'defense__vs__position': [
            ('response_format', str, ['optional']),
            ('timeframe', str, ['optional']),
            ('period', str, ['optional']),
            ('position', str, ['optional']),
            ('team', str, ['optional']),
            ('view', str, ['optional']),
        ],
        'situational_stats': [
            ('response_format', str, ['optional']),
            ('timeframe', str, ['optional']),
            ('player_id', int, []),
            ('situation', str, ['optional']),
        ],
        'categories': [
            ('response_format', str, ['optional'])
        ]
    },
    'players': {
        'average__draft__position': [
            ('response_format', str, ['optional']),
            ('position', str, ['optional']),
            ('limit', str, ['optional']),
        ],
        'gamelog': [
            ('response_format', str, ['optional']),
            ('player_id', int, []),
            ('timeframe', str, []),
            ('num_games', str, ['optional']),
            ('start_date', str, ['not_valid']),   # Baseball only
            ('end_date', str, ['not_valid']),   # Baseball only
        ],
        'inactives': [
            ('response_format', str, ['optional']),
            ('period', str, [])
        ],
        'injuries': [
            ('response_format', str, ['optional']),
            ('position', str, ['optional'])
        ],
        'list': [
            ('response_format', str, ['optional'])
        ],
        'outlook': [

            ('response_format', str, ['optional']),
            ('player_id', int, [])
        ],
        'profile': [
            ('response_format', str, ['optional']),
            ('player_id', int, [])
        ],
        'rankings': [
            ('response_format', str, ['optional']),
            ('position', str, ['optional']),
            ('type', str, ['optional']),
            ('source', str, ['optional']),
            ('timeframe', str, ['optional']),
        ],
        'search': [
            ('response_format', str, ['optional']),
            ('player_id', int, ['optional']),
            ('pro_team', str, ['optional']),
            ('name', str, ['optional']),
            ('position', str, ['optional']),
            ('team_id', int, ['optional']),
            ('free_agents', str, ['optional']),
            ('owned', str, ['optional']),
            ('eligible_only', str, ['optional']),
            ('limit', int, ['optional']),
        ],
        'updates': [
            ('response_format', str, ['optional']),
            ('team_id', int, ['optional']),
            ('team_type', str, ['optional']),
            ('team_abbr', str, ['optional']),
            ('position', str, ['optional']),
            ('player_id', int, ['optional']),
            ('eligible_position', str, ['optional']),
            ('free_agents', int, ['optional']),
            ('type', str, ['optional']),
            ('limit', int, ['optional']),
        ]
    },  # players
    'players_roster__trends': {
        'most__activated': [
            ('response_format', str, ['optional']),
            ('position', str, ['optional']),
            ('player_status', str, ['optional']),
            ('limit', int, ['optional']),
        ],
        'most__added': [
            ('response_format', str, ['optional']),
            ('position', str, ['optional']),
            ('player_status', str, ['optional']),
            ('limit', int, ['optional']),
        ],
        'most__benched': [
            ('response_format', str, ['optional']),
            ('position', str, ['optional']),
            ('player_status', str, ['optional']),
            ('limit', int, ['optional']),
        ],
        'most__dropped': [
            ('response_format', str, ['optional']),
            ('position', str, ['optional']),
            ('player_status', str, ['optional']),
            ('limit', int, ['optional']),
        ],
        'most__owned': [
            ('response_format', str, ['optional']),
            ('position', str, ['optional']),
            ('player_status', str, ['optional']),
            ('limit', int, ['optional']),
        ],
        'most__started': [
            ('response_format', str, ['optional']),
            ('position', str, ['optional']),
            ('player_status', str, ['optional']),
            ('limit', int, ['optional']),
        ],
        'most__traded': [
            ('response_format', str, ['optional']),
            ('position', str, ['optional']),
            ('player_status', str, ['optional']),
            ('limit', int, ['optional']),
        ],
        'most__viewed': [
            ('response_format', str, ['optional']),
            ('position', str, ['optional']),
            ('player_status', str, ['optional']),
            ('limit', int, ['optional']),
        ]
    },  # players.roster-trends
    'fantasy_news': {
        'story': [
            ('response_format', str, ['optional']),
            ('id', int, []),
        ],
        'headlines': [
            ('response_format', str, ['optional']),
            ('limit', int, ['optional']),
            ('offset', int, ['optional']),
        ],
    },
    'fantasy_league_news': {
        'story': [
            ('response_format', str, ['optional']),
            ('id', int, []),
        ],
        'headlines': [
            ('response_format', str, ['optional']),
            ('limit', int, ['optional']),
            ('offset', int, ['optional']),
        ],
    },
    'general': {
        'auction__values': [
            ('response_format', str, ['optional']),
            ('source', str, ['optional'])
        ],
        'stats': [
            ('response_format', str, ['optional']),
            ('timeframe', str, []),
            ('period', str, []),
            ('player_id', int, ['optional']),
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


def _check_allowed(value, allowed_values):
    if not value in allowed_values:
        raise ValueError('%s is not allowed, try instead one of %s' % (value, allowed_values))


def gen_cbssports_method(namespace, method_name, param_data):
    """
    given the above data parse it into a function that will
    check parameters
    """
    required = []
    for param in param_data:
        if 'optional' not in param[2]:
            required.append(param)

    def cbssports_method(self, *args, **kwargs):
        params = {}
        for i, arg in enumerate(args):
            print 'arg: ' + repr(arg)
        params[param_data[i][0]] = arg
        params.update(kwargs)

        # check for all required args
        for param in required:
            if param[0] not in params:
                raise TypeError('%s: missing parameter %s'
                                % (method_name, param[0]))

        # check that remaining args match what we expect
        for name, klass, options in param_data:
            if name in params:
                print params[name]
            print 'arg: %s is a %s and has options %s' % (name, repr(klass), repr(options))

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
            methods[method] = gen_cbssports_method(namespace, method, param_data)
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
        print 'calling %s with args %s' % (method, repr(args))
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
