import sys
import itertools
import math
import numpy
import flask

# [START functions_helloworld_http]
# [START functions_http_content]
from flask import escape

# [END functions_helloworld_http]
# [END functions_http_content]


# [START functions_tips_terminate]
# [START functions_helloworld_get]
def hello(request):
    if request.method == 'OPTIONS':
        # Allows GET requests from origin https://mydomain.com with
        # Authorization header
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'content-type',
            'Access-Control-Max-Age': '3600'
            # 'Access-Control-Max-Age': '3600',
            # 'Access-Control-Allow-Credentials': 'true'
        }
        return ('', 204, headers)
    print(request.get_json())
    requestBodyJson = request.get_json()
    # liklihood(["1","2","3", "4"], [.1,.2,.3,.4], [1], [2], ["3"], ["1","2","3", "4"])
    
    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*',
    }
    value = liklihood(requestBodyJson["alleles_vector"], requestBodyJson["population_probability"], requestBodyJson["prosecution_unknowncontributors"], requestBodyJson["defense_unknowncontributors"], requestBodyJson["prosecution_unknownalleles"], requestBodyJson["defense_unknownalleles"])
    print(value)
    return (str(value), 200, headers)
    # return ('Hello World!', 200, headers)
# [END functions_helloworld_get]


# [START functions_helloworld_background]
def hello_background(data, context):
    """Background Cloud Function.
    Args:
         data (dict): The dictionary with data specific to the given event.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata.
    """
    if data and 'name' in data:
        name = data['name']
    else:
        name = 'World'
    return 'Hello {}!'.format(name)
# [END functions_helloworld_background]
# [END functions_tips_terminate]


# [START functions_helloworld_http]
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    return 'Hello {}!'.format(escape(name))
# [END functions_helloworld_http]


# [START functions_helloworld_pubsub]
def hello_pubsub(data, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         data (dict): The dictionary with data specific to this type of event.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata.
    """
    import base64

    if 'data' in data:
        name = base64.b64decode(data['data']).decode('utf-8')
    else:
        name = 'World'
    print('Hello {}!'.format(name))
# [END functions_helloworld_pubsub]


# [START functions_helloworld_storage]
def hello_gcs(data, context):
    """Background Cloud Function to be triggered by Cloud Storage.
    Args:
         data (dict): The dictionary with data specific to this type of event.
         context (google.cloud.functions.Context): The Cloud Functions
         event metadata.
    """
    print("File: {}.".format(data['objectId']))
# [END functions_helloworld_storage]


# [START functions_http_content]
def hello_content(request):
    """ Responds to an HTTP request using data from the request body parsed
    according to the "content-type" header.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    content_type = request.headers['content-type']
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'name' in request_json:
            name = request_json['name']
        else:
            raise ValueError("JSON is invalid, or missing a 'name' property")
    elif content_type == 'application/octet-stream':
        name = request.data
    elif content_type == 'text/plain':
        name = request.data
    elif content_type == 'application/x-www-form-urlencoded':
        name = request.form.get('name')
    else:
        raise ValueError("Unknown content type: {}".format(content_type))
    return 'Hello {}!'.format(escape(name))
# [END functions_http_content]


# [START functions_http_methods]
def hello_method(request):
    """ Responds to a GET request with "Hello world!". Forbids a PUT request.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
         Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    from flask import abort

    if request.method == 'GET':
        return 'Hello World!'
    elif request.method == 'PUT':
        return abort(403)
    else:
        return abort(405)
# [END functions_http_methods]





def liklihood (alleles, prob, x1, x2, u1, u2):
    # Begin input error checking

    n_u1 = len(u1)

    n_u2 = len(u2)

    G = len(x1)


    ind1 = None
    ind2 = None

    if (n_u1 > 0):
        ind1 = numpy.repeat(None, n_u1)
        for k in range(0, n_u1):
            ind1[k] = numpy.min(numpy.where(numpy.array(alleles) == u1[k]))

    if (n_u2 > 0):
        ind2 = numpy.repeat(None, n_u2)
        for k in range(0, n_u2):
            ind2[k] = numpy.min(numpy.where(numpy.array(alleles) == u2[k]))

    p1 = p_evid(p = prob, x = x1, ind = ind1, g = G)
    p2 = p_evid(p = prob, x = x2, ind = ind2, g = G)
    LR = p1 / p2
    return LR


def p_evid (p, x, ind, g):
    if ind is None:
        n_u = 0
    else:
        n_u = len(ind)
        
    
    T = numpy.float32(numpy.repeat(0, n_u + 1))
    T[0] = numpy.prod(math.pow(sum(p), 2 * x[0]))

    if(n_u > 1):
        for skip in range(1, n_u):
            K = list(itertools.combinations(ind, skip))
            Kcol = len(K)
            t = numpy.float32(numpy.repeat(0, Kcol))
            for j in range(0, Kcol):
                # print("j = ", j)
                # print("p[int(j)+1:]", numpy.delete(p, K[j]))
                t[j] = numpy.prod(math.pow(sum(numpy.delete(p, K[j])), (2 * x[0])))
                # print("SUM = ", math.pow(sum(numpy.delete(p, K[j])), 2 * x[0]))
            T[skip] = math.pow(-1, skip) * sum(t)
    if(n_u > 0):
        T[n_u] = math.pow(-1, n_u) * numpy.prod(math.pow(sum(numpy.delete(p, ind)), 2 * x[0]))
    return(sum(T))




    # if (n_u1 > 0):
    #     if not u1.intersection(alleles) == u1:
    #         exit("'u1' must contain only elements from 'alleles'")
    # if (n_u2 > 0):
    #     if not u2.intersection(alleles) == u2:
    #         exit("'u2' must contain only elements from 'alleles'")

    # if (alleles == u1):
    #     exit("under the null hypothesis there must be at least one known contributor")
    # G = len(x1)

    
    
    

# liklihood(["1","2","3"], [.1,.2,.3], [0], [1], [], ["1"])
# liklihood(["1","2","3", "4"], [.1,.2,.3,.4], [1], [2], ["3"], ["1","2","3", "4"])
