var typeGeometries = {
  LineString: 1,
  MultiLineString: 1,
  MultiPoint: 1,
  MultiPolygon: 1,
  Point: 1,
  Polygon: 1,
  GeometryCollection: 1
};

var typeObjects = {
  Feature: 1,
  FeatureCollection: 1
};

var typeDefaults = {

  Feature: function(feature) {
    if (feature.geometry) {
      this.geometry(feature.geometry);
    }
  },

  FeatureCollection: function(collection) {
    var features = collection.features;
    var i = -1;
    var n = features.length;
    while (++i < n) {
      this.Feature(features[i]);
    }
  },

  GeometryCollection: function(collection) {
    var geometries = collection.geometries;
    var i = -1;
    var n = geometries.length;
    while (++i < n) {
      this.geometry(geometries[i]);
    }
  },

  LineString: function(lineString) {
    this.line(lineString.coordinates);
  },

  MultiLineString: function(multiLineString) {
    var coordinates = multiLineString.coordinates;
    var i = -1;
    var n = coordinates.length;
    while (++i < n) {
      this.line(coordinates[i]);
    }
  },

  MultiPoint: function(multiPoint) {
    var coordinates = multiPoint.coordinates;
    var i = -1;
    var n = coordinates.length;
    while (++i < n) {
      this.point(coordinates[i]);
    }
  },

  MultiPolygon: function(multiPolygon) {
    var coordinates = multiPolygon.coordinates;
    var i = -1;
    var n = coordinates.length;
    while (++i < n) {
      this.polygon(coordinates[i]);
    }
  },

  Point: function(point) {
    this.point(point.coordinates);
  },

  Polygon: function(polygon) {
    this.polygon(polygon.coordinates);
  },

  object: function(object) {
    return object == null ? null
        : typeObjects.hasOwnProperty(object.type) ? this[object.type](object)
        : this.geometry(object);
  },

  geometry: function(geometry) {
    if(geometry != null && typeGeometries.hasOwnProperty(geometry.type)){
      return this[geometry.type](geometry);
    } else {
      return null;
    }
  },

  point: function() {},

  line: function(coordinates) {
    var i = -1;
    var n = coordinates.length;
    while (++i < n) {
      this.point(coordinates[i]);
    }
  },

  polygon: function(coordinates) {
    var i = -1;
    var n = coordinates.length;
    while (++i < n) {
      this.line(coordinates[i]);
    }
  }
};

module.exports = function(types) {
  for (var type in typeDefaults) {
    if (!(type in types)) {
      types[type] = typeDefaults[type];
    }
  }
  types.defaults = typeDefaults;
  return types;
};