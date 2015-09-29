import json
import unittest

from topojson.conversion import convert

class TestTopojson(unittest.TestCase):

    GeoJSON = json.loads("""
        {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-10, 10],
                            [ 10, 10],
                            [ 10, -10],
                            [-10, -10],
                            [-10, 10]
                        ]]
                    }
                }
            ]
        }
    """)

    def setUp(self):
        pass

    def test_topojson(self):
        tj = convert(self.GeoJSON)
        self.assertEqual(tj['type'], 'Topology')
        # with open('/tmp/out.topojson', 'w') as f:
            # json.dump(tj, f)
