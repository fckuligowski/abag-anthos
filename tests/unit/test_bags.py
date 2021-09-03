import json

def test_home_page(test_bags):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_bags.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_history(test_bags):
    """
    GIVEN a Bag Id
    WHEN the /history page is requested (GET)
    THEN the bag_id is found in the first item in return array
    """
    bag_id = '001'
    response = test_bags.get('/history/%s' % bag_id)
    assert response.status_code == 200
    response_body = json.loads(response.data)
    assert response_body[0]['bag'] == bag_id

def test_status(test_bags):
    """
    GIVEN a Bag Id
    WHEN the /status page is requested (GET)
    THEN the bag_id is found in the returned object
    """
    bag_id = '001'
    response = test_bags.get('/status/%s' % bag_id)
    assert response.status_code == 200
    response_body = json.loads(response.data)
    assert response_body['bag'] == bag_id
