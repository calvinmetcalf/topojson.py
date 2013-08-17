# coding=utf8
from math import sqrt,pi,cos,sin,atan2,tan,atan,asin
systems = {}
systems['cartesian']={}
systems['spherical']={}


def cartformatDistance(d):
	return str(d)


def cartringArea(ring):
	area = ring[-1][1] * ring[0][0] - ring[-1][0] * ring[0][1]
	i=0
	for j in ring:
		area += ring[i - 1][1] * j[0] - ring[i - 1][0] * j[1];
		i+=1
	return area*0.5

def carttriangleArea(triangle):
	return abs((triangle[0][0] - triangle[2][0]) * (triangle[1][1] - triangle[0][1]) -(triangle[0][0] - triangle[1][0]) * (triangle[2][1] - triangle[0][1]))

def cartdistance(x0, y0, x1, y1):
	dx = x0 - x1
	dy = y0 - y1
	return sqrt(dx * dx + dy * dy)


pi4 = pi / 4
radians = pi / 180
systems['cartesian']['name'] = "cartesian"
systems['cartesian']['formatDistance'] = cartformatDistance
systems['cartesian']['ringArea'] = cartringArea
systems['cartesian']['absoluteArea'] = abs
systems['cartesian']['triangleArea'] = carttriangleArea
systems['cartesian']['distance'] = cartdistance


def sphformatDistance(radians):
	km = radians * 6371.0;
	return (str(round(km,3)) +"km" if km > 1 else "%.3fm"%(km * 1000)) + " (%.3f°)"%(radians * 180 / pi)

def sphringArea(ring):
	if not len(ring):
		return 0
	area = 0
	p = ring[0]
	lambd = p[0] * radians
	phi = p[1] * radians / 2.0 + pi4
	lambda0 = lambd
	cosphi0 = cos(phi)
	sinphi0 = sin(phi)
	for pp in ring[1:]:
		lambd = pp[0] * radians;
		phi = pp[1] * radians / 2.0 + pi4;
		# Spherical excess E for a spherical triangle with vertices: south pole,
		# previous point, current point.  Uses a formula derived from Cagnoli’s
		# theorem.  See Todhunter, Spherical Trig. (1871), Sec. 103, Eq. (2).
		dlambda = lambd - lambda0
		cosphi = cos(phi)
		sinphi = sin(phi)
		k = sinphi0 * sinphi
		u = cosphi0 * cosphi + k * cos(dlambda)
		v = k * sin(dlambda)
		area += atan2(v, u)
		#Advance the previous point.
		lambda0 = lambd;
		cosphi0 = cosphi;
		sinphi0 = sinphi;
	return 2 * area;


def sphabsoluteArea(a):
	return a + 4 * pi if a < 0 else a


def sphtriangleArea(t):
	a = distance(t[0], t[1])
	b = distance(t[1], t[2])
	c = distance(t[2], t[0])
	s = (a + b + c) / 2.0
	return 4 * atan(sqrt(max(0, tan(s / 2.0) * tan((s - a) / 2.0) * tan((s - b) / 2.0) * tan((s - c) / 2.0))))

def distance(a, b):
	deltalambda = (b[0] - a[0]) * radians
	sindeltalambda = Math.sin(deltalambda)
	cosdeltalambda = Math.cos(deltalambda)
	sinphi0 = Math.sin(a[1] * radians)
	cosphi0 = Math.cos(a[1] * radians)
	sinphi1 = Math.sin(b[1] * radians)
	cosphi1 = Math.cos(b[1] * radians)
	cs=cosphi1 * sindeltalambda
	cs2 = cosphi0 * sinphi1 - sinphi0 * cosphi1 * cosdeltalambda
	return Math.atan2(Math.sqrt(cs * cs + cs2 * cs2), sinphi0 * sinphi1 + cosphi0 * cosphi1 * cosdeltalambda)

def sphhaversinDistance(x0, y0, x1, y1):
	x0 *= radians;
	y0 *= radians;
	x1 *= radians;
	y1 *= radians;
	return 2.0 * asin(sqrt(haversin(y1 - y0) + cos(y0) * cos(y1) * haversin(x1 - x0)))
systems['spherical']['name'] = "spherical";
systems['spherical']['formatDistance'] = sphformatDistance;
systems['spherical']['ringArea'] = sphringArea;
systems['spherical']['absoluteArea'] = sphabsoluteArea;
systems['spherical']['triangleArea'] = sphtriangleArea;
systems['spherical']['distance'] = sphhaversinDistance;

def haversin(x):
	x = sin(x / 2.0)
	return x*x
