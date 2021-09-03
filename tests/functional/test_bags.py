from datetime import datetime
import json

def test_scan(test_bags):
    """
    GIVEN a Flask application
    WHEN the '/scan' page is used (POST)
    THEN check the response is valid
    WHEN the '/status' page is used (GET)
    THEN that last scan is the one returned
    """
    bag_id = '002'
    now = datetime.now()
    datestr = now.strftime('%Y-%m-%d %H:%M:%S.%f')
    data = {
        "bag": bag_id,
        "scan_time": datestr,
        "location": "AATEST002"
    }
    headers={'Content-Type': 'application/json'}
    response = test_bags.post('/scan', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    response = test_bags.get('/status/%s' % bag_id)
    assert response.status_code == 200
    response_body = json.loads(response.data)
    assert response_body['scan_time'] == datestr