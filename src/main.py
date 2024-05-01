from http import HTTPStatus
import flask
from flask import request
from src import db
import os


app = flask.Flask(__name__)

connection = db.get_connection()


@app.get("/repository")
def get_repositories():
    return db.get_repositories(connection)


@app.post("/repository/create")
def create_repository():
    return db.create_repository(connection, request.json), HTTPStatus.CREATED


@app.put("/repository/update")
def update_repository():
    result = db.update_repository(connection, request.json)
    if len(result) == 0:
        return "", HTTPStatus.NOT_FOUND

    return '', HTTPStatus.NO_CONTENT


@app.delete("/repository/delete")
def delete_repository():
    result = db.delete_repository(connection, request.json)
    if len(result) == 0:
        return "", HTTPStatus.NOT_FOUND

    return '', HTTPStatus.NO_CONTENT


if __name__ == "__main__":
    app.run(port=os.getenv('FLASK_PORT'))
