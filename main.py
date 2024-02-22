from flask import Flask, request, jsonify, make_response
import hmac, hashlib
import re
import string
import json
import base64
import datetime

urls = {}
users = {}
JWT_info = {}

app = Flask(__name__)

def generate_JWT(user_name):
    date_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    header = {
    "alg": "HS256",
    "typ": "JWT"
    }

    payload = {
    "sub": "JWT",
    "name": user_name,
    "iat": date_time,
    "exp": 600
    }

    secret = b'student138, 145.100.135.138, JahL7laipah1voob'

    header_bytes = json.dumps(header).encode('utf-8')

    payload_bytes = json.dumps(payload).encode('utf-8')

    base_string = base64.urlsafe_b64encode(header_bytes) + b'.' + base64.urlsafe_b64encode(payload_bytes)

    signature = hmac.new(secret, base_string, digestmod=hashlib.sha256).hexdigest()

    JWT_info[user_name] = {'token': signature, 'issue_date': date_time}

    return signature

#Generate hash value of url
def hash(url):

    ans = 0 #hash value

    for letter in url: #sum ASCII value of all letters in url
        ans += ord(letter)
        # ans = ans % limit
    
    while ans in urls.keys(): #if there is same ASCII sum , the ans will plus one until they are different
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

def get_user_by_JWT(JWT):
    for user, entry in JWT_info.items():
        if entry['token'] == JWT:
            return (user, entry['issue_date'])
    return None

def check_jwt_vadility(start_time, end_time):
    duration = end_time - start_time

    seconds = duration.total_seconds()

    if seconds > 600:
        return False
    else:
        return True

# get the url of the identifier
@app.route("/<identifier>", methods=["GET"])
def get_url(identifier):
    # data = request.json

    header = request.headers
    JWT = header.get('Authorization')

    info = get_user_by_JWT(JWT)
    if info == None:
        return "forbidden", 403

    user = info[0]
    prev_date_time = datetime.datetime.strptime(info[1], "%m/%d/%Y, %H:%M:%S")
    if check_jwt_vadility(prev_date_time, datetime.datetime.now()) == False:
        return "forbidden", 403
    
    if user not in urls.keys():
        urls[user] = {}

    #if id is found in urls, return its url, else return 404 not found
    url = urls[user].get(identifier)
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
    data = json.loads(data.decode())
    url = data['url']

    header = request.headers
    JWT = header.get('Authorization')

    info = get_user_by_JWT(JWT)
    if info == None:
        return "forbidden", 403

    user = info[0]
    prev_date_time = datetime.datetime.strptime(info[1], "%m/%d/%Y, %H:%M:%S")
    if check_jwt_vadility(prev_date_time, datetime.datetime.now()) == False:
        return "forbidden", 403

    print(urls)
    if user in urls.keys() and urls[user].get(identifier) != None:
        if check_url_validity(url) == False:
            return "Invalid URL", 400 #400 with an error if the update failed (e.g., the URL was invalid)
        else:
            urls[user][identifier] = url
            return "Updated", 200 #Updates the URL behind the given ID.
    else:   
        return "Not Found", 404 #404 if the ID does not exist
    
# delete the identifier
@app.route("/<identifier>", methods=["DELETE"])
def delete_identifier(identifier):
    # data = request.json
    header = request.headers
    JWT = header.get('Authorization')

    info = get_user_by_JWT(JWT)
    if info == None:
        return "forbidden", 403

    user = info[0]
    prev_date_time = datetime.datetime.strptime(info[1], "%m/%d/%Y, %H:%M:%S")
    if check_jwt_vadility(prev_date_time, datetime.datetime.now()) == False:
        return "forbidden", 403

    if user in urls.keys() and urls[user].get(identifier) != None:
        del urls[user][identifier]
        return "Deleted", 204 #find the identifier and delete it 
    else:
        return "Not Found", 404 #identifier not found
    
# get all the identifiers
@app.route("/", methods=["GET"])
def get_identifiers():
    # data = request.json
    header = request.headers
    JWT = header.get('Authorization')

    info = get_user_by_JWT(JWT)
    if info == None:
        return "forbidden", 403

    user = info[0]
    prev_date_time = datetime.datetime.strptime(info[1], "%m/%d/%Y, %H:%M:%S")
    if check_jwt_vadility(prev_date_time, datetime.datetime.now()) == False:
        return "forbidden", 403
    
    if user not in urls.keys():
        urls[user] = {}

    return urls[user], 200

# create a new identifier for the url
@app.route("/", methods=["POST"])
def create_identifier():
    data = request.json
    header = request.headers
    url = data.get('value')
    JWT = header.get('Authorization')

    info = get_user_by_JWT(JWT)
    if info == None:
        return "forbidden", 403

    user = info[0]
    prev_date_time = datetime.datetime.strptime(info[1], "%m/%d/%Y, %H:%M:%S")
    if check_jwt_vadility(prev_date_time, datetime.datetime.now()) == False:
        return "forbidden", 403
    # Check URL validity with a regex expression before creating a mapping for it
    if check_url_validity(url) == False:
        return  "Invalid URL", 400
    # Check whether the url already exists or not
    if user in urls.keys() and url in urls[user].values():
        #id = [k for k, v in urls.items() if v == url][0] 
        return 'identifier of {} already exists'.format(url), 400

    identifier = int2base64(hash(url))
    if user in urls.keys():
        urls[user][identifier] = url
    else:
        urls[user] = {}
        urls[user][identifier] = url

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
    # data = request.json
    header = request.headers
    JWT = header.get('Authorization')

    info = get_user_by_JWT(JWT)
    if info == None:
        return "forbidden", 403

    user = info[0]
    prev_date_time = datetime.datetime.strptime(info[1], "%m/%d/%Y, %H:%M:%S")
    if check_jwt_vadility(prev_date_time, datetime.datetime.now()) == False:
        return "forbidden", 403
    
    if user in urls.keys():
        urls[user].clear()
    return "All Deleted", 404

# Create a new user with username and password and store it in a table
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username in users.keys():
        status_code = 409
        msg = json.dumps({'detail': 'duplicate'})
        response = make_response(msg, status_code)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        users[username] = password
        return "Created", 201
    
# Update the user’s password if the user presents the correct old password, or else return 403.
@app.route("/users", methods=["PUT"])
def update_user():
    data = request.json
    username = data.get('username')
    old_password = data.get('password')
    new_password = data.get('new_password')
    print(users, users.get(username))
    if users.get(username) == old_password:
        users[username] = new_password
        status_code = 200
        msg = json.dumps({'detail': 'Updated'})
        response = make_response(msg, status_code)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        status_code = 403
        msg = json.dumps({'detail': 'forbidden'})
        response = make_response(msg, status_code)
        response.headers['Content-Type'] = 'application/json'
        return response
    
# Check if username and password exist in the table and generate a JWT or else return 403
@app.route("/users/login", methods=["POST"])
def get_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if users.get(username) == password:
        status_code = 200
        JWT = generate_JWT(username)
        msg = json.dumps({'token': JWT})
        response = make_response(msg, status_code)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        status_code = 403
        msg = json.dumps({'detail': 'forbidden'})
        response = make_response(msg, status_code)
        response.headers['Content-Type'] = 'application/json'
        return response

def check_url_validity(url):
    # regex pattern for url validation, source from https://uibakery.io/regex-library/url-regex-python https://blog.csdn.net/qq_42019226/article/details/126395030
    pattern_1 = re.compile("^((https|http|ftp|rtsp|mms)?:\/\/)(([A-Za-z0-9]+-[A-Za-z0-9]+|[A-Za-z0-9]+)\.)+([A-Za-z]{2,6})(:\d+)?(\/.*)?(\?.*)?(#.*)?$")
    pattern_2 = re.compile("^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$")
    if pattern_1.match(url) or pattern_2.match(url):
        return True
    else:
        return False
    
