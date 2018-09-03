from json import load, dump
import os
import io

from .topology import topology


def convert(geojson, topojson=None, object_name=False, *args, **kwargs):
    if isinstance(geojson, dict):
        input_dict = geojson

    elif isinstance(geojson, str):
        assert os.path.exists(geojson)

        with open(geojson) as f:
            input_dict = load(f)

        if not object_name and "type" in input_dict and geojson.endswith(".geojson"):
            input_dict = {geojson[:-8].split("/")[-1]: input_dict}

    elif isinstance(geojson, io.TextIOWrapper):
        input_dict = load(geojson)

    if "type" in input_dict:
        if object_name:
            input_dict = {object_name: input_dict}
        else:
            input_dict = {"name": input_dict}
    output_dict = topology(input_dict, *args, **kwargs)
    if isinstance(topojson, str) or isinstance(topojson, str):
        with open(topojson, "w") as f:
            dump(output_dict, f)
    elif isinstance(topojson, io.TextIOWrapper):
        dump(output_dict, topojson)
    else:
        return output_dict
