from geojson import from_topo
from json import load,dump

def convert(topojson,input_name=None,geojson=None):
    if isinstance(topojson,dict):
        parsed_geojson = topojson
    elif isinstance(topojson,str) or isinstance(topojson,unicode):
        in_file = open(topojson)
        parsed_geojson = load(in_file)
        in_file.close()
    elif isinstance(topojson,file):
        parsed_geojson=load(topojson)
    if input_name is None:
            input_name = parsed_geojson['objects'].keys()[0]
    out = from_topo(parsed_geojson,input_name)
    if isinstance(geojson,str) or isinstance(geojson,unicode):
        with open(geojson,'w') as f:
            dump(out,f)
    elif isinstance(geojson,file):
        dump(out,geojson)
    else:
        return out