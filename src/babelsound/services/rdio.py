# Example URL:
#   http://rd.io/x/QTmmBjdegFRQ/

import operator
import requests
import requests_oauthlib
import urlparse

from babelsound import config
from babelsound.services import Track


service_name = 'Rdio'
api_endpoint = 'http://api.rdio.com/1/'


def _make_rdio_session():
    oauth = requests_oauthlib.OAuth1(
        client_key=config.RDIO_CONSUMER_KEY,
        client_secret=config.RDIO_CONSUMER_SECRET,
        resource_owner_key=config.RDIO_RESOURCE_OWNER_KEY,
        resource_owner_secret=config.RDIO_RESOURCE_OWNER_SECRET)

    session = requests.session()
    session.auth = oauth
    return session

rdio_session = _make_rdio_session()


def _is_valid_resolve_result(rv):
    return ((rv.status_code == requests.codes.ok) and
            (rv.json()['status'] == 'ok'))


def _is_valid_search_result(rv):
    return (_is_valid_resolve_result(rv) and
            (rv.json()['result']['number_results'] > 0))


def _query_str(track):
    return ' '.join([track.artist, track.title])


def _track_from_api(data):
    field_map = [
        ('album',    ('album',)),
        ('artist',   ('artist',)),
        ('duration', ('duration',)),
        ('link',     ('shortUrl',)),
        ('title',    ('name',)),
    ]

    infos = {f[0]: reduce(operator.getitem, f[1], data) for f in field_map}
    return Track(**infos)


def accepts(uri):
    return urlparse.urlparse(uri).netloc == 'rd.io'


def find(track):
    params = {'method': 'search', 'types': 'Track', 'query': _query_str(track)}
    rv = rdio_session.post(api_endpoint, data=params)
    if _is_valid_search_result(rv):
        return _track_from_api(rv.json()['result']['results'][0])
    return None


def resolve(uri):
    params = {'method': 'getObjectFromUrl', 'url': uri}
    rv = rdio_session.post(api_endpoint, data=params)
    if _is_valid_resolve_result(rv):
        return _track_from_api(rv.json()['result'])
    return None
