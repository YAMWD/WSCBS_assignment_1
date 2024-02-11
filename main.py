from flask import Flask
import hashlib
import re

urls = {}

app = Flask(__name__)

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
    try:
        # Check URL validity with a regex expression before creating a mapping for it
        # if check_url_validity(url):
        #     identifier = hashlib.sha256(url.encode()).hexdigest()
        #     urls[identifier] = url
        #     return 201, identifier
        # else:
        #     return 404, "Invalid URL"
        identifier = hashlib.sha256(url.encode()).hexdigest()
        urls[identifier] = url
        return identifier, 201
    except:
        return "Create Failed", 404
    
# delete all the identifiers
@app.route("/", methods=["DELETE"])
def delete_identifiers():
    urls.clear()
    return "All Deleted", 404

def check_url_validity(url):
    # regex pattern for url validation
    pattern = re.compile(r"(http|https)://[a-zA-Z0-9\-.]+\.[a-zA-Z]{2,3}(/\S*)?")
    if pattern.match(url):
        return True
    else:
        return False
    
