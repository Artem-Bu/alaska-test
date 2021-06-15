import requests
from copy import deepcopy

test_bears = [{"bear_type":"POLAR","bear_name":"UMKA","bear_age":3}, {"bear_type":"GUMMY","bear_name":"VINNIE","bear_age":13},
                {"bear_type":"BROWN","bear_name":"MEDVED","bear_age":55}, {"bear_type":"BLACK","bear_name":"GRIZZLY","bear_age":11}]
test_answ = [{"bear_id":1, "bear_type":"POLAR","bear_name":"UMKA","bear_age":3.0}, {"bear_id":2, "bear_type":"GUMMY","bear_name":"VINNIE","bear_age":13.0},
                {"bear_id":3, "bear_type":"BROWN","bear_name":"MEDVED","bear_age":55.0}, {"bear_id":4, "bear_type":"BLACK","bear_name":"GRIZZLY","bear_age":11.0}]

class TestPostRequests(object):
    def test_bear_type(self, bear):
        for index, test_bear in enumerate(test_bears, start=0):
            response = requests.post(url=bear, json=test_bear)
            assert response.status_code == 200
            response = requests.get(url=bear + '/' + response.text)
            assert response.json() == test_answ[index]

    def test_wrong_type(self, bear):
        test_bear = deepcopy(test_bears[0])
        test_bear["bear_type"] = "GROLAR"
        response = requests.post(url=bear, json=test_bear)
        assert response.status_code == 500
        test_bear["bear_type"] = "UNKNOWN"
        response = requests.post(url=bear, json=test_bear)
        assert response.status_code == 500

    def test_bear_age(self, bear):
        test_bear = deepcopy(test_bears[0])
        test_bear["bear_age"] = -12
        response = requests.post(url=bear, json=test_bear)
        assert response.status_code == 400

        test_bear["bear_age"] = 101
        response = requests.post(url=bear, json=test_bear)
        assert response.status_code == 400

    def test_bear_names(self, bear):
        renamed_test_bears = deepcopy(test_bears)
        renamed_test_answ = deepcopy(test_answ)
        renamed_test_bears[0]["bear_name"] = renamed_test_answ[0]["bear_name"] = '!?%$#__'
        renamed_test_bears[1]["bear_name"] = renamed_test_answ[1]["bear_name"] = 'B\^^E^&%A+R'
        renamed_test_bears[1]["bear_type"] = renamed_test_answ[1]["bear_type"] = 'POLAR'
        renamed_test_bears[2]["bear_name"] = renamed_test_answ[2]["bear_name"] = '1234'
        renamed_test_bears[3]["bear_name"] = renamed_test_answ[3]["bear_name"] = 'MEDВЕДЬ'
        for index, test_bear in enumerate(renamed_test_bears, start=0):
            response = requests.post(url=bear, json=test_bear)
            assert response.status_code == 200
            response = requests.get(url=bear + '/' + response.text)
            assert response.json() == renamed_test_answ[index]

    def test_create_bear_with_id(self, bear):
        test_bear = deepcopy(test_bears[0])
        test_bear["bear_id"] = 777
        response = requests.post(url=bear, json=test_bear)
        assert response.status_code == 200
        bear_id = response.text
        response = requests.get(url=bear + '/777')
        assert response.status_code == 200
        assert response.text == 'EMPTY'
        response = requests.get(url=bear + '/' + bear_id)
        assert response.json() == test_answ[0]

    def test_empty_attr(self, bear):
        empty_test_bears = deepcopy(test_bears)
        empty_test_bears[0]["bear_age"] = ''
        empty_test_bears[1]["bear_age"] = ''
        empty_test_bears[2]["bear_age"] = ''
        empty_test_bears[2]["bear_type"] = ''
        empty_test_bears[3]["bear_type"] = ''

        for test_bear in empty_test_bears:
            response = requests.post(url=bear, json=test_bear)
            assert response.status_code == 500
