import json
import pytest
from os import path
import requests as rq
from .utils import validate_json

test_dir = path.join(path.dirname(__file__), 'data')


@pytest.fixture(scope='class')
def tpscheme(request):
    url = 'https://raw.githubusercontent.com/calvinmetcalf/topojson.py/v1.1.x/test_objects/schema/topojson.json'
    request.cls.tpscheme = rq.get(url).json()


@pytest.fixture(scope='function')
def square():
    with open(path.join(test_dir, 'square.geojson')) as f:
            square = json.load(f)

    return square


@pytest.mark.usefixtures("tpscheme")
class TestTopojson(object):

    def test_convert_geojson_to_topojson(self, square):
        from topojson.conversion import convert

        tj = convert(square)
        print(tj)
        assert tj['type'] == 'Topology'
        assert validate_json(tj, self.tpscheme)
