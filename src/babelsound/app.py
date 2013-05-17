# Create the flask application.
from flask import Flask, jsonify, request, send_file
app = Flask(__name__, static_url_path='')


# Create a list of eligible services. When an URI is submitted, they will be
# tried in a sequence to find an accepting service.
from babelsound.services import deezer, rdio, spotify
services = set([deezer, rdio, spotify])


@app.route('/')
def index():
    # Avoid using render_template: we choose client-side templating with
    # angularJS rather than server-side templating.
    return send_file('templates/index.html')


@app.route('/1/translate.json', methods=['POST'])
def translate():
    uri = request.json['uri']

    # Find the service which matches the track URI format and request the
    # correspond track data.
    finder = ((s, s.resolve(uri)) for s in services if s.accepts(uri))
    result = next(finder, None)
    if not result:
        return jsonify({'error_msg': 'Could not guess track provider'}), 400

    # The first element of the tuple corresponds to the service which was
    # elected to resolve the URL. We compute the set of remaining services to
    # make the opposite query (search from the track data).
    service, track = result
    if not track:
        return jsonify({'error_msg': 'Could not resolve track'}), 400

    # Ask each remaining provider to give their own information for the track.
    result = [{'name': service.service_name, 'info': track._asdict()}]
    for other in (services - set([service])):
        res = other.find(track)
        if res:
            result.append({'name': other.service_name, 'info': res._asdict()})

    # Result is sent as JSON.
    return jsonify({'services': result})
