# Login

## Request

POST 'login/'

```json
{
    "auth": {
        "user-name": "xxx",
        "passwork": "xxx"
    }
}
```

## Response

### 1. Login success

200 OK

### 2. Wrong format

400 Bad Request

### 3. No such user

401 Unauthorized

### 4. Wrong Password

403 Forbidden

# Logout

## Request

POST 'logout/'

## Response

200 OK

# Submit Pathole

## Request

POST 'submit/'

```json
{
    "pathole": {
        "address": "xxxxxx",
        "size": 1~10,
        "location": "middle/curb/...."
    }
}
```

## Response

### 1. Submit success

200 OK

### 2. Wrong format

400 Bad Request

### 3. Not Login

401 Unauthorized

# User Query Submitted Pathole

## Request

POST 'check-submit/'

## Response

### 1. Success

200 OK

```json
{
    "submit": [
        {
            "address": "xxx",
            "size": 1~10,
            "location": "middle/curb/..."
        },
        {
            "address": "xxx",
            "size": 1~10,
            "location": "middle/curb/..."
        }
    ]
}
```

### 2. Not Login

401 Unauthorized

# Test Part

## User 1

username: lijian
password: 12345678fuck

## User 2

username: zhongjinghui
password: 12345678fuck

## User 3

username: yuzhiwen
password: 12345678fuck




