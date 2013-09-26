#!/usr/bin/env python
#
# pycbssports - Python bindings for the CBSSports Developer API
#
#
#
import requests
import datetime
import json

VERSION = '0.001a'

CBSSPORTS_URL = 'http://api.cbssports.com/fantasy/'
CBSSPORTS_API_VERSION = '2.0'

CBSSPORTS_EXCEPTION = '400'
CBSSPORTS_UNALLOWED_TYPE = 'val_not_allowed'
CBSSPORTS_ACCESS_TOKEN_ERROR = 'access_token'

ALLOWED_TIMEFRAME = ('season', 'weekly')
ALLOWED_SOURCE = ('cbs', 'dave_richard', 'jamey_eisenberg', 'nathan_zegura')
ALLOWED_TYPE = ('by_pos', 'overall')
ALLOWED_TEAM_TYPE = ('roster', 'scout')
ALLOWED_UPDATE_TYPE = ('hot', 'cold', 'normal')
ALLOWED_PLAYER_STATUS = ('all', 'free_agents', 'owned')
ALLOWED_POSITIONS = ('QB', 'RB', 'WR', 'TE', 'K', 'DST', 'all')
ALLOWED_VIEW = ('playerbreakdown', 'teambreakdown')
ALLOWED_STATS_TYPE = ('stats', 'projections', 'redzone')
ALLOWED_SITUATIONS = ('win-loss', 'home-road', 'venue', 'conf',
                      'div', 'playing-surface', 'overall',
                      'vs-opponent', 'postseason')
ALLOWED_TX_FILTERS = ('trades', 'lineup', 'add_drops', 'waivers',
                      'billable', 'custom', 'all_but_lineup', 'all')
ALLOWED_PERIOD = ('ytd', '3yr', 'projections')
ALLOWED_RESPONSE_VALUES = ('JSON', 'XML')


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
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ],
        'teams': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ],
        'dates': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ],
        'details': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ],
        'rules': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ],
        'schedules': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('period', str, {'optional': True}),
            ('team_id', int, {'optional': True}),
        ],
        'rosters': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('team_id', int, {'optional': True}),
            ('point', int, {'optional': True}),
            ('period', int, {'optional': True}),
        ],
        'fantasy__points': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('timeframe', str, []),
            ('period', str, []),
            ('player_id', int, {'optional': True}),
        ],
        'stats': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('limit', int, {'optional': True}),
            ('offset', int, {'optional': True}),
            ('player_id', list, {'optional': True}),
            ('player_status', str, {'optional': True}),
            ('position', str, {'optional': True}),
            ('timeframe', str, {'optional': True}),
            ('period', str, {'optional': True}),
            ('stats_type', str, {'optional': True}),
            ('source', str, {'optional': True}),
            ('team_id', int, {'optional': True}),
            ('team_type', str, {'optional': True}),
            ('pro_or_fantasy', str, {'optional': True}),
        ]
    },
    'league_fantasy__points': {
        'weekly__scoring': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('timeframe', str, {'optional': True}),
            ('player_id', int, {'optional': True}),
            ('team_id', int, {'optional': True}),
            ('team_type', str, {'optional': True}),
            ('player_status', str, {'optional': True}),
            ('position', str, {'optional': True}),
        ],
    },
    'league_transaction__list': {
        'add__drops': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ],
        'trades': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ],
        'log': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('filter', str, {'optional': True}),
            ('team_id', int, {'optional': True}),
        ]
    },
    # these methods can make changes to the league, might require special
    # groups
    'league_transactions': {
        'add__drop': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('id', str, {'optional': True}),
        ],
        'lineup': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ],
        'trade': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ],
        'waiver__order': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ]
    },  # league.transactions
    'league_scoring': {
        'live': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('team_id', int, {'optional': True}),
            ('period', str, {'optional': True}),
            ('no_players', bool, {'optional': True}),
        ],
        'preview': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('matchup_id', str, {'optional': True}),
            ('team_id', int, {'optional': True}),
            ('period', str, {'optional': True}),
        ],
        'categories': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ],
        'rules': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ]
    },  # league.scoring
    'league_standings': {
        'breakdown': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('period', int, {'optional': True}),
        ],
        'by__period': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('period', int, {'optional': True}),
        ],
        'overall': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('period', int, {'optional': True}),
        ],
        'power': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('period', str, {'optional': True}),
        ]
    },  # league.standings
    'league_draft': {
        'results': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('round', int, {'optional': True}),
            ('limit', int, {'optional': True}),
            ('offset', int, {'optional': True}),
            ('suppress_player_data', int, ['optional', ('allowed', 1)]),
            ('suppress_team_data', int, ['optional', ('allowed', 1)]),
            ('suppress_round_data', int, ['optional', ('allowed', 1)]),
            ('minimum_data', int, ['optional', ('allowed', 1)]),
        ],
        'order': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ],
        'config': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ]
    },  # league.draft
    # stats methods
    'stats': {
        'defense__vs__position': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('timeframe', str, {'optional': True}),
            ('period', str, {'optional': True}),
            ('position', str, {'optional': True}),
            ('team', str, {'optional': True}),
            ('view', str, {'optional': True}),
        ],
        'situational_stats': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('timeframe', str, {'optional': True}),
            ('player_id', int, []),
            ('situation', str, {'optional': True}),
        ],
        'categories': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ]
    },
    'players': {
        'average__draft__position': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('position', str, {'optional': True}),
            ('limit', str, {'optional': True}),
        ],
        'gamelog': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('player_id', int, []),
            ('timeframe', str, []),
            ('num_games', str, {'optional': True}),
            ('start_date', str, ['not_valid']),   # Baseball only
            ('end_date', str, ['not_valid']),   # Baseball only
        ],
        'inactives': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('period', str, [])
        ],
        'injuries': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('position', str, {'optional': True}),
        ],
        'list': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ],
        'outlook': [

            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('player_id', int, [])
        ],
        'profile': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('player_id', int, [])
        ],
        'rankings': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('position', str, {'optional': True}),
            ('type', str, {'optional': True}),
            ('source', str, {'optional': True}),
            ('timeframe', str, {'optional': True}),
        ],
        'search': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('player_id', int, {'optional': True}),
            ('pro_team', str, {'optional': True}),
            ('name', str, {'optional': True}),
            ('position', str, {'optional': True}),
            ('team_id', int, {'optional': True}),
            ('free_agents', str, {'optional': True}),
            ('owned', str, {'optional': True}),
            ('eligible_only', str, {'optional': True}),
            ('limit', int, {'optional': True}),
        ],
        'updates': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('team_id', int, {'optional': True}),
            ('team_type', str, {'optional': True}),
            ('team_abbr', str, {'optional': True}),
            ('position', str, {'optional': True}),
            ('player_id', int, {'optional': True}),
            ('eligible_position', str, {'optional': True}),
            ('free_agents', int, {'optional': True}),
            ('type', str, {'optional': True}),
            ('limit', int, {'optional': True}),
        ]
    },  # players
    'players_roster__trends': {
        'most__activated': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('position', str, {'optional': True}),
            ('player_status', str, {'optional': True}),
            ('limit', int, {'optional': True}),
        ],
        'most__added': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('position', str, {'optional': True}),
            ('player_status', str, {'optional': True}),
            ('limit', int, {'optional': True}),
        ],
        'most__benched': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('position', str, {'optional': True}),
            ('player_status', str, {'optional': True}),
            ('limit', int, {'optional': True}),
        ],
        'most__dropped': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('position', str, {'optional': True}),
            ('player_status', str, {'optional': True}),
            ('limit', int, {'optional': True}),
        ],
        'most__owned': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('position', str, {'optional': True}),
            ('player_status', str, {'optional': True}),
            ('limit', int, {'optional': True}),
        ],
        'most__started': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('position', str, {'optional': True}),
            ('player_status', str, {'optional': True}),
            ('limit', int, {'optional': True}),
        ],
        'most__traded': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('position', str, {'optional': True}),
            ('player_status', str, {'optional': True}),
            ('limit', int, {'optional': True}),
        ],
        'most__viewed': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('position', str, {'optional': True}),
            ('player_status', str, {'optional': True}),
            ('limit', int, {'optional': True}),
        ]
    },  # players.roster-trends
    'fantasy_news': {
        'story': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('id', int, []),
        ],
        'headlines': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('limit', int, {'optional': True}),
            ('offset', int, {'optional': True}),
        ],
    },
    'fantasy_league_news': {
        'story': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('id', str, []),
        ],
        'headlines': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('limit', int, {'optional': True}),
            ('offset', int, {'optional': True}),
        ],
    },
    'general': {
        'auction__values': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('source', str, {'optional': True}),
        ],
        'stats': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES}),
            ('timeframe', str, {'allowed_mask': ('YYYY')}),
            ('period', str, {'allowed': ALLOWED_PERIOD,
                             'allowed_mask': 'YYYYMMDD'}),
            ('player_id', list, {'optional': True}),
        ],
        'positions': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ],
        'pro__teams': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ],
        'sports': [
            ('response_format', str, {'optional': True,
                                      'allowed': ALLOWED_RESPONSE_VALUES})
        ]
    },  # general methods with no group
}


def _fix_param(name, klass, options, param):
    """
        need to fix params that come in as lists to be
        comma separated
    """
    if klass is list and isinstance(param, list):
        new_param = ''
        for idx, single in enumerate(param, start=1):
            new_param += single
            if idx != len(param):
                new_param += ','
        return new_param
    return param


def _check_allowed(name, klass, allowed, param):
    if param not in allowed:
        raise CBSSportsError([{'msg': 'value \'%s\' not allowed, try one of <%s>' % (param, allowed),
                               'type': CBSSPORTS_UNALLOWED_TYPE}])
    return True


def _check_allowed_mask(name, allowed, param):
    print allowed


def gen_cbssports_method(namespace, method_name, param_data):
    """
    given the above data parse it into a function that will
    check parameters
    """
    required = []
    for param in param_data:
        if 'optional' not in param[2]:
            required.append(param)

    param_names = [x[0] for x in param_data]

    def cbssports_method(self, *args, **kwargs):
        params = {}
        # if there are any args that arent 'key' = 'value' this
        # loop goes through and assigns them in order of param_data
        # listed above
        for i, arg in enumerate(args):
            try:
                params[param_data[i][0]] = arg
            except IndexError:
                raise ValueError('too many args for %s' % method_name)

        params.update(kwargs)

        # check for all required args
        for param in required:
            if param[0] not in params:
                raise TypeError('%s: missing parameter \'%s\''
                                % (method_name, param[0]))

        # check params to see if there is anything that
        # should not be here
        for param in params:
            if param not in param_names:
                raise ValueError('%s: unexpected arg \'%s\''
                                 % (method_name, param))

        # run through and fix any params from python form to cbssports api form
        for name, klass, options in param_data:
            if name in params:
                #if 'allowed' in options or 'allowed_mask' in options:
                 #   passed = _check_allowed(name, klass, options['allowed'], params[name])
                #elif 'allowed_mask' in options:
                #    _check_allowed_mask(name, options['allowed_mask'], params[name])
                params[name] = _fix_param(name, klass, options, params[name])

        return self(method_name, params)

    cbssports_method.__name__ = method_name
    cbssports_method.__doc__ = \
        "CBSSports API call. See http://www.developer.\
            cbssports.com/documentation %s:%s" \
        % (namespace, method_name)

    return cbssports_method


class Group(object):
    """Represents a "namespace" of CBSSPORTS API Calls."""

    def __init__(self, client, name):
        print ('name: ' + name + ' client: ' + repr(client))
        self._client = client
        self._name = name

    def __call__(self, method=None, args=None):
        if method is None:
            return self
        return self._client('%s.%s' % (self._name, method), args)


def generate_methods(args):
    # loop over all the groups in the METHODS table
    for namespace in args:
        methods = {}
        # loop over each method in each group and process it
        for method, param_data in args[namespace].iteritems():
            methods[method] = gen_cbssports_method(namespace, method, param_data)

        # need to add our new functions to the globals so they can be used later
        group = type('%sGroup' % namespace.title(), (Group,), methods)

        globals()[group.__name__] = group

generate_methods(METHODS)


class CBSSportsError(Exception):
    """ Exception class for custom errors """
    def __init__(self, values):
        self.values = values

    def __str__(self):
        to_return = ''
        for idx, value in enumerate(self.values, start=1):
            to_return += value['msg']
            if idx != len(self.values):
                to_return += '\n'
        return to_return


class API(object):

    def __init__(self, response_format='JSON', access_token=None):
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
            raise CBSSportsError([{'msg': 'No access token set',
                                   'type': CBSSPORTS_ACCESS_TOKEN_ERROR}])

        if method is None:
            return self

        method = self._fix_method_name(method)

        args = self._build_args(args)

        url = self._build_url(method)

        r = requests.get(url, params=args)

        return self._parse_response(r, method)

    def _parse_response(self, response, method):
        # decode the JSON object
        decoder = json.JSONDecoder()
        json_response = decoder.decode(response.text)

        status_code = json_response['statusCode']

        if status_code == CBSSPORTS_EXCEPTION:
            raise CBSSportsError(json_response['body']['exceptions'])
        else:
            pass
        return json_response['body']

    def set_access_token(self, access_token):
        """Set the access_token if not already done"""
        self.access_token = access_token

    def _build_args(self, args=None):
        """Attach args that need to be with every query"""
        if args is None:
            args = {}

        #response_set = 'response_format' in args.keys()

        for arg in args:
            pass

        args['version'] = CBSSPORTS_API_VERSION
        args['access_token'] = self.access_token

        # if a response format was passed in on initialization use it
        # otherwise we do not pass the argument which results in xml response
        #if not response_set and self.default_response == 'JSON':
        # this version of the app will force JSON response
        args['response_format'] = 'JSON'

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
