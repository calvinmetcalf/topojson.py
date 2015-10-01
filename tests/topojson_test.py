import json
import unittest

from topojson.conversion import convert


class TestTopojson(unittest.TestCase):

    def setUp(self):
        with open("tests/data/square.geojson") as f:
            self.square_geojson = json.load(f)

    def test_convert_geojson_to_topojson(self):
        tj = convert(self.square_geojson)
        self.assertEqual(tj['type'], 'Topology')
