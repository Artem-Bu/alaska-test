import requests
from copy import deepcopy

test_bears = [{"bear_type":"POLAR","bear_name":"UMKA","bear_age":3}, {"bear_type":"GUMMY","bear_name":"VINNIE","bear_age":13},
                {"bear_type":"BROWN","bear_name":"MEDVED","bear_age":55}, {"bear_type":"BLACK","bear_name":"GRIZZLY","bear_age":11}]
test_answ = [{"bear_id":1, "bear_type":"POLAR","bear_name":"UMKA","bear_age":3.0}, {"bear_id":2, "bear_type":"GUMMY","bear_name":"VINNIE","bear_age":13.0},
                {"bear_id":3, "bear_type":"BROWN","bear_name":"MEDVED","bear_age":55.0}, {"bear_id":4, "bear_type":"BLACK","bear_name":"GRIZZLY","bear_age":11.0}]

class TestPutRequests(object):
    def test_bear_modify(self, bear):
        response = requests.post(url=bear, json=test_bears[0])
        assert response.status_code == 200
        test_bear = response.text
        response = requests.put(url=bear + '/' + test_bear, json=test_bears[3])
        assert response.status_code == 200
        new_bear = deepcopy(test_answ[3])
        new_bear["bear_id"] = 1
        response = requests.get(url=bear + '/' + test_bear)
        assert response.json() == test_answ[3]

    def test_bear_modify_bad_attr(self, bear):
        response = requests.post(url=bear, json=test_bears[0])
        assert response.status_code == 200
        test_bear = response.text
        bad_bear = deepcopy(test_bears[3])
        bad_bear["bear_type"] = "GROLAR"
        response = requests.put(url=bear+ '/' + test_bear, json=bad_bear)
        assert response.status_code == 500

    def test_nonexistent_bear_modify(self, bear):
        response = requests.post(url=bear, json=test_bears[0])
        assert response.status_code == 200
        response = requests.put(url=bear + '/12', json=test_bears[3])
        assert response.status_code == 200
        assert response.text == 'EMPTY'

    def test_deleted_bear_modify(self, bear):
        response = requests.post(url=bear, json=test_bears[0])
        assert response.status_code == 200
        test_bear = response.text
        response = requests.delete(url=bear + '/' + test_bear)
        assert response.status_code == 200
        response = requests.put(url=bear + '/' + test_bear, json=test_bears[3])
        assert response.status_code == 200
        assert response.text == 'EMPTY'

    def test_wrong_endpoint(self, bear):
        for test_bear in test_bears:
            response = requests.post(url=bear, json=test_bear)
            assert response.status_code == 200
        response = requests.put(url=bear, json=test_bears)
        assert response.status_code == 404
