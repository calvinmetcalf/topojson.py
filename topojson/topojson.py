# coding=utf8
from mytypes import types
from stitchpoles import stitch
from coordinatesystems import systems
from bounds import bound
from line import Line
from clockwise import clock
from decimal import Decimal

e = 1e-6
def isInfinit(n):
	return abs(n)==float('inf')

def topology (objects, options=False):
	Q = 1e4; # precision of quantization
	id = lambda d:d['id']
	def propertyTransform (outprop, key, inprop):
		outprop[key]=inprop
		return True
	stitchPoles = True
	verbose = False
	emax = 0
	system = False
	objectName = 'name'
	if type(options)==type({}):
		if options.has_key('verbose'):
			verbose = not not options['verbose']
		if options.has_key('stitch-poles'):
			stitchPoles = not not options["stitch-poles"]
		if options.has_key('coordinate-system'):
			system = systems[options["coordinate-system"]]
		if options.has_key('quantization'):
			Q = float(options["quantization"])
		if options.has_key('id'):
			id = options['id']
		if options.has_key('property-transform'):
			propertyTransform = options["property-transform"]
		if options.has_key('name'):
			objectName = options['name']

	ln = Line(Q)
	
	
	[x0,x1,y0,y1]=bound(objects)
	
	oversize = x0 < -180 - e or x1 > 180 + e or y0 < -90 - e or y1 > 90 + e
	if not system:
		if oversize:
			system = systems["cartesian"]
		else:
			system = systems["spherical"]
		if type(options)==type({}):
			options["coordinate-system"] = system['name']
	if system == systems['spherical']:
		if oversize:
			raise Exception(u"spherical coordinates outside of [±180°, ±90°]")
		if stitchPoles:
			stitch(objects)
			[x0,x1,y0,y1]=bound(objects)
		if x0 < -180 + e:
			x0 = -180
		if x1 > 180 - e:
			x1 = 180
		if y0 < -90 + e:
			y0 = -90
		if y1 > 90 - e:
			y1 = 90;
	if isInfinit(x0):
		x0 = 0
	if isInfinit(x1):
		x1 = 0;

	if isInfinit(y0):
		y0 = 0;
	if isInfinit(y1):
		y1 = 0;
	[kx,ky]=makeKs(Q,x0,x1,y0,y1)
	if not Q:
		Q = x1 + 1
		x0 = y0 = 0
	class findEmax(types):
		def __init__(self,obj):
			self.emax=0
			self.obj(obj)
		def point(self,point):
			x1 = point[0]
			y1 = point[1]
			x = ((x1 - x0) * kx)
			y =((y1 - y0) * ky)
			ee = system['distance'](x1, y1, x / kx + x0, y / ky + y0)
			if ee > self.emax:
				self.emax = ee
			point[0] = int(x)
			point[1] = int(y)
	finde=findEmax(objects)
	emax = finde.emax
	clock(objects,system['ringArea'])
	class findCoincidences(types):
		def line(self,line):
			for point in line:
				lines = ln.coincidences.get(point)
				if not line in lines:
					lines.append(line)
	fcInst = findCoincidences(objects)
	polygon = lambda poly:map(ln.lineClosed,poly)
	#Convert features to geometries, and stitch together arcs.
	class makeTopo(types):
		def Feature (self,feature):
			geometry = feature["geometry"]
			if feature['geometry'] == None:
				geometry = {};
			if feature.has_key('id'):
				geometry['id'] = feature['id']
			if feature.has_key('properties'):
				geometry['properties'] = feature['properties']
			return self.geometry(geometry);
		def FeatureCollection(self,collection):
			collection['type'] = "GeometryCollection";
			collection['geometries'] = map(self.Feature,collection['features'])
			del collection['features']
			return collection
		def GeometryCollection(self,collection):
			collection['geometries'] = map(self.geometry,collection['geometries'])
		def MultiPolygon(self,multiPolygon):
			multiPolygon['arcs'] = map(polygon,multiPolygon['coordinates'])
		def Polygon(self,polygon):
			 polygon['arcs'] = map(ln.lineClosed,polygon['coordinates'])
		def MultiLineString(self,multiLineString):
			multiLineString['arcs'] = map(ln.lineOpen,multiLineString['coordinates'])
		def LineString(self,lineString):
			lineString['arcs'] = ln.lineOpen(lineString['coordinates'])
		def geometry(self,geometry):
			if geometry == None:
				geometry = {};
			else:
				types.geometry(self,geometry)
			geometry['id'] = id(geometry)
			if geometry['id'] == None:
				del geometry['id']
			properties0 = geometry['properties']
			if properties0:
				properties1 = {}
				del geometry['properties']
				for key0 in properties0:
					if propertyTransform(properties1, key0, properties0[key0]):
						geometry['properties'] = properties1
			if geometry.has_key('arcs'):
				del geometry['coordinates']
			return geometry;
	makeTopoInst = makeTopo(objects)
	return {
		'type': "Topology",
		'bbox': [x0, y0, x1, y1],
		'transform': {
			'scale': [1.0 / kx, 1.0 / ky],
			'translate': [x0, y0]
		},
		'objects': {objectName:makeTopoInst.outObj},
		'arcs': ln.getArcs()
	}

def makeKs(Q,x0,x1,y0,y1):
	[x,y]=[1,1]
	if Q:
		if x1 - x0:
			x= (Q - 1.0) / (x1 - x0)
		if y1 - y0:
			y=(Q - 1.0) / (y1 - y0)
	return [x,y]
def linesEqual(a, b):
	if not(type(a)==type(b)==type([])):
		return True
	n = len(a);
	i = 0
	if len(b) != n:
		return False
	while i < n:
		if a[i] != b[i]:
			return False;
		i+=1
	return True;

def pointCompare(a, b):
	if isPoint(a) and isPoint(b):
		return a[0] - b[0] or a[1] - b[1]

isPoint = lambda x : type(x)==type([]) and len(x)==2
