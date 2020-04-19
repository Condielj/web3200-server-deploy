**DVD**

Attributes:
* title (string)
* rating (string) ((rating as in PG, PG13, R, etc.))
* price (string)
* date (string) ((date the the store purchased/acquired the DVD to see how long it has been in inventory))
* genre (string)

**User**

Attributes:
* email (string)
* password (string) ((stored encrypted))
* fname (string) ((first name))
* lname (string) ((last name))

**Session**

Attributes:
* sessionId (string)
* sessionData (dictionary)
* uid (string) ((user id if there happens to be one logged in, stored inside sessionData))

## Schema

```sql
CREATE TABLE dvds (
inv SERIAL PRIMARY KEY,
title TEXT,
rating TEXT,
price TEXT,
date TEXT,
genre TEXT);
```

```sql
CREATE TABLE users (
uid SERIAL PRIMARY KEY,
email TEXT,
password TEXT,
fname TEXT,
lname TEXT);
```

## REST Endpoints

Name                                   | Method | Path
---------------------------------------|--------|------------------
Retrieve dvd collection                | GET    | /dvds
Retrieve dvd member                    | GET    | /dvds/*\<inv\>*
Create dvd member                      | POST   | /dvds
Update dvd member                      | PUT    | /dvds/*\<inv\>*
Delete dvd member                      | DELETE | /dvds/*\<inv\>*
Create user member (registration)      | POST   | /users
Create session member (authentication) | POST   | /sessions


## Password Hashing Method

Bcrypt was used as provided by the passlib python library.
