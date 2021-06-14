import requests

test_bears = [{"bear_type":"POLAR","bear_name":"UMKA","bear_age":1}, {"bear_type":"GUMMY","bear_name":"VINNIE","bear_age":13},
                {"bear_type":"BROWN","bear_name":"MEDVED","bear_age":15}, {"bear_type":"BLACK","bear_name":"GRIZZLY","bear_age":71}]
test_answ = [{"bear_id":1, "bear_type":"POLAR","bear_name":"UMKA","bear_age":1.0}, {"bear_id":2, "bear_type":"GUMMY","bear_name":"VINNIE","bear_age":13.0},
                {"bear_id":3, "bear_type":"BROWN","bear_name":"MEDVED","bear_age":15.0}, {"bear_id":4, "bear_type":"BLACK","bear_name":"GRIZZLY","bear_age":71.0}]

class TestGetRequests(object):
    def test_info_answer(self, info):
        response = requests.get(info)
        assert response.status_code == 200

    def test_empty_list(self, bear):
        response = requests.get(bear)
        assert response.status_code == 200
        assert response.json() == []

    def test_bears_list(self, bear):
        response = requests.post(url=bear, json=test_bears[0])
        assert response.status_code == 200
        response = requests.post(url=bear, json=test_bears[1])
        assert response.status_code == 200
        response = requests.post(url=bear, json=test_bears[2])
        assert response.status_code == 200
        response = requests.post(url=bear, json=test_bears[3])
        assert response.status_code == 200
        response = requests.get(url=bear)
        assert response.json() == test_answ

    def test_bear_read(self, bear):
        response = requests.post(url=bear, json=test_bears[0])
        assert response.status_code == 200
        response = requests.get(url=bear + '/' + response.text)
        assert response.json() == test_answ[0]

    def test_empty_bear_read(self, bear):
        response = requests.post(url=bear, json=test_bears[0])
        assert response.status_code == 200
        response = requests.get(url=bear + '/14')
        assert response.status_code == 200
        assert response.text == 'EMPTY'

    def test_deleted_bear_read(self, bear):
        response = requests.post(url=bear, json=test_bears[0])
        assert response.status_code == 200
        created_bear = response.text
        response = requests.delete(url=bear + '/' + created_bear)
        assert response.status_code == 200
        response = requests.get(url=bear + '/' + created_bear)
        assert response.status_code == 200
        assert response.text == 'EMPTY'

    def test_wrong_endpoint(self, bear):
        response = requests.get(bear + 's')
        assert response.status_code == 404