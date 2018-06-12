
from chalice import Chalice
from chalice import BadRequestError
from chalice import NotFoundError
import sys
import json
import boto3
from botocore.exceptions import ClientError

if sys.version_info[0] == 3:
    # Python 3 imports.
    from urllib.parse import urlparse, parse_qs
else:
    # Python 2 imports.
    from urlparse import urlparse, parse_qs

app = Chalice(app_name='helloworld')
app.debug = True

S3 = boto3.client('s3', region_name='us-west-2')
BUCKET = 'chalice-demo'

CITIES_TO_STATE = {
    'seattle': 'WA',
    'portland': 'OR'
}

OBJECTS = {
}

@app.route('/', methods=['POST'],
           content_types=['application/x-www-form-urlencoded'])
def index():
    parsed = parse_qs(app.current_request.raw_body.decode())
    return {
        'states': parsed.get('states', [])
    }

@app.route('/cities/{city}')
def state_of_city(city):
    try:
        return {'state': CITIES_TO_STATE[city]}
    except KeyError:
        raise BadRequestError("Unknown city '%s', valid choices are: %s" % (
            city, ', '.join(CITIES_TO_STATE.keys())))

@app.route('/resource/{value}', methods=['PUT'])
def put_test(value):
    return {'value': value}

@app.route('/s3_objects/{key}', methods=['GET', 'PUT'])
def s3objects(key):
    request = app.current_request
    if request.method == 'PUT':
        S3.put_object(Bucket=BUCKET, Key=key, Body=json.dumps(request.json_body))
    elif request.method == 'GET':
        try:
            response = S3.get_object(Bucket=BUCKET, Key=key)
            return json.loads(response['Body'].read())
        except ClientError as e:
            raise NotFoundError(key)

@app.route('/objects/{key}', methods=['GET', 'PUT'])
def myobject(key):
    request = app.current_request
    if request.method == 'PUT':
        OBJECTS[key] = request.json_body
    elif request.method == 'GET':
        try:
            return{key: OBJECTS[key]}
        except KeyError:
            raise NotFoundError(key)

@app.route('/myview', methods=['POST'])
def myview_post():
    return {'message': 'This is the route for POST.'}

@app.route('/myview', methods=['PUT'])
def myview_put():
    return {'message': 'This is the route for PUT.'}

@app.route('/plain-text')
def plain_text():
    return Response(body='hello world!',
                    status_code=200,
                    headers={'Content-Type': 'text/plain'})

@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

