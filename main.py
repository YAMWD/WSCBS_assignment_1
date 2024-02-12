from flask import Flask
import hashlib
import re
import string

urls = {}

app = Flask(__name__)

def hash(url):

    ans = 0

    for letter in url:
        ans += ord(letter)
        # ans = ans % limit
    
    while ans in urls.keys():
        ans += 1
        # ans = ans % limit

    return ans

def int2base64(n):
    table = list(string.ascii_uppercase + string.ascii_lowercase + string.digits + '+' + '/')
    s = bin(n)[2:]
    
    if len(s) % 6 != 0:
        s = '0' * (6 - len(s) % 6) + s
            
    ans = ''
    iter = int(len(s) / 6)
    for i in range(iter):
        start = i * 6
        end = (i + 1) * 6
        s_par = int(s[start:end], base = 2)
        ans += table[s_par]
    
    return ans

# get the url of the identifier
@app.route("/<identifier>", methods=["GET"])
def get_url(identifier):
    url = urls.get(identifier)
    if url:
        return url, 301
    else:
        return "Not Found", 404
    
# add a new identifier for the url
@app.route("/<url>/<identifier>", methods=["PUT"])
def add_item(url, identifier):
    try:
        if urls.get(identifier):
            return "Identifier already exists", 400
        else:
            urls[identifier] = url
            return "Created", 200
    except:
        return "Not Found", 404
    
# delete the identifier
@app.route("/<identifier>", methods=["DELETE"])
def delete_identifier(identifier):
    if urls.get(identifier):
        del urls[identifier]
        return "Deleted", 204
    else:
        return "Not Found", 404
    
# get all the identifiers
@app.route("/", methods=["GET"])
def get_identifiers():
    return urls, 200

# create a new identifier for the url
@app.route("/<url>", methods=["POST"])
def create_identifier(url):

    # Check URL validity with a regex expression before creating a mapping for it
    if check_url_validity(url) == False:
        return  "Invalid URL", 400

    if url in urls.values():
        id = [k for k, v in urls.items() if v == url][0]
        return 'identifier of {} already exists'.format(url), 400

    identifier = int2base64(hash(url))

    # identifier = str(hash(url))

    urls[identifier] = url
    return identifier, 201

# delete all the identifiers
@app.route("/", methods=["DELETE"])
def delete_identifiers():
    urls.clear()
    return "All Deleted", 404

def check_url_validity(url):
    # regex pattern for url validation, source from https://uibakery.io/regex-library/url-regex-python
    pattern_1 = re.compile("^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$")
    pattern_2 = re.compile("^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$")
    if pattern_1.match(url) or pattern_2.match(url):
        return True
    else:
        return False
    
