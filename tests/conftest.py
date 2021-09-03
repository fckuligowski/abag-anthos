import pytest
from project import create_app
from google.cloud import storage
from google.cloud.storage import Blob

# Call the Application Factory function to construct a Flask application instance
# using the standard configuration defined in /instance/flask.cfg
# app = create_app('test_config.py')

@pytest.fixture(scope='module')
def test_bags():
    # Call the Application Factory function to construct a Flask application instance
    # using the standard configuration defined in /instance/test_config.py
    flask_app = create_app('test_config.py')

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    # Teardown - drop the database and remove app context
    drop_db(flask_app)
    ctx.pop()

def drop_db(flask_app):
    """
        Remove the bucket and object that we used for testing
    """
    storage_client = storage.Client()
    bucket_name = flask_app.config.get('DATA_BUCKET_NAME')
    bucket = storage_client.get_bucket(bucket_name)
    blob = Blob(flask_app.config.get('DATA_FILE_NAME'), bucket)
    if blob.exists():
        blob.delete()
    bucket.delete()