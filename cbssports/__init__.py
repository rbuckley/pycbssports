#!/usr/bin/env python
#
# pycbssports - Python bindings for the CBSSports Developer API
#
#
#


VERSION = '0.001a'

CBSSPORTS_URL = 'http://api.cbssports.com/fantasy'

RESPONSE_FORMAT = 'JSON'


# METHODS follows this
#       'namespace1': {
#           'method1': [
#               (name, klass, [options]),
#               (name, klass, [options])
#           ],
#           'method2: [
#               (name, klass, [options])
#           ]
#       },
#       'namespace2:{
#       ...
#       ...

METHODS = {
    # draft methods
    'draft': {
        'config': [
        ],
        'order': [
        ],
        'results': [
        ]
    },
    # gerneral methods
    'general': {
        'positions': [
        ],
        'professional_teams': [
        ],
        'sports': [
        ]
    },
    'league_info': {
        'owners': [
        ],
        'teams': [
        ],
        'dates': [
        ],
        'details': [
        ],
        'rules': [
        ],
        'schedule': [
        ]
    },

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
        group = type('%sGroup' % namespace.title(), (Group,), methods)

        globals()[group.__name__] = group

generate_methods()


class API(object):

    def __init__(self, access_token=None):
        self.access_token = access_token

        for namespace in METHODS:
            self.__dict__[namespace] = eval('%sGroup(self, \'%s\')' % (namespace.title(), 'api.%s' % namespace))

    def __call__(self, method=None, args=None):
        """Do the actual call to the REST api"""
        if method is None:
            return self

        payload = {'access_token': access_token}
