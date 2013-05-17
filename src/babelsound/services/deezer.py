# Example URL:
#   http://www.deezer.com/track/66609426

import operator
import requests
import urlparse

from babelsound.services import Track


service_name = 'Deezer'

find_call = 'http://api.deezer.com/2.0/search'
resolve_call = 'http://api.deezer.com/2.0/track/'


def _query_str(track):
    return ' '.join([track.artist, track.title])


def _is_valid_find_result(rv):
    return (rv.status_code == requests.codes.ok) and (rv.json()['total'] > 0)


def _is_valid_search_result(rv):
    return (rv.status_code == requests.codes.ok) and ('error' not in rv.json())


def _track_from_api(data):
    field_map = [
        ('album',    ('album', 'title')),
        ('artist',   ('artist', 'name')),
        ('duration', ('duration',)),
        ('link',     ('link',)),
        ('title',    ('title',)),
    ]

    infos = {f[0]: reduce(operator.getitem, f[1], data) for f in field_map}
    return Track(**infos)


def accepts(uri):
    return urlparse.urlparse(uri).netloc == 'www.deezer.com'


def find(track):
    rv = requests.get(find_call, params={'q': _query_str(track)})
    if _is_valid_find_result(rv):
        return _track_from_api(rv.json()['data'][0])
    return None


def resolve(uri):
    track_id = uri.rsplit('/', 1)[-1]
    rv = requests.get(resolve_call + track_id, params={'output': 'json'})
    if _is_valid_search_result(rv):
        return _track_from_api(rv.json())
    return None
