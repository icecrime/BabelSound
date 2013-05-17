# Example URL:
#   spotify:track:2Foc5Q5nqNiosCNqttzHof
#   http://open.spotify.com/track/2Foc5Q5nqNiosCNqttzHof

import operator
import requests
import urlparse

from babelsound.services import Track


service_name = 'Spotify'

find_call = 'http://ws.spotify.com/search/1/track.json'
resolve_call = 'http://ws.spotify.com/lookup/1/.json'


def _extract_artist(data):
    if 'artist' in data:
        return data['artist']['name']
    elif 'artists' in data:
        fn = operator.itemgetter('name')
        return ', '.join(fn(elem) for elem in data['artists'])
    return None


def _is_valid_find_result(rv):
    return ((rv.status_code == requests.codes.ok) and
            (rv.json()['info']['num_results'] > 0))


def _is_valid_resolve_result(rv):
    return ((rv.status_code == requests.codes.ok) and
            (rv.json()['info']['type'] == 'track'))


def _query_str(track):
    return ' AND '.join('{}:"{}"'.format(k, v)
                        for k, v in track._asdict().items()
                        if k in ['artist', 'track', 'album'])


def _track_from_api(data):
    field_map = [
        ('album',    ('album', 'name')),
        ('duration', ('length',)),
        ('link',     ('href',)),
        ('title',    ('name',)),
    ]

    infos = {f[0]: reduce(operator.getitem, f[1], data) for f in field_map}
    infos['artist'] = _extract_artist(data)
    return Track(**infos)


def accepts(uri):
    return (uri.startswith('spotify:') or
            (urlparse.urlparse(uri).netloc == 'open.spotify.com'))


def find(track):
    rv = requests.get(find_call, params={'q': _query_str(track)})
    if _is_valid_find_result(rv):
        return _track_from_api(rv.json()['tracks'][0])
    return None


def resolve(uri):
    rv = requests.get(resolve_call, params={'uri': uri})
    if _is_valid_resolve_result(rv):
        return _track_from_api(rv.json()['track'])
    return None
