
typeGeometries = (
  'LineString',
  'MultiLineString',
  'MultiPoint',
  'MultiPolygon',
  'Point',
  'Polygon',
  'GeometryCollection'
)

class types:
	def Feature(self,feature):
		if feature.has_key('geometry'):
			self.geometry(feature['geometry'])
	def FeatureCollection(self,collection):
		for feature in collection['features']:
			self.Feature(feature)
	def GeometryCollection(self,collection):
		if collection.has_key('geometries'):
			for geometry in collection['geometries']:
				self.geometry(geometry)
	def LineString(self,lineString):
		self.line(lineString['coordinates'])
	def MultiLineString(self,multiLineString):
		for coordinate in multiLineString['coordinates']:
			self.line(coordinate)
	def MultiPoint(self,multiPoint):
		for coordinate in multiPoint['coordinates']:
			self.point(coordinate);
	def MultiPolygon(self,multiPolygon):
		for coordinate in multiPolygon['coordinates']:
			self.polygon(coordinate);
	def Point(self,point):
		self.point(point['coordinates'])
	def Polygon(self,polygon):
		self.polygon(polygon['coordinates'])
	def obj(self,obj):
		if obj == None :
			return None
		elif obj['type']=='Feature':
			return self.Feature(obj)
		elif obj['type']=='FeatureCollection':
			return self.FeatureCollection(obj)
		else:
			return self.geometry(obj)
	def geometry(self,geometry):
		if not (geometry != None and geometry['type'] in typeGeometries):
			return None
		elif geometry['type']== 'LineString':
			return self.LineString(geometry)
		elif geometry['type']== 'MultiLineString':
			return self.MultiLineString(geometry)
		elif geometry['type']== 'MultiPoint':
			return self.MultiPoint(geometry)
		elif geometry['type']== 'Point':
			return self.Point(geometry)
		elif geometry['type']== 'Polygon':
			return self.Polygon(geometry)
		elif geometry['type']== 'GeometryCollection':
			return self.GeometryCollection(geometry)
	def point(self):
		pass
	def line(self,coordinates):
		for coordinate in coordinates:
			self.point(coordinate)
	def polygon(self,coordinates):
		for coordinate in coordinates:
			self.line(coordinate)
