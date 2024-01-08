# academically-thesis-api

### create a venv first
```
$ mkdir thesis-api
$ cd thesis-api
$ python3 -m venv .venv
$ source .venv/bin/activate
```

### flask quickstart
```
$ pip install Flask
$ flask -app <source> run
$ python3 -m flask run
```

### requirements
```
python3 -m pip install Flask, numpy, tensorflow, scikit-learn, flask-restplus, flask2postman, Flask-Migrate
```

### update db schema
```
flask db init
flask db migrate -m "migrate message, include notes what changed"
flask db upgrade
```
### generate postman collection
```
flask2postman app.api --name "AcademicAlly API Collection" --folders > academically_api.json
```