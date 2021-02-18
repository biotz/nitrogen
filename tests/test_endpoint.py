import pytest
from nitrogen.endpoint import create_app, assimilation_blueprint


app = create_app()


def test_index_returns_200():
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.json["status"] == "ok"


def test_index_put_not_allowed():
    request, response = app.test_client.put("/")
    assert response.status == 405


app.blueprint(assimilation_blueprint)


def test_answer_correct():
    request, response = app.test_client.get("/assimilation/validate-answer/42")
    assert response.status == 200


def test_answer_string():
    request, response = app.test_client.get("/assimilation/validate-answer/happiness")
    assert response.status == 404


def test_answer_low():
    request, response = app.test_client.get("/assimilation/validate-answer/41")
    assert response.status == 200


def test_classification():
    request, response = app.test_client.get("/assimilation/validate-answer/42")
    assert response.status == 200


def test_classification():
    request, response = app.test_client.get("/assimilation/cat-or-dog/local/cat")
    assert response.status == 200
