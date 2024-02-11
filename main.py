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
        return 301, url
    else:
        return 404, "Not Found"
    
# add a new identifier for the url
@app.route("/<url>/<identifier>", methods=["PUT"])
def add_item(url, identifier):
    try:
        if urls.get(identifier):
            return 400, "Identifier already exists"
        else:
            urls[identifier] = url
            return 200, "Created"
    except:
        return 404, "Not Found"
    
# delete the identifier
@app.route("/<identifier>", methods=["DELETE"])
def delete_identifier(identifier):
    if urls.get(identifier):
        del urls[identifier]
        return 204, "Deleted"
    else:
        return 404, "Not Found"
    
# get all the identifiers
@app.route("/", methods=["GET"])
def get_identifiers():
    return 200, urls

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
        return 201, identifier
    except:
        return 404, "Create Failed"
    
# delete all the identifiers
@app.route("/", methods=["DELETE"])
def delete_identifiers():
    urls.clear()
    return 404, "All Deleted"

def check_url_validity(url):
    # regex pattern for url validation
    pattern = re.compile(r"(http|https)://[a-zA-Z0-9\-.]+\.[a-zA-Z]{2,3}(/\S*)?")
    if pattern.match(url):
        return True
    else:
        return False
    
