import unittest
from app import create_app
from app.main.utils import build_query, parse_response, parse_satellite
import datetime


class MockResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_build_query(self):
        satellite_id = "000000"
        (query, headers) = build_query(satellite_id)
        self.assertEqual(query, "https://tle.ivanstanojevic.me/api/tle/000000")
        self.assertTrue("User-Agent" in headers)

    def test_parse_response_success(self):
        mock_resp = MockResponse(200, {
            "satelliteId": 25544,
            "name": "ISS (ZARYA)",
            "line1": "1 25544U",
            "line2": "2 25544",
            "date": "2026-06-07T21:37:51+00:00"
        })
        result = parse_response(mock_resp)
        self.assertEqual(result["satellite_name"], "ISS (ZARYA)")
        self.assertEqual(result["date"], "2026-06-07T21:37:51+00:00")

    def test_parse_response_failure(self):
        mock_resp = MockResponse(404, None)
        result = parse_response(mock_resp)
        self.assertIsNone(result)

    def test_parse_satellite(self):
        tle_dict = {
            "line1": "1 25544U 98067A   26158.90128687  .00007994  00000+0  14961-3 0  9995",
            "line2": "2 25544  51.6338 346.0598 0006926 145.2709 214.8733 15.49660544570312"
        }
        dt = datetime.datetime(2026, 6, 1, 12, 0)
        error, r, v = parse_satellite(tle_dict, dt)
        self.assertEqual(error, 0)
        self.assertIsNotNone(r)
        self.assertIsNotNone(v)