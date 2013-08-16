var type = require("./type"),
    stitch = require("./stitch-poles"),
    hashtable = require("./hashtable"),
    systems = require("./coordinate-systems");

var e = 1e-6;

module.exports = function(objects, options) {
  var Q = 1e4; // precision of quantization
  var id = function(d) { return d.id; }; // function to compute object id
  var propertyTransform = function() {}; // function to transform properties
  var stitchPoles = true;
  var verbose = false;
  var x0, y0, x1, y1;
  var kx, ky;
  var emax = 0;
  var coincidences;
  var system = null;
  var arcs = [];
  var arcsByPoint;
  var pointsByPoint;

  if (options) {
    if ("verbose" in options) {
      verbose = !!options.verbose;
    }
    if ("stitch-poles" in options) {
      stitchPoles = !!options["stitch-poles"];
    }
    if ("coordinate-system" in options) {
      system = systems[options["coordinate-system"]];
    }
    if ("quantization" in options) {
      Q = +options.quantization;
    }
    if ("id" in options) {
      id = options.id;
    }
    if ("property-transform") {
      propertyTransform = options["property-transform"];
    }
  }

  coincidences = hashtable(Q * 10);
  arcsByPoint = hashtable(Q * 10);
  pointsByPoint = hashtable(Q * 10);

  function each(callback) {
    var t = type(callback);
    var o = {};
    for (var k in objects) {
      o[k] = t.object(objects[k]) || {};
    }
    return o;
  }

  // Compute bounding box.
  function bound() {
    x1 = y1 = -(x0 = y0 = Infinity);
    each({
      point: function(point) {
        var x = point[0];
        var y = point[1];
        if (x < x0) {
          x0 = x;
        }
        if (x > x1) {
          x1 = x;
        }
        if (y < y0) {
          y0 = y;
        }
        if (y > y1) {
          y1 = y;
        }
      }
    });
  }

  bound();

  // For automatic coordinate system determination, consider the bounding box.
  var oversize = x0 < -180 - e || x1 > 180 + e || y0 < -90 - e || y1 > 90 + e;
  if (!system) {
    system = systems[oversize ? "cartesian" : "spherical"];
    if (options) {
      options["coordinate-system"] = system.name;
    }
  }

  if (system === systems.spherical) {
    if (oversize) {
      throw new Error("spherical coordinates outside of [±180°, ±90°]");
    }
    if (stitchPoles) {
      stitch(objects);
      bound();
    }

    // When near the spherical coordinate limits, clamp to nice round values.
    // This avoids quantized coordinates that are slightly outside the limits.
    if (x0 < -180 + e) {
      x0 = -180;
    }
    if (x1 > 180 - e) {
      x1 = 180;
    }
    if (y0 < -90 + e) {
      y0 = -90;
    }
    if (y1 > 90 - e) {
      y1 = 90;
    }
  }

  if (!isFinite(x0)) {
    x0 = 0;
  }
  if (!isFinite(x1)) {
    x1 = 0;
  }
  if (!isFinite(y0)) {
    y0 = 0;
  }
  if (!isFinite(y1)) {
    y1 = 0;
  }
  // Compute quantization scaling factors.
  if (Q) {
    kx = x1 - x0 ? (Q - 1) / (x1 - x0) : 1;
    ky = y1 - y0 ? (Q - 1) / (y1 - y0) : 1;
  } else {
    console.warn("quantization: disabled; assuming inputs already quantized");
    Q = x1 + 1;
    kx = ky = 1;
    x0 = y0 = 0;
  }

  if (verbose) {
    var qx0 = Math.round((x0 - x0) * kx) * (1 / kx) + x0;
    var qx1 = Math.round((x1 - x0) * kx) * (1 / kx) + x0;
    var qy0 = Math.round((y0 - y0) * ky) * (1 / ky) + y0;
    var qy1 = Math.round((y1 - y0) * ky) * (1 / ky) + y0;
    console.warn("quantization: bounds " + [qx0, qy0, qx1, qy1].join(" ") + " (" + system.name + ")");
  }

  // Quantize coordinates.
  each({
    point: function(point) {
      var x1 = point[0];
      var y1 = point[1];
      var x = Math.round((x1 - x0) * kx);
      var y = Math.round((y1 - y0) * ky);
      var e = system.distance(x1, y1, x / kx + x0, y / ky + y0);
      if (e > emax) {
        emax = e;
      }
      point[0] = x;
      point[1] = y;
    }
  });

  if (verbose) {
    console.warn("quantization: maximum error "  + system.formatDistance(emax));
  }

  // Compute the line strings that go through each unique point.
  // If the line string goes through the same point more than once,
  // only record that point once.
  each({
    line: function(line) {
      var i = -1;
      var n = line.length;
      var lines;
      while (++i < n) {
        lines = coincidences.get(line[i]);
        if (lines.indexOf(line) < 0) {
          lines.push(line);
        }
      }
    }
  });

  // Convert features to geometries, and stitch together arcs.
  objects = each({
    Feature: function(feature) {
      var geometry = feature.geometry;
      if (feature.geometry == null) {
        geometry = {};
      }
      if ("id" in feature) {
        geometry.id = feature.id;
      }
      if ("properties" in feature) {
        geometry.properties = feature.properties;
      }
      return this.geometry(geometry);
    },

    FeatureCollection: function(collection) {
      collection.type = "GeometryCollection";
      collection.geometries = collection.features.map(this.Feature, this);
      delete collection.features;
      return collection;
    },

    GeometryCollection: function(collection) {
      collection.geometries = collection.geometries.map(this.geometry, this);
    },

    MultiPolygon: function(multiPolygon) {
      multiPolygon.arcs = multiPolygon.coordinates.map(polygon);
    },

    Polygon: function(polygon) {
      polygon.arcs = polygon.coordinates.map(lineClosed);
    },

    MultiLineString: function(multiLineString) {
      multiLineString.arcs = multiLineString.coordinates.map(lineOpen);
    },

    LineString: function(lineString) {
      lineString.arcs = lineOpen(lineString.coordinates);
    },

    geometry: function(geometry) {
      if (geometry == null) {
        geometry = {};
      } else {
        this.defaults.geometry.call(this, geometry);
      }

      geometry.id = id(geometry);
      if (geometry.id == null) {
        delete geometry.id;
      }
      var properties0 = geometry.properties;
      if (properties0) {
        var properties1 = {};
        delete geometry.properties;
        for (var key0 in properties0) {
          if (propertyTransform(properties1, key0, properties0[key0])) {
            geometry.properties = properties1;
          }
        }
      }

      if (geometry.arcs) {
        delete geometry.coordinates;
      }
      return geometry;
    }
  });

  coincidences = arcsByPoint = pointsByPoint = null;

  function polygon(poly) {
    return poly.map(lineClosed);
  }

  function lineClosed(points) {
    return line(points, false);
  }

  function lineOpen(points) {
    return line(points, true);
  }

  function line(points, open) {
    var lineArcs = [];
    var n = points.length;
    var a = [];
    var k = 0;
    var p;
    var point;
    var t;
    var tInP;
    var pInT;
    var i;

    if (!open) {
      points.pop();
      --n;
    }

    // For closed lines, rotate to find a suitable shared starting point.
    for (; k < n; ++k) {
      t = coincidences.peek(points[k]);
      if (open) {
        break;
      }
      if (p && !linesEqual(p, t)) {
        tInP = t.every(function(line) { return p.indexOf(line) >= 0; });
        pInT = p.every(function(line) { return t.indexOf(line) >= 0; });
        if (tInP && !pInT) {
          --k;
        }
        break;
      }
      p = t;
    }
    // If no shared starting point is found for closed lines, rotate to minimum.
    if (k === n && p.length > 1) {
      var point0 = points[0];
      i = 0;
      for (k = 0; i < n; ++i) {
        point = points[i];
        if (pointCompare(point0, point) > 0) {
          point0 = point;
          k = i;
        }
      }
    }
    i = 0;
    for (var m = open ? n : n + 1; i < m; ++i) {
      point = points[(i + k) % n];
      p = coincidences.peek(point);
      if (!linesEqual(p, t)) {
        tInP = t.every(function(line) { return p.indexOf(line) >= 0; });
        pInT = p.every(function(line) { return t.indexOf(line) >= 0; });
        if (tInP) {
          a.push(point);
        }
        arc(a);
        if (!tInP && !pInT) {
          arc([a[a.length - 1], point]);
        }
        if (pInT) {
          a = [a[a.length - 1]];
        } else {
          a = [];
        }
      }
      if (!a.length || pointCompare(a[a.length - 1], point)) {
        a.push(point); // skip duplicate points
      }
      t = p;
    }

    arc(a, true);

    function arc(a, last) {
      var n = a.length;
      var point;
      if (last && !lineArcs.length && n === 1) {
        point = a[0];
        var index = pointsByPoint.get(point);
        if (index.length) {
          lineArcs.push(index[0]);
        } else {
          lineArcs.push(index[0] = arcs.length);
          arcs.push(a);
        }
      } else if (n > 1) {
        var a0 = a[0];
        var a1 = a[n - 1];
        point = pointCompare(a0, a1) < 0 ? a0 : a1;
        var pointArcs = arcsByPoint.get(point);
        if (pointArcs.some(matchForward)) {
          return;
        }
        if (pointArcs.some(matchBackward)) {
          return;
        }
        pointArcs.push(a);
        lineArcs.push(a.index = arcs.length);
        arcs.push(a);
      }

      function matchForward(b) {
        var i = -1;
        if (b.length !== n) {
          return false;
        }
        while (++i < n) {
          if (pointCompare(a[i], b[i])) {
            return false;
          }
        }
        lineArcs.push(b.index);
        return true;
      }

      function matchBackward(b) {
        var i = -1;
        if (b.length !== n) {
          return false;
        }
        while (++i < n) {
          if (pointCompare(a[i], b[n - i - 1])) {
            return false;
          }
        }
        lineArcs.push(~b.index);
        return true;
      }
    }

    return lineArcs;
  }

  return {
    type: "Topology",
    bbox: [x0, y0, x1, y1],
    transform: {
      scale: [1 / kx, 1 / ky],
      translate: [x0, y0]
    },
    objects: objects,
    arcs: arcs.map(function(arc) {
      var i = 0;
      var n = arc.length;
      var point = arc[0];
      var x1 = point[0];
      var x2;
      var dx;
      var y1 = point[1];
      var y2;
      var dy;
      var points = [[x1, y1]];
      while (++i < n) {
        point = arc[i];
        x2 = point[0];
        y2 = point[1];
        dx = x2 - x1;
        dy = y2 - y1;
        if (dx || dy) {
          points.push([dx, dy]);
          x1 = x2;
          y1 = y2;
        }
      }
      return points;
    })
  };
};

function linesEqual(a, b) {
  var n = a.length;
  var i = -1;
  if (b.length !== n) {
    return false;
  }
  while (++i < n) {
    if (a[i] !== b[i]) {
      return false;
    }
  }
  return true;
}

function pointCompare(a, b) {
  return a[0] - b[0] || a[1] - b[1];
}

