# WSCS_assignment_1
This Flask project implements a URL manager with six main functions:

## 1. Get URL by Identifier: GET /&lt;identifier&gt;
Retrieves the URL associated with the given identifier.

## 2. Update URL by Identifier: PUT /&lt;identifier&gt;
Updates the URL associated with the given identifier with the new one provided in JSON format.

## 3. Delete URL by Identifier: DELETE /&lt;identifier&gt;
Deletes the identifier and its associated URL.

## 4. Get All URLs: GET /
Retrieves all URLs along with their corresponding identifiers.

## 5. Generate Identifier for URL: POST /
Generates a new identifier for the URL provided in JSON format using a custom hash algorithm.

## 6. Delete All URLs and Identifiers: DELETE /
Deletes all stored URLs and identifiers.

## 7. Create New User: POST /users
Create a new user with username and password and store it in a table

## 8. Change password: PUT /users
Update the user’s password if the user presents the correct old password

## 9. Login: POST /users/login
Check if username and password exist in the table and generate a JWT

# How to Install Flask
You can install Flask simply using pip, run the following command in your terminal:
```
pip install flask
```
you can find more information on the website of Flask.

https://flask.palletsprojects.com/en/3.0.x/installation/

# How to Run the Server
Clone this repository to your local machine.

Navigate to the project directory in your terminal.

Run the following command to start the Flask server:
```
flask --app main run
```
The server will start running locally on http://127.0.0.1:5000/.

# How to Call the Services
You can call the services using curl, a command-line tool for transferring data with URLs. Here are examples of how to call each service:

## 1. Get URL by Identifier
curl -X GET -H "Content-Type: application/json" -d '{"JWT": "JWT"}' http://127.0.0.1:5000/<identifier&gt;

## 2. Update URL by Identifier
curl -X PUT -H "Content-Type: application/json" -d '{"url": "https://example.com/new", "JWT": "JWT"}' http://127.0.0.1:5000/<identifier&gt;

## 3. Delete URL by Identifier
curl -X DELETE -H "Content-Type: application/json" -d '{"JWT": "JWT"}' http://127.0.0.1:5000/<identifier&gt;

## 4. Get All URLs
curl -X GET -H "Content-Type: application/json" -d '{"JWT": "JWT"}' http://127.0.0.1:5000/

## 5. Generate Identifier for URL
curl -X POST -H "Content-Type: application/json" -d '{"value": "https://example.com", "JWT": "JWT"}' http://127.0.0.1:5000/

## 6. Delete All URLs and Identifiers
curl -X DELETE -H "Content-Type: application/json" -d '{"JWT": "JWT"}' http://127.0.0.1:5000/

## 7. Create New User
curl -X POST -H "Content-Type: application/json" -d '{"username": "username", "password": "password"}' http://127.0.0.1:5000/users

## 8. Update Password
curl -X PUT -H "Content-Type: application/json" -d '{"username": "username", "password": "old_password", "new_password":"new_password"}' http://127.0.0.1:5000/users

## 9. Login
curl -X POST -H "Content-Type: application/json" -d '{"username": "username", "password": "password"}' http://127.0.0.1:5000/users/login



