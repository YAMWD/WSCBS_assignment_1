from flask import Flask, request, jsonify, make_response
import hashlib
import re
import string
import json

urls = {}

app = Flask(__name__)
#Generate hash value of url
def hash(url):

    ans = 0 #hash value

    for letter in url: #sum ASCII value of all letters in url
        ans += ord(letter)
        # ans = ans % limit
    
    while ans in urls.keys(): #if there is same ASCII sum , the ans will plus one to make them different
        ans += 1
        # ans = ans % limit

    return ans
#shorten the hash. The hash(url) returns an integer, this funtion turn 10 base into 64base
def int2base64(n):
    #make a base64 table, list by index-character 
    table = list(string.ascii_uppercase + string.ascii_lowercase + string.digits + '+' + '/')
    #turn integer into binary
    s = bin(n)[2:]
    #if the length of binary sequence is not a multiple of 6, to ensure the base conversion, 0 is added in front
    if len(s) % 6 != 0:
        s = '0' * (6 - len(s) % 6) + s
            
    ans = '' #initial ans for restoring base64 result
    iter = int(len(s) / 6) #length of Base64 number
    for i in range(iter):
        start = i * 6
        end = (i + 1) * 6
        s_par = int(s[start:end], base = 2) #convert binary in integer as index
        ans += table[s_par] #add base64 character into ans, located by index of table
    
    return ans

# get the url of the identifier
@app.route("/<identifier>", methods=["GET"])
def get_url(identifier):
    #if id is found in urls, return its url, else return 404 not found
    url = urls.get(identifier)
    if url != None:
        # desired HTTP status code
        status_code = 301

        msg = json.dumps({'value': url})
        # Create a response with JSON and text data
        response = make_response(msg, status_code)

        # Set the Content-Type header to application/json
        response.headers['Content-Type'] = 'application/json'

        return response
    else:
        return "Not Found", 404
    
# update the url of the identifier
@app.route("/<identifier>", methods=["PUT"])
def update_item(identifier):
    data = request.data
    url = json.loads(data.decode())['url']
    if urls.get(identifier):
        if check_url_validity(url) == False:
            return "Invalid URL", 400 #400 with an error if the update failed (e.g., the URL was invalid)
        else:
            urls[identifier] = url
            print("1")
            return "Updated", 200 #Updates the URL behind the given ID.
    else:   
        return "Not Found", 404 #404 if the ID does not exist
    
# delete the identifier
@app.route("/<identifier>", methods=["DELETE"])
def delete_identifier(identifier):
    if urls.get(identifier):
        del urls[identifier]
        return "Deleted", 204 #find the identifier and delete it 
    else:
        return "Not Found", 404 #identifier not found
    
# get all the identifiers
@app.route("/", methods=["GET"])
def get_identifiers():
    return urls, 200

# create a new identifier for the url
@app.route("/", methods=["POST"])
def create_identifier():
    data = request.json
    url = data.get('value')
    # Check URL validity with a regex expression before creating a mapping for it
    if check_url_validity(url) == False:
        return  "Invalid URL", 400
    # Check whether the url already exists or not
    if url in urls.values():
        id = [k for k, v in urls.items() if v == url][0] 
        return 'identifier of {} already exists'.format(url), 400

    identifier = int2base64(hash(url))
    urls[identifier] = url

    # desired HTTP status code
    status_code = 201

    msg = json.dumps({'id': identifier})
    # Create a response with JSON and text data
    response = make_response(msg, status_code)

    # Set the Content-Type header to application/json
    response.headers['Content-Type'] = 'application/json'

    return response

# delete all the identifiers
@app.route("/", methods=["DELETE"])
def delete_identifiers():
    urls.clear()
    return "All Deleted", 404

def check_url_validity(url):
    # regex pattern for url validation, source from https://uibakery.io/regex-library/url-regex-python https://blog.csdn.net/qq_42019226/article/details/126395030
    pattern_1 = re.compile("^((https|http|ftp|rtsp|mms)?:\/\/)(([A-Za-z0-9]+-[A-Za-z0-9]+|[A-Za-z0-9]+)\.)+([A-Za-z]{2,6})(:\d+)?(\/.*)?(\?.*)?(#.*)?$")
    pattern_2 = re.compile("^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$")
    if pattern_1.match(url) or pattern_2.match(url):
        return True
    else:
        return False
    
