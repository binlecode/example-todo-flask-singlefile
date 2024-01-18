# a minimal single script flask app
#
# serve todos REST endpoints with raw sql without models


from werkzeug.exceptions import HTTPException
import json
import uuid
from flask import Flask, request, Response
import sqlite3
import os

import logging

LOG = logging.getLogger(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
LOG.debug(f">> basedir: {basedir}")


# reuse the sqlite3 db created by todos.py app
DB_PATH = os.path.join(basedir, "todos.db")


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hi! This is a mini Todos (REST + Sql) single-file app."


@app.route("/todos")
def get_todos():
    try:
        conn = sqlite3.connect(DB_PATH)

        # use row factory to transform tuple result set to dict list
        # C is cursor, R is each row in result set
        conn.row_factory = lambda C, R: {
            c[0]: R[i] for i, c in enumerate(C.description)
        }

        # Once a connection is established, we use the cursor
        # object to execute queries
        c = conn.cursor()

        c.execute("select * from todo")
        todo_list = c.fetchall()

        # with row_factory, todo_list is serializable to json directly
        return {"todo_list": todo_list, "count": len(todo_list)}

        # or dump todo_list to json explicitly
        # return Response(json.dumps(todo_list), mimetype='application/json')
    except Exception as e:
        print("Error: ", e)
        return {}


# Example call:
# curl -X POST http://127.0.0.1:5000/todos -d '{"title": "Implement POST endpoint"}' -H 'Content-Type: application/json'
#
@app.route("/todos", methods=["POST"])
def add_todo():
    # try:
    # Get item from the POST body
    todo_json = request.get_json()
    title = todo_json["title"]  # todo: validation

    # test raising error from within route action
    # raise Exception('error thrown from add_todo')

    # generate pk id with uuid4
    id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("insert into todo(id, title) values(?, ?)", (id, title))
    conn.commit()
    return {"data": {"id": id, "title": title, "complete": False}}
    # except Exception as e:
    #     print('Error: ', e)
    #     return {}


@app.errorhandler(HTTPException)
def handle_exception(e):
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response
    # return Response(err_json, mimetype='application/json', status=500)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS todo")
    c.execute(
        # for multi-line SQL string, note the space at the end of each line
        "CREATE TABLE todo ( "
        "id TEXT(48) NOT NULL, "
        "title VARCHAR(128), "
        "complete BOOLEAN, "
        "PRIMARY KEY (id), "
        "CHECK (complete IN (0, 1)) "
        ")"
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
