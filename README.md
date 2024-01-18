# todos-flask-singlefile

A single-file minimal web stack with flask and sql.

## run application

Runtime env and dependencies:

```sh
pyenv shell 3.10
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

To run:

```sh
FLASK_DEBUG=1 python todos_rest.py
# or
FLASK_DEBUG=1 flask --app todos_rest run
# or run shell
FLASK_DEBUG=1 flask --app todos_rest shell
```

This `todos_rest.py` will create a sqlite3 `todos.db` file.

## project environment setup

```sh
pyenv shell 3.10
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
# pip install setuptools --force-reinstall
pip install flask
pip install black
pip freeze > requirements.txt
```
