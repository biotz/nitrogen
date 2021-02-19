from PIL import Image
from assimilation.classification import categories, predict, preprocess


def test_categories():
    assert len(categories) == 1000


def open_image(ifile):
    return Image.open(f"/app/tests/resources/{ifile}.jpg")


def test_preprocess():
    assert list(preprocess(open_image("cat")).size()) == [3, 224, 224]


def test_magnet_in_categories():
    print(categories)
    assert "magnet" not in categories


def prediction(ifile):
    return predict(f"/app/tests/resources/{ifile}.jpg")


def test_cat():
    r = prediction("cat")
    assert r["prediction"] == "Persian cat"
    assert r["probability"] > 0.8


def test_cat():
    r = prediction("dog")
    assert r["prediction"] == "Samoyed"
    assert r["probability"] > 0.8
