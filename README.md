## URL Shortener on Python Flask
### NavBar

0. [Run the app](#Run-the-app)
1. [Use the app](#Use-the-app)
2. [Use the API](#Use-the-API)
    1. [GET request](#GET-request)
    2. [POST requests](#POST-requests)
    3. [Error handler](#Error-handler)
3. [Test API](#Test-API)
### Run the app

```
$ git clone https://github.com/bmisyurk/jooble_test_python_dev
$ pip install -r requirements.txt
$ python -c "from app import db; db.drop_all(); db.create_all()"
$ python app.py
```

 ### Use the app
http://127.0.0.1:5000

Original URL - link which to shorten

Lifetime - short link lifetime in days, and after these days not redirected on original url.


### Use the API
#### GET request
http://127.0.0.1:5000/get_data/<short_link>

Get all data via short link, which has already been generated and stored in DataBase(DB). For e.g. GET: http://127.0.0.1:5000/get_data/DV5V. You should send only the **hash of url** itself, without the host address.
Response body:
```json
{
  "date_created": "Thu, 15 Oct 2020 11:35:01 GMT",
  "date_expire": "Thu, 14 Oct 2021 13:19:51 GMT",
  "lifetime": "364 days",
  "original_link": "http://soska.jooble.com/",
  "short_link": "http://127.0.0.1:5000/1lRF"
}
```
#### POST requests
http://127.0.0.1:5000/add_link

key `original_links` takes string data type as one link as two and more.

key `lifetime` takes from 1 to 365 days, integer data type. It cannot be empty.

Request body:
`Content-Type: application/json`
```json
{
  "original_links" : "http://1234.com",
  "lifetime": "364"
}
```
Response body:
```json
{
  "code": 200,
  "lifetime": "364 days",
  "log": "Successfully added link",
  "new_link": "http://127.0.0.1:5000/Bb12",
  "original_link": "http://1234.com"
}
```
For two and more links, you should type with separator `,` in key `original_links`:

Request body:
```json
{
  "original_links" : "http://1234.com, https://github.com, http://soska.jooble.com/",
  "lifetime":"364"
}
```
If links two and more, response body returns status code and log of success or fail response.

Request body:
```json
{
  "code": 200,
  "log": "Successfully added links"
}
```


key `lifetime` not required. If not exist - lifetime of link default 90 days.
Request body:
```json
{
  "original_links" : "http://1234.com"
}
```
Response body:
```json
{
  "code": 200,
  "lifetime": "90 days",
  "log": "Successfully added link",
  "new_link": "http://127.0.0.1:5000/Bb59",
  "original_link": "http://1234.com"
}
```
#### Error handler
If request body was not сorrect, response returns status and error:
```json
{
  "error": "invalid literal for int() with base 10: '364.0'",
  "status": "Bad Request"
}
```
```json
{
  "error": "key 'lifetime' is out of range",
  "status": "Bad Request"
}

```
### Test API

