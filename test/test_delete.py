import requests
from copy import deepcopy

test_bears = [{"bear_type":"POLAR","bear_name":"UMKA","bear_age":3}, {"bear_type":"GUMMY","bear_name":"VINNIE","bear_age":13},
                {"bear_type":"BROWN","bear_name":"MEDVED","bear_age":55}, {"bear_type":"BLACK","bear_name":"GRIZZLY","bear_age":11}]
test_answ = [{"bear_id":1, "bear_type":"POLAR","bear_name":"UMKA","bear_age":3.0}, {"bear_id":2, "bear_type":"GUMMY","bear_name":"VINNIE","bear_age":13.0},
                {"bear_id":3, "bear_type":"BROWN","bear_name":"MEDVED","bear_age":55.0}, {"bear_id":4, "bear_type":"BLACK","bear_name":"GRIZZLY","bear_age":11.0}]

class TestDeleteRequests(object):
    def test_delete_all_bears(self, bear):
        for test_bear in test_bears:
            response = requests.post(url=bear, json=test_bear)
            assert response.status_code == 200
        response = requests.delete(bear)
        assert response.status_code == 200
        response = requests.get(bear)
        assert response.status_code == 200
        assert response.json() == []

    def test_delete_bear(self, bear):
        response = requests.post(url=bear, json=test_bears[0])
        assert response.status_code == 200
        test_bear = response.text
        response = requests.post(url=bear, json=test_bears[2])
        test_second_bear = response.text
        assert response.status_code == 200
        test_answ[2]["bear_id"] = int(test_second_bear)
        response = requests.delete(url=bear + '/' + test_bear)
        assert response.status_code == 200
        response = requests.get(bear)
        assert response.status_code == 200
        assert response.json() == [test_answ[2]]

    def test_delete_nonexistent_bear(self, bear):
        response = requests.post(url=bear, json=test_bears[0])
        assert response.status_code == 200
        response = requests.delete(url=bear + '/3')
        assert response.status_code == 200
        response = requests.get(bear)
        assert response.status_code == 200
        assert response.json() == [test_answ[0]]

    def test_delete_deleted_bear(self, bear):
        response = requests.post(url=bear, json=test_bears[0])
        assert response.status_code == 200
        test_bear = response.text
        response = requests.post(url=bear, json=test_bears[2])
        assert response.status_code == 200
        test_second_bear = response.text
        test_answ[2]["bear_id"] = int(test_second_bear)
        response = requests.delete(url=bear + '/' + test_bear)
        assert response.status_code == 200
        response = requests.delete(url=bear + '/' + test_bear)
        assert response.status_code == 200
        response = requests.get(bear)
        assert response.status_code == 200
        assert response.json() == [test_answ[2]]

    def test_wrong_endpoint(self, info):
        response = requests.delete(info)
        assert response.status_code == 404
