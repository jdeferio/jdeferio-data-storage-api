
import unittest
import json
import webtest
import server

class DataStorageServerTest(unittest.TestCase):

    def setUp(self):
        app = server.DataStorageServer()
        self.testapp = webtest.TestApp(app)

    def test_get_not_found(self):
        resp = self.testapp.get("/data/foo/noooope", expect_errors=True)
        self.assertEqual(404, resp.status_code)

    def test_put(self):
        resp = self.testapp.put("/data/foo", "some object")
        res = json.loads(resp.body)

        self.assertEqual(201, resp.status_code)
        self.assertEqual(11, res["size"])
        self.assertEqual(type(res["oid"]), str)
        self.assertTrue(len(res["oid"]) > 0)

    def test_get(self):
        resp = self.testapp.put("/data/foo", "some object")
        res1 = json.loads(resp.body)

        resp = self.testapp.put("/data/foo", "other object")
        res2 = json.loads(resp.body)

        self.assertNotEqual(res1["oid"], res2["oid"])

        resp = self.testapp.get(f"/data/foo/{res1['oid']}")
        self.assertEqual(b"some object", resp.body)

        resp = self.testapp.get(f"/data/foo/{res2['oid']}")
        self.assertEqual(b"other object", resp.body)

    def test_delete(self):
        resp = self.testapp.put("/data/foo", "some object")
        res = json.loads(resp.body)

        resp = self.testapp.delete(f"/data/foo/{res['oid']}")
        self.assertEqual(200, resp.status_code)

        resp = self.testapp.get(f"/data/foo/{res['oid']}", expect_errors=True)
        self.assertEqual(404, resp.status_code)

    def test_delete_nonexistant_object(self):
        resp = self.testapp.delete("/data/foo/nooope", expect_errors=True)
        self.assertEqual(404, resp.status_code)

if __name__ == '__main__':
    unittest.main()
