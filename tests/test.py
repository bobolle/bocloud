import unittest
import requests

class TestBoCloud(unittest.TestCase):

    def test_get(self):
        r = requests.get('http://localhost:9090')
        self.assertEqual(r.status_code, 200)

    def test_post(self):
        r = requests.post('http://localhost:9090/api/data', data='{"device_id": "test", "sensor_type": "test", "value": 200}')
        self.assertEqual(r.status_code, 201)

if __name__ == '__main__':
    unittest.main()
