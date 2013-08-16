var type = require("./type");


module.exports = function(topology, options) {
  var verbose = false;
  var retained = [];
  var j = -1;
  var n = topology.arcs.length;

  if (options && "verbose" in options){
    verbose = !!options.verbose;
  }

  var prune = type({
    LineString: function(lineString) {
      this.line(lineString.arcs);
    },
    MultiLineString: function(multiLineString) {
      var arcs = multiLineString.arcs;
      var i = -1;
      var n = arcs.length;
      while (++i < n) {
        this.line(arcs[i]);
      }
    },
    MultiPoint: noop,
    MultiPolygon: function(multiPolygon) {
      var arcs = multiPolygon.arcs;
      var i = -1;
      var n = arcs.length;
      while (++i < n) {
        this.polygon(arcs[i]);
      }
    },
    Point: noop,
    Polygon: function(polygon) {
      this.polygon(polygon.arcs);
    },
    line: function(arcs) {
      var i = -1;
      var n = arcs.length;
      var arc;
      var reversed;
      while (++i < n) {
        arc = arcs[i];
        reversed = arc < 0;
        if (reversed) {
          arc = ~arc;
        }
        if (retained[arc] == null) {
          retained[arc] = ++j;
          arc = j;
        } else {
          arc = retained[arc];
        }
        arcs[i] = reversed ? ~arc : arc;
      }
    },
    polygon: function(arcs) {
      var i = -1;
      var n = arcs.length;
      while (++i < n) {
        this.line(arcs[i]);
      }
    }
  });

  for (var key in topology.objects) {
    prune.object(topology.objects[key]);
  }

  if (verbose) {
    console.warn("prune: retained " + (j + 1) + " / " + n + " arcs (" + Math.round((j + 1) / n * 100) + "%)");
  }

  var arcs = [];
  retained.forEach(function(i, j) {
    arcs[i] = topology.arcs[j];
  });
  topology.arcs = arcs;
};

function noop() {}