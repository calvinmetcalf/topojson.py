import json
import pytest
from os import path
import jsonschema
import requests as rq

test_dir = path.join(path.dirname(__file__), 'data')


@pytest.fixture(scope='class')
def tpscheme(request):
    url = 'https://raw.githubusercontent.com/nhuebel/TopoJSON_schema/master/topojson.json'
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

        assert tj['type'] == 'Topology'
        assert jsonschema.validate(tj, self.tpscheme), tj
