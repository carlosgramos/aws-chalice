# aws-chalice

AWS Chalice is a serverless framework which can use Python2.7 or Python3.6. The framework has the feel of Flask and is simple to use. When a Chalice application is deployed, it generates an AWS Lambda function to power the app's routes, and an  API Gateway API to handle the request/ response cycle.

Installation is made easy by using: 
```sh 
$ pip install chalice
```

Some of Chalice's features include:

Support for URL Parameters:
```sh
@app.route('/cities/{city}')
```

Debugging:
```sh
app = Chalice(app_name='helloworld')
app.debug = True
```

Error Reporting:
Chalice supports the following error classes:
* BadRequestError - return a status code of 400
* UnauthorizedError - return a status code of 401
* ForbiddenError - return a status code of 403
* NotFoundError - return a status code of 404
* ConflictError - return a status code of 409
* UnprocessableEntityError - return a status code of 422
* TooManyRequestsError - return a status code of 429
* ChaliceViewError - return a status code of 500

Separate view functions for the same route URL, with different HTTP Methods:
```sh
@app.route('/myview', methods=['POST'])
def myview_post():
    pass

@app.route('/myview', methods=['PUT'])
def myview_put():
    pass
```

Information about the current request:
Chalice makes a request object available to each view function when the function is called.
The request object can be used to create conditional logic based on which HTTP method was used when the function was called. If the request was a GET, you can take one action. If the request was a POST you can take another.

The current_request object has the following properties:
```sh
current_request.query_params - A dict of the query params for the request.
current_request.headers - A dict of the request headers.
current_request.uri_params - A dict of the captured URI params.
current_request.method - The HTTP method (as a string).
current_request.json_body - The parsed JSON body (json.loads(raw_body))
current_request.raw_body - The raw HTTP body as bytes.
current_request.context - A dict of additional context information
current_request.stage_vars - Configuration for the API Gateway stage
```

Managing request content types:
A "Content-type" is simply a header defined in many protocols, such as HTTP, that makes use of MIME types to specify the nature of the file currently being handled.

There are many MIME types, and you can see a list here:
[https://www.freeformatter.com/mime-types-list.html](https://www.freeformatter.com/mime-types-list.htm)

Chalice view functions send the HTTP request body using the application/json Content-Type by default.
You can set other content types in your view function by setting the content_types parameter:
@app.route('/', methods=['POST'],
           content_types=['application/x-www-form-urlencoded'])

Returning something other than JSON:
By default a Chalice view function will return data serialized in a JSON format string. If you want to return data in a another format, such as plain text, you must specify this inside the view function's body.
```sh
@app.route('/')
def index():
    return Response(body='hello world!',
                    status_code=200,
                    headers={'Content-Type': 'text/plain'})
```

Supporting CORS requests:
You can specify whether a view supports CORS by adding the cors parameter to your view function definition.
```sh 
@app.route('/supports-cors', methods=['PUT'], cors=True)
```

Settings 'cors=True' has similar behavior to enabling CORS using the AWS Console. This includes:

- Injecting the Access-Control-Allow-Origin: * header to your responses, including all error responses you can return.
- Automatically adding an OPTIONS method to support preflighting requests.

If more fine grained control of the CORS headers is desired, set the cors parameter to an instance of 'CORSConfig' object instead of True.

You can import the CORSConfig object from the chalice package:
    
```sh
from chalice import CORSConfig
cors_config = CORSConfig(
    allow_origin='https://foo.example.com',
    allow_headers=['X-Special-Header'],
    max_age=600,
    expose_headers=['X-Special-Header'],
    allow_credentials=True
)
@app.route('/custom_cors', methods=['GET'], cors=cors_config)
def supports_custom_cors():
    return {'cors': True}
```
Authenticating API Gateway routes:
There are serveral ways of authenticating a request to the backend API Gateway.
- API Key -> api_key_required=True
- AWS IAM -> authorizer = IAMAuthorizer()
- Cognito User Pool -> authorizer = CognitoUserPoolAuthorizer()
- Custom Authorizer -> authorizer = CustomAuthorizer()

Using Chalice's built in testing web server:
Chalice includes it's own web server which you can run while developing. It runs on port 8000 by default.

```sh
chalice local
```
Overall, Chalice is a super easy framework to use, and it leverages AWS's Lambda and API Gateway natively. For more info go to: [https://github.com/aws/chalice](https://github.com/aws/chalice)
