# django-api
A Django restframework based API with MySQL backend, Nginx frontend wrapped up with docker-compose.

## Configuration
Rename or link the file env.example to .env and configure variables. Replace the values you need:
```
# MySQL
MYSQL_ROOT_PASSWORD=your_password
MYSQL_DATABASE=your_db_name
MYSQL_USER=your_db_user
MYSQL_PASSWORD=your_password

# Django
DJANGO_DEBUG=False
DJANGO_SUPERUSER_NAME=your_admin
DJANGO_SUPERUSER_PASSWORD=your_password
```
**`MYSQL_ROOT_PASSWORD`**, **`MYSQL_DATABASE`**, **`MYSQL_USER`**, **`MYSQL_PASSWORD`** variables are required for MySQL.  
**`MYSQL_DATABASE`**, **`MYSQL_USER`**, **`MYSQL_PASSWORD`** variables are required for Django, too.  
**`DJANGO_DEBUG`** set Django run in debug mode or not.
**`DJANGO_SUPERUSER_NAME`** and **`DJANGO_SUPERUSER_PASSWORD`** are required for creating superuser of Django admin backend.

## Startup
In the root of project, run:
```bash
docker-compose up -d
```
The frontend Nginx shoud be running on port 80 and bound to your host 0.0.0.0:80.  
Go to [`http://<your_host_ip>/admin/`](http://<your_host_ip>/admin/) on a web browser to access Django Admin backend to manage Django account.  
Go to [`http://<your_host_ip>/api-token/`](http://<your_host_ip>/api-token/) to request API token.  
Go to [`http://<your_host_ip>/api/users/`](http://<your_host_ip>/api/users/) to request API.

## API Request
| Endpoint                           | HTTP Method             | Description             |
| :--------------------------------: | :---------------------: | :---------------------: |
| `/api-token/`                      | `GET`                   | `Get API Token`         |
| `/api/users/`                      | `GET`                   | `List all users`        |
| `/api/users/`                      | `POST`                  | `Create a new user`     |
| `/api/users/:id`                   | `GET`                   | `Get user`              |
| `/api/users/:id`                   | `PUT`                   | `Update a user`         |
| `/api/users/:id`                   | `DELETE`                | `Delete a user`         |

## Test API locally using curl
### Get API Token
* request with your django username and password in HTTP Header
```bash
curl -i -X POST -H 'Content-Type: application/json' -d '{"username":"your_admin", "password":"your_password"}' http://localhost/api-token/
```

* response
```bash
HTTP/1.1 200 OK
Date: Sun, 21 Nov 2021 07:33:02 GMT
Server: WSGIServer/0.2 CPython/3.8.10
Content-Type: application/json
Allow: POST, OPTIONS
X-Frame-Options: DENY
Content-Length: 52
Vary: Cookie
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin

{"token":"your_token"}
```

### List users   
* request with your API token in HTTP Header
```bash
curl -i -H 'Authorization: Token your_token' http://localhost/api/users/
```

* response
```bash
HTTP/1.1 200 OK
Server: nginx
Date: Sun, 21 Nov 2021 07:34:02 GMT
Content-Type: application/json
Content-Length: 336
Connection: keep-alive
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin

[
  {
    "id": 1,
    "name": "user1",
    "job_title": "SRE",
    "communicate_information": {
      "email": "user1@123.com",
      "mobile": "0937123456"
    }
  },
  {
    "id": 2,
    "name": "user2",
    "job_title": "Dev",
    "communicate_information": {
      "email": "user2@456.net",
      "mobile": "0935789000"
    }
  }
]
```

### Create user
* request with your API token in HTTP Header
```bash
curl -i -X POST -H 'Content-Type: application/json' -H 'Authorization: Token your_token' http://localhost/api/users/ -d '
{
    "name": "user3",
    "job_title": "QA",
    "communicate_information": {
        "email": "user3@xyz.net",
        "mobile": "0936111222"
    }
}'
```
* response
```bash
HTTP/1.1 201 Created
Server: nginx
Date: Sun, 21 Nov 2021 07:35:33 GMT
Content-Type: application/json
Content-Length: 146
Connection: keep-alive
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin

{
  "id": 3,
  "name": "user3",
  "job_title": "QA",
  "communicate_information": {
    "email": "user3@xyz.net",
    "mobile": "0936111222"
  }
}
```
### Update user
* request with your API token in HTTP Header
```bash
curl -i -X PUT -H 'Content-Type: application/json' -H 'Authorization: Token your_token' http://localhost/api/users/3/ -d '
{
    "name": "user3",
    "job_title": "OP",
    "communicate_information": {
        "email": "user3@xyz.net",
        "mobile": "0951123456"
    }
}'
```

* response
```bash
HTTP/1.1 200 OK
Server: nginx
Date: Sun, 21 Nov 2021 07:37:42 GMT
Content-Type: application/json
Content-Length: 146
Connection: keep-alive
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin

{
  "id": 3,
  "name": "user3",
  "job_title": "OP",
  "communicate_information": {
    "email": "user3@xyz.net",
    "mobile": "0951123456"
  }
}
```
### Delete user
* request with your API token in HTTP Header
```bash
curl -i -X DELETE -H 'Authorization: Token your_token' http://localhost/api/users/3/
```
* response
```bash
HTTP/1.1 204 No Content
Server: nginx
Date: Sun, 21 Nov 2021 07:38:12 GMT
Content-Length: 0
Connection: keep-alive
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
```
