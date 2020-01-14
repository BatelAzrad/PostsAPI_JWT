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

## Saving the token in variable
```
token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNTc5MDM4NDE2LCJuYmYiOjE1NzkwMzg0MTYsImV4cCI6MTU3OTAzODcxNn0.s0nqLc69sdYGtvRHbuz4LBIeVyb-d5-vTbLMnuyRMao
```

## Identify the token owner
```
curl -i http://54.93.232.155:9000/whoami -H "Authorization: jwt $token"
```

## Response of the owner
```
"ID:1, User:batel"
```

## Get all users
```
curl -i http://54.93.232.155:9000/users -H "Authorization: jwt $token"
```

## All users response
```
[
  [
    1,
    "batel",
    "123456",
    "admin"
  ],
  [
    2,
    "kira",
    "123456",
    "admin"
  ],
  [
    3,
    "red",
    "123456",
    "user"
  ],
]
```

## Get all posts
```
curl -i http://54.93.232.155:9000/posts -H "Authorization: jwt $token"
```

## All posts response
```
[
  [
    1,
    "kira",
    "3 places to bury my bone",
    "1) Yard, 2) Under my parents bed, 3) Inside the pot. - Woff-Woff Kira",
    "",
    "",
    2
  ],
  [
    2,
    "batel",
    "My developing skills",
    "Python, Javascript, Java, HTML, CSS, etc.",
    "Software engineer skills",
    "#Developer #Software",
    1
  ],
  [
    3,
    "kira",
    "Test Title woof",
    "Test Content",
    "Admin content",
    "#Tag1 #tag2",
    1
  ]
]
```
