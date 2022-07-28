[![CI/CD api_yamdb](https://github.com/photometer/yamdb_final/workflows/CI%2FCD%20api_yamdb/badge.svg)](https://github.com/photometer/yamdb_final/actions/workflows/yamdb_workflow.yml)

[comment]: <> (This is for pytest: https://github.com/photometer/yamdb_final/workflows/yamdb_workflow.yml/badge.svg)

# API Yamdb

### Project description

The YaMDb project collects user feedback on works. The works are divided into 
categories: "Books", "Films", "Music". The list of categories can be expanded 
by the administrator. The works themselves are not stored in YaMDb; you 
cannot watch a movie or listen to music here. In each category there are 
works: books, films or music. A work can be assigned a genre from the 
predefined list (for example, "Fairytale", "Rock" or "Arthouse"). New genres 
can only be created by the administrator. Users can leave text reviews for 
works and rate the work from 1 to 10; from user scores, an average sckre of 
the work is formed - a rating. A user can leave only one review per work.

Information about the possibilities of the project can be found at the 
endpoint ```/redoc/```.

### Technologies

- Python;
- Django-Rest-Framework;
- PostgreSQL;
- Gunicorn;
- Docker/Docker-compose;
- Nginx;
- Yandex.Cloud;
- Github Actions.

<details>
  <summary><h3> Project installation (Windows) </h3></summary>

Clone repository and switch to it on the command line:

```bash
git clone https://github.com/photometer/api_yamdb
cd api_yamdb
```

Don't forget to create ```.env``` file and add your secret key in it:
```
SECRET_KEY=Your_secret_key
```

Create and activate vurtual environment:

```bash
python -m venv venv
source venv/scripts/activate
```

Install dependencies from the file requirements.txt:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Go to the directory with the file ```manage.py```:

```bash
cd api_yamdb
```

Make migrations:

```
python manage.py migrate
```

Fill the database with first values:

```bash
cd ..
python csvread.py
```

Run the project:

```bash
cd api_yamdb
python manage.py runserver
```
</details>

<details>
  <summary><h3> API request examples </h3></summary>
  <details>
    <summary><h5> 1. User registration and issuance of tokens </h5></summary>

- New user registration (receiving a confirmation code for the transmitted 
email):
```
POST /api/v1/auth/signup/
{
  "email": "string",
  "username": "string"
}
```

- Getting JWT-token in exchange for username and confirmation code:
```
POST /api/v1/auth/token/
{
  "username": "string",
  "confirmation_code": "string"
}
```
  </details>
  <details>
    <summary><h5> 2. Categories of works </h5></summary>

- Getting list of all categories:
```
GET /api/v1/categories/
```

- Adding new castegory:
**only for administrators*
```
POST /api/v1/categories/
{
  "name": "string",
  "slug": "string"
}
```

- Deleting category:
**only for administrators*
```
DELETE /api/v1/categories/{slug}/
```
  </details>
  <details>
    <summary><h5> 3. Genres of works </h5></summary>

Similar to categories of works, but by endpoint ```/genres/```.
  </details>
  <details>
    <summary><h5> 4. Works </h5></summary>

- Getting list of all works:
```
GET /api/v1/titles/
```

- Adding new work:
**only for administrators*
```
POST /api/v1/titles/
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

- Getting information about the work:
```
GET /api/v1/titles/{titles_id}/
```

- Partial updating of information about the work:
**only for administrators*
```
PATCH /api/v1/titles/{titles_id}/
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

- Deleting the work:
**only for administrators*
```
DELETE /api/v1/titles/{titles_id}/
```
  </details>
  <details>
    <summary><h5> 5. Reviews </h5></summary>

- Getting list of all reviews on the work:
```
GET /api/v1/titles/{title_id}/reviews/
```

- Adding new review on the work:
**only for authenticated users*
```
POST /api/v1/titles/{title_id}/reviews/
{
  "text": "string",
  "score": 1
}
```

- Getting review by id:
```
GET /api/v1/titles/{title_id}/reviews/{review_id}/
```

- Partial updating of review by id:
**for review author, moderator or administrator*
```
PATCH /api/v1/titles/{title_id}/reviews/{review_id}/
{
  "text": "string",
  "score": 1
}
```

- Deleting review by id:
**for review author, moderator or administrator*
```
DELETE /api/v1/titles/{title_id}/reviews/{review_id}/
```
  </details>
  <details>
    <summary><h5> 6. Comments on reviews </h5></summary>

- Getting list of comments on the review:
```
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

- Adding comment on the review:
**only for authenticated users*
```
POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
{
  "text": "string"
}
```

- Getting the comment on the review by id:
```
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

- Partial updating of the comment on the review by id:
**for the comment author, moderator or administrator*
```
PATCH /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
{
  "text": "string"
}
```

- Partial updating of the comment on the review:
**for the comment author, moderator or administrator*
```
DELETE /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
  </details>
  <details>
    <summary><h5> 7. Users </h5></summary>

- Getting list of all users:
**only for administrators*
```
GET /api/v1/users/
```

- Adding user:
**only for administrators*
```
POST /api/v1/users/
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

- Getting user by username:
**only for administrators*
```
GET /api/v1/users/{username}/
```

- Updating user data by username:
**only for administrators*
```
PATCH /api/v1/users/{username}/
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

- Deleting user by username:
**only for administrators*
```
DELETE /api/v1/users/{username}/
```

- Getting your account information:
**only for authenticated users*
```
GET /api/v1/users/me/
```

- Updating your account information:
**only for authenticated users*
```
PATCH /api/v1/users/me/
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}
```
  </details>
</details>

### Authors
[Androsova Elizaveta](https://github.com/photometer), 
[Max Abramov](https://github.com/AbramovMax), 
[Dmitry Shotel](https://github.com/ShotelYa)
