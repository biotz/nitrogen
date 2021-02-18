from nitrogen.boundary.storage import cloud_image, local_image_path


def test_download():
    assert cloud_image("cat") == "/tmp/cat.jpg"

def test_get_local():
    assert str(local_image_path("dog")) == "/app/tests/resources/dog.jpg"
