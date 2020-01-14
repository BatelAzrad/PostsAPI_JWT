A Posts API (CRUD) with permission management using JWT

## AWS EC2 deployment for testing hands-on
[URL](http://54.93.232.155:9000/)


## Generating token using JWT
```
curl -i --header "Content-Type: application/json" --request POST \
--data '{"username":"batel","password":"123456"}' http://54.93.232.155:9000/auth
```

## Response token
```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNTc5MDM4NDE2LCJuYmYiOjE1NzkwMzg0MTYsImV4cCI6MTU3OTAzODcxNn0.s0nqLc69sdYGtvRHbuz4LBIeVyb-d5-vTbLMnuyRMao"
}

```

