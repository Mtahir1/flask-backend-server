import imp
from tkinter import SEL
from urllib import response


try:
    import requests
    import unittest
except Exception as e:
    print("Some modules are missing {}".format(e))

class TestAPI(unittest.TestCase):
    URL = "https://kodex-ai-app.herokuapp.com/"
    # check if Response is 200
    def test_index(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()),1)
        print("Test 1 completed")

if __name__ == "__main__":
    tester = TestAPI()
    tester.test_index()