var pi = Math.PI;
var pi4 = pi / 4;
var radians = pi / 180;

exports.name = "spherical";
exports.formatDistance = formatDistance;
exports.ringArea = ringArea;
exports.absoluteArea = absoluteArea;
exports.triangleArea = triangleArea;
exports.distance = haversinDistance; // XXX why two implementations?

function formatDistance(radians) {
  var km = radians * 6371;
  return (km > 1 ? km.toFixed(3) + "km" : (km * 1000).toPrecision(3) + "m") +
    " (" + (radians * 180 / Math.PI).toPrecision(3) + "°)";
}

function ringArea(ring) {
  if (!ring.length) {
    return 0;
  }
  var area = 0;
  var p = ring[0];
  var lambda = p[0] * radians;
  var phi = p[1] * radians / 2 + pi4;
  var lambda0 = lambda;
  var cosphi0 = Math.cos(phi);
  var sinphi0 = Math.sin(phi);

  for (var i = 1, n = ring.length; i < n; ++i) {
    p = ring[i];
    lambda = p[0] * radians;
    phi = p[1] * radians / 2 + pi4;

    // Spherical excess E for a spherical triangle with vertices: south pole,
    // previous point, current point.  Uses a formula derived from Cagnoli’s
    // theorem.  See Todhunter, Spherical Trig. (1871), Sec. 103, Eq. (2).
    var dlambda = lambda - lambda0;
    var cosphi = Math.cos(phi);
    var sinphi = Math.sin(phi);
    var k = sinphi0 * sinphi;
    var u = cosphi0 * cosphi + k * Math.cos(dlambda);
    var v = k * Math.sin(dlambda);
    area += Math.atan2(v, u);

    // Advance the previous point.
    lambda0 = lambda;
    cosphi0 = cosphi;
    sinphi0 = sinphi;
  }

  return 2 * area;
}

function absoluteArea(a) {
  return a < 0 ? a + 4 * pi : a;
}

function triangleArea(t) {
  var a = distance(t[0], t[1]);
  var b = distance(t[1], t[2]);
  var c = distance(t[2], t[0]);
  var s = (a + b + c) / 2;
  return 4 * Math.atan(Math.sqrt(Math.max(0, Math.tan(s / 2) * Math.tan((s - a) / 2) * Math.tan((s - b) / 2) * Math.tan((s - c) / 2))));
}

function distance(a, b) {
  var deltalambda = (b[0] - a[0]) * radians;
  var sindeltalambda = Math.sin(deltalambda);
  var cosdeltalambda = Math.cos(deltalambda);
  var sinphi0 = Math.sin(a[1] * radians);
  var cosphi0 = Math.cos(a[1] * radians);
  var sinphi1 = Math.sin(b[1] * radians);
  var cosphi1 = Math.cos(b[1] * radians);
  var _;
  return Math.atan2(Math.sqrt((_ = cosphi1 * sindeltalambda) * _ + (_ = cosphi0 * sinphi1 - sinphi0 * cosphi1 * cosdeltalambda) * _), sinphi0 * sinphi1 + cosphi0 * cosphi1 * cosdeltalambda);
}

function haversinDistance(x0, y0, x1, y1) {
  x0 *= radians;
  y0 *= radians;
  x1 *= radians;
  y1 *= radians;
  return 2 * Math.asin(Math.sqrt(haversin(y1 - y0) + Math.cos(y0) * Math.cos(y1) * haversin(x1 - x0)));
}

function haversin(x) {
  return (x = Math.sin(x / 2)) * x;
}
