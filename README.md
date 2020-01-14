A Posts API (CRUD) with permission management using JWT

## AWS EC2 deployment for testing hands-on
[URL](http://54.93.232.155:9000/)


## Generating token using JWT
```
curl -i --header "Content-Type: application/json" --request POST \
--data '{"username":"batel","password":"123456"}' http://54.93.232.155:9000/auth
```

## Running the application
```
python app.py
```

