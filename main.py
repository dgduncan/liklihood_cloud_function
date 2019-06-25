import sys
import flask

# [START functions_helloworld_http]
# [START functions_http_content]
from flask import escape
from Liklihood import liklihood

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
        }
        return ('', 204, headers)
    print(request.get_json())
    requestBodyJson = request.get_json()
    # liklihood(["1","2","3", "4"], [.1,.2,.3,.4], [1], [2], ["3"], ["1","2","3", "4"])
    
    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*',
    }
    # value = liklihood(requestBodyJson["alleles_vector"], requestBodyJson["population_probability"], requestBodyJson["prosecution_unknowncontributors"], requestBodyJson["defense_unknowncontributors"], requestBodyJson["prosecution_unknownalleles"], requestBodyJson["defense_unknownalleles"])
    value = liklihood(requestBodyJson["alleles_vector"], requestBodyJson["population_probability"], requestBodyJson["prosecution_unknowncontributors"], requestBodyJson["defense_unknowncontributors"], requestBodyJson["prosecution_unknownalleles"], requestBodyJson["defense_unknownalleles"])
    
    print(value)
    
    return (str(value), 200, headers)
    # return ('Hello World!', 200, headers)
