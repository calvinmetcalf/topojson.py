TYPEGEOMETRIES = (
    'LineString',
    'MultiLineString',
    'MultiPoint',
    'MultiPolygon',
    'Point',
    'Polygon',
    'GeometryCollection'
)


class Transformer:
    def __init__(self,transform,arcs):
        self.scale = transform['scale']
        self.translate = transform['translate']
        self.arcs = list(map(self.convert_arc,arcs))
    def convert_arc(self,arc):
        out_arc = []
        previous=[0,0]
        for point in arc:
            previous[0]+=point[0]
            previous[1]+=point[1]
            out_arc.append(self.convert_point(previous))
        return out_arc
    def reversed_arc(self,arc):
        return list(map(None,reversed(self.arcs[~arc])))
    def stitch_arcs(self,arcs):
        line_string = []
        for arc in arcs:
            if arc<0:
                line = self.reversed_arc(arc)
            else:
                line = self.arcs[arc]
            if len(line_string)>0:
                if line_string[-1] == line[0]:
                    line_string.extend(line[1:])
                else:
                    line_string.extend(line)
            else:
                line_string.extend(line)
        return line_string
    def stich_multi_arcs(self,arcs):
        return list(map(self.stitch_arcs,arcs))
    def convert_point(self,point):
        return [point[0]*self.scale[0]+self.translate[0],point[1]*self.scale[1]+self.translate[1]]
    def feature(self,feature):
        out={'type':'Feature'}
        out['geometry']={'type':feature['type']}
        if feature['type'] in ('Point','MultiPoint'):
            out['geometry']['coordinates'] = feature['coordinates']
        elif feature['type'] in ('LineString','MultiLineString','MultiPolygon','Polygon'):
            out['geometry']['arcs'] = feature['arcs']
        elif feature['type'] == 'GeometryCollection':
            out['geometry']['geometries'] = feature['geometries']
        for key in ('properties','bbox','id'):
            if key in feature:
                out[key] = feature[key]
        out['geometry']=self.geometry(out['geometry'])
        return out
    def geometry(self,geometry):
        if geometry['type']=='Point':
            return self.point(geometry)
        elif geometry['type']=='MultiPoint':
            return self.multi_point(geometry)
        elif geometry['type']=='LineString':
            return self.line_string(geometry)
        elif geometry['type']=='MultiLineString':
            return self.multi_line_string_poly(geometry)
        elif geometry['type']=='Polygon':
            return self.multi_line_string_poly(geometry)
        elif geometry['type']=='MultiPolygon':
            return self.multi_poly(geometry)
        elif geometry['type']=='GeometryCollection':
            return self.geometry_collection(geometry)
    def point(self,geometry):
        geometry['coordinates']=self.convert_point(geometry[coordinates])
        return geometry
    def multi_point(self,geometry):
        geometry['coordinates']= list(map(self.convert_point,geometry[coordinates]))
        return  geometry
    def line_string(self,geometry):
        geometry['coordinates']=self.stitch_arcs(geometry['arcs'])
        del geometry['arcs']
        return geometry
    def multi_line_string_poly(self,geometry):
        geometry['coordinates']=self.stich_multi_arcs(geometry['arcs'])
        del geometry['arcs']
        return geometry
    def multi_poly(self,geometry):
        geometry['coordinates']= list(map(self.stich_multi_arcs,geometry['arcs']))
        del geometry['arcs']
        return geometry
    def geometry_collection(self,geometry):
        out = {'type':'FeatureCollection'}
        out['features']= list(map(self.feature,geometry['geometries']))
        return out
def from_topo(topo,obj_name):
    if obj_name in topo['objects']:
        geojson = topo['objects'][obj_name]
    else:
        raise Exception(u"Something ain't right")
    transformer = Transformer(topo['transform'],topo['arcs'])
    if geojson['type'] in TYPEGEOMETRIES:
        geojson = transformer.geometry(geojson)
    return geojson
