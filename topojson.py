from types import types
from stitchpoles import stitch
from hashtable import hashtable
from coordinatesystems import systems

e = 1e-6
def isInfinit(n):
	return abs(n)==float('inf')

def topology (objects, options=False):
	Q = 1e4; # precision of quantization
	id = lambda d:d['id']
	def propertyTransform ():
		pass
	stitchPoles = True;
	verbose = False;
	emax = 0
	system = False
	arcs = []
	x0=y0=x1=y1=kx=ky=False
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

	coincidences = hashtable(Q * 10);
	arcsByPoint = hashtable(Q * 10);
	pointsByPoint = hashtable(Q * 10);

	def each(t):
		out = {}
		for key in objects:
			out[key] = t.object(objects[key])
			if not out[key]:
				out[key]={}
		return out

	def bound():
		[x0,x1]=[y0,y1]=[float('inf'),-float('inf')]
		class boundit(types):
			def point (self,point):
				x = point[0]
				y = point[1]
				if x < x0:
					x0 = x;
				if x > x1:
					x1 = x;
				if y < y0:
					y0 = y;
				if y > y1:
					y1 = y;
		each(boundit)
	bound()
	
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
			bound()
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
	if Q:
		kx = (Q - 1) / (x1 - x0) if x1 - x0 else 1
		ky = (Q - 1) / (y1 - y0) if y1 - y0 else 1;
	else:
		print("quantization: disabled; assuming inputs already quantized")
		Q = x1 + 1;
		kx = ky = 1;
		x0 = y0 = 0;
	if verbose:
		qx0 = round((x0 - x0) * kx) * (1 / kx) + x0
		qx1 = round((x1 - x0) * kx) * (1 / kx) + x0
		qy0 = round((y0 - y0) * ky) * (1 / ky) + y0
		qy1 = round((y1 - y0) * ky) * (1 / ky) + y0
		print("quantization: bounds " + str(qx0)+str(qy0)+str(qx1)+str(qy1) + " (" + system.name + ")")
	class newPointFunc(types):
		def point(self,point):
			x1 = point[0]
			y1 = point[1]
			x = round((x1 - x0) * kx)
			y = round((y1 - y0) * ky)
			ee = system.distance(x1, y1, x / kx + x0, y / ky + y0)
			if ee > emax:
				emax = ee
			point[0] = x
			point[1] = y

	each(newPointFunc)
	class newLineFunc(types):
		def line(line):
			i = 0
			n = len(line)
			while i < n:
				lines = coincidences.get(line[i])
				if not line in lines:
					lines.append(line)
				i+=0
	each(newLineFunc)

	#Convert features to geometries, and stitch together arcs.
	class bigEach(types):
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
			del collection.features
			return collection
		def GeometryCollection(self,collection):
			collection['geometries'] = map(self.geometry,collection['geometries'])
		def MultiPolygon(self,multiPolygon):
			multiPolygon['arcs'] = map(polygon,multiPolygon['coordinates'])
		def Polygon(self,polygon):
			 polygon['arcs'] = map(lineClosed,polygon['coordinates'])
		def MultiLineString(self,multiLineString):
			multiLineString['arcs'] = map(lineOpen,multiLineString['coordinates'])
		def LineString(self,lineString):
			lineString['arcs'] = lineOpen(lineString['coordinates'])
		def geometry(self,geometry):
			if geometry == None:
				geometry = {};
			else:
				super(types,self).geometry(geometry)
			geometry['id'] = id(geometry)
			if geometry['id'] == None:
				del geometry['id']
			properties0 = geometry.properties
			if properties0:
				properties1 = {}
				del geometry['properties']
				for key0 in properties0:
					if propertyTransform(properties1, key0, properties0[key0]):
						geometry['properties'] = properties1
			if geometry.has_key('arcs'):
				del geometry['coordinates']
			return geometry;
	objects = each(bigEach)

	coincidences = arcsByPoint = pointsByPoint = None

	polygon = lambda poly:map(lineClosed,poly)
	lineClosed = lambda points:line(points,False)
	lineOpen = lambda points:line(points,True)
	def line(points, open):
		lineArcs = [];
		n = len(points)
		a = []
		k = -1
		p=False
		if not open:
			points.pop()
			n-=1
		while k<n:
			k+=1
			t = coincidences['peek'](points[k])
			if open:
				break
			if p and not linesEqual(p, t):
				tInP = all(map(lambda line: line in p,t))
				pInT = all(map(lambda line: line in t,p))
				if tInP and not pInT:
					k-=1
				break;
			p = t;
		# If no shared starting point is found for closed lines, rotate to minimum.
		if k == n and len(p) > 1:
			point0 = points[0]
			i = -1
			k=0
			while i<n:
				i+=1
				point = points[i];
				if pointCompare(point0, point) > 0:
					point0 = point
					k = i
		i = -1
		m = n if open else n + 1
		while i < m:
			i+=1
			point = points[(i + k) % n]
			p = coincidences['peek'](point)
			if  not linesEqual(p, t):
				tInP = all(map(lambda line: line in p,t))
				pInT = all(map(lambda line: line in t,p))
				if tInP:
					a.append(point);
				arc(a)
				if not tInP and not pInT:
					arc([a[-1], point])
				if pInT:
					a = [a[-1]]
				else:
					a = [];
			if not len(a) or pointCompare(a[-1], point):
				a.append(point) # skip duplicate points
			t = p
		arc(a, True)
		def arc(a, last):
			n = len(a)
			point=False
			if last and not len(lineArcs) and n == 1:
				point = a[0]
				index = pointsByPoint['get'](point)
				if len(index):
					lineArcs.append(index[0])
				else:
					index[0] = len(arcs)
					lineArcs.append(index[0])
					arcs.append(a)
			elif n > 1:
				a0 = a[0]
				a1 = a[-1]
				point = a0 if pointCompare(a0, a1) < 0 else a1
				pointArcs = arcsByPoint['get'](point)
				if any(map(matchForward,pointArcs)) or any(map(matchBackward,pointArcs)):
					return
				pointArcs.append(a)
				a['index']=len(arcs)
				lineArcs.append(a['index'])
				arcs.append(a)
		def matchForward(b):
			i = 0;
			if len(b) != n:
				return False
			while i < n:
				if pointCompare(a[i], b[i]):
					return False;
				i+=1
			lineArcs.append(b['index'])
			return True;

		def matchBackward(b):
			i = 0
			if len(b) != n:
				return False
			while i<n:
				if pointCompare(a[i], b[n - i - 1]):
					return False
				i+=1
			lineArcs.append(~b['index'])
			return True
		return lineArcs
	def mapFunc (arc):
		i = 1;
		n = len(arc)
		point = arc[0]
		x1 = point[0]
		x2= dx =y2 = dy=False
		y1 = point[1]
		points = [[x1, y1]]
		while i < n:
			point = arc[i]
			x2 = point[0]
			y2 = point[1]
			dx = x2 - x1
			dy = y2 - y1
			if dx or dy:
				points.append([dx, dy])
				x1 = x2
				y1 = y2
			i+=1
		return points
	return {
		'type': "Topology",
		'bbox': [x0, y0, x1, y1],
		'transform': {
			'scale': [1 / kx, 1 / ky],
			'translate': [x0, y0]
		},
		'objects': objects,
		'arcs': map(mapFunc,arcs)
	}


def linesEqual(a, b):
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
	return a[0] - b[0] or a[1] - b[1]
