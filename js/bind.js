var type = require("./type");

function bindFunc(topology, propertiesById) {
  var key;
  var bind = type({
    geometry: function(geometry) {
      var properties0 = geometry.properties;
      var properties1 = propertiesById[geometry.id];
      var k;
      if (properties1) {
        if (properties0){
          for (k in properties1){
            properties0[k] = properties1[k];
          }
        } else {
          for (k in properties1) {
            geometry.properties = properties1;
            break;
          }
        }
      }
      this.defaults.geometry.call(this, geometry);
    },
    LineString: noop,
    MultiLineString: noop,
    Point: noop,
    MultiPoint: noop,
    Polygon: noop,
    MultiPolygon: noop
  });

  for (key in topology.objects) {
    bind.object(topology.objects[key]);
  }
}

function noop() {
    //pass
}
module.exports = bindFunc;