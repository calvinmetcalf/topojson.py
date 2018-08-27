import json
import pytest
from os import path
import requests as rq
from .utils import validate_json
from glob import glob

test_dir = path.join(path.dirname(__file__), "data")


@pytest.fixture(scope="class")
def tpscheme(request):
    url = "https://raw.githubusercontent.com/calvinmetcalf/topojson.py/v1.1.x/test_objects/schema/topojson.json"
    request.cls.tpscheme = rq.get(url).json()


objs = {
    "square": {"type": "Topology", "bbox_length": 4, "geometries": 1},
    "square_with_hole": {"type": "Topology", "bbox_length": 4, "geometries": 1},
    "two_squares": {"type": "Topology", "bbox_length": 4, "geometries": 2},
}


@pytest.mark.usefixtures("tpscheme")
class TestTopojson(object):

    @pytest.mark.parametrize("type, props", objs.items())
    def test_convert_geojson_to_topojson(self, type, props):
        from topojson.conversion import convert

        with open(path.join(test_dir, f'{type}.geojson'), 'r') as f:
            obj = json.load(f)

        tj = convert(obj)

        # check vs schema
        validate_json(tj, self.tpscheme)

        assert tj["type"] == props['type']
        assert len(tj["bbox"]) == props['bbox_length']
        assert len(tj["objects"]["name"]["geometries"]) == props['geometries']
