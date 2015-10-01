# coding=utf8
from __future__ import division
from .mytypes import Types
from .stitchpoles import stitch
from .coordinatesystems import systems
from .bounds import bound
from .line import Line
from .clockwise import Clock
from decimal import Decimal
from .simplify import simplify_object
from .utils import is_infinit,E
def property_transform (outprop, key, inprop):
        outprop[key]=inprop
        return True
def topology (objects, stitchPoles=True,quantization=1e4,id_key='id',property_transform=property_transform,system = False,simplify=False):
    ln = Line(quantization)
    id_func = lambda x:x.get(id_key, None)
    if simplify:
        objects = simplify_object(objects,simplify)
    [x0,x1,y0,y1]=bound(objects)
    
    oversize = x0 < -180 - E or x1 > 180 + E or y0 < -90 - E or y1 > 90 + E
    if not system:
        if oversize:
            system =systems["cartesian"]
        else:
            system = systems["spherical"]
    if system.name == 'spherical':
        if oversize:
            raise Exception(u"spherical coordinates outside of [±180°, ±90°]")
        if stitchPoles:
            stitch(objects)
            [x0,x1,y0,y1] = bound(objects)
        if x0 < -180 + E:
            x0 = -180
        if x1 > 180 - E:
            x1 = 180
        if y0 < -90 + E:
            y0 = -90
        if y1 > 90 - E:
            y1 = 90
    if is_infinit(x0):
        x0 = 0
    if is_infinit(x1):
        x1 = 0

    if is_infinit(y0):
        y0 = 0
    if is_infinit(y1):
        y1 = 0
    [kx,ky]=make_ks(quantization,x0,x1,y0,y1)
    if not quantization:
        quantization = x1 + 1
        x0 = y0 = 0
        
    class findEmax(Types):
        def __init__(self,obj):
            self.emax=0
            self.obj(obj)
        def point(self,point):
            x1 = point[0]
            y1 = point[1]
            x = ((x1 - x0) * kx)
            y =((y1 - y0) * ky)
            ee = system.distance(x1, y1, x / kx + x0, y / ky + y0)
            if ee > self.emax:
                self.emax = ee
            point[0] = int(x)
            point[1] = int(y)
    finde=findEmax(objects)
    emax = finde.emax
    # Clock(objects,system.ring_area)
    class find_coincidences(Types):
        def line(self,line):
            for point in line:
                lines = ln.arcs.coincidence_lines(point)
                if not line in lines:
                    lines.append(line)
    fcInst = find_coincidences(objects)
    polygon = lambda poly:list(map(ln.line_closed,poly))
    #Convert features to geometries, and stitch together arcs.
    class make_topo(Types):
        def Feature (self,feature):
            geometry = feature["geometry"]
            if feature['geometry'] == None:
                geometry = {}
            if 'id' in feature:
                geometry['id'] = feature['id']
            if 'properties' in feature:
                geometry['properties'] = feature['properties']
            return self.geometry(geometry)
        def FeatureCollection(self,collection):
            collection['type'] = "GeometryCollection"
            collection['geometries'] = list(map(self.Feature,collection['features']))
            del collection['features']
            return collection
        def GeometryCollection(self,collection):
            collection['geometries'] = list(map(self.geometry,collection['geometries']))
        def MultiPolygon(self,multiPolygon):
            multiPolygon['arcs'] = list(map(polygon,multiPolygon['coordinates']))
        def Polygon(self,polygon):
             polygon['arcs'] = list(map(ln.line_closed,polygon['coordinates']))
        def MultiLineString(self,multiLineString):
            multiLineString['arcs'] = list(map(ln.line_open,multiLineString['coordinates']))
        def LineString(self,lineString):
            lineString['arcs'] = ln.line_open(lineString['coordinates'])
        def geometry(self,geometry):
            if geometry == None:
                geometry = {}
            else:
                Types.geometry(self,geometry)
            geometry['id'] = id_func(geometry)
            if geometry['id'] == None:
                del geometry['id']
            properties0 = geometry['properties']
            if properties0:
                properties1 = {}
                del geometry['properties']
                for key0 in properties0:
                    if property_transform(properties1, key0, properties0[key0]):
                        geometry['properties'] = properties1
            if 'arcs' in geometry:
                del geometry['coordinates']
            return geometry
    make_topo_inst = make_topo(objects)
    return {
        'type': "Topology",
        'bbox': [x0, y0, x1, y1],
        'transform': {
            'scale': [1.0 / kx, 1.0 / ky],
            'translate': [x0, y0]
        },
        'objects': make_topo_inst.outObj,
        'arcs': ln.get_arcs()
    }

def make_ks(quantization,x0,x1,y0,y1):
    [x,y]=[1,1]
    if quantization:
        if x1 - x0:
            x= (quantization - 1.0) / (x1 - x0)
        if y1 - y0:
            y=(quantization - 1.0) / (y1 - y0)
    return [x,y]
