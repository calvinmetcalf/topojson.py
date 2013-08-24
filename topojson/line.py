from arcs import Arcs
isPoint = lambda x : type(x)==type([]) and len(x)==2
class strut(list):
	def __init__(self,ite=[]):
		self.index=0
		list.__init__(self,ite)
def linesEqual(a, b):
	if not(type(a)==type(b)==type([])):
		return True
	n = len(a);
	i = 0
	if len(b) != n:
		return False
	while i < n:
		if pointCompare(a[i], b[i]):
			return False;
		i+=1
	return True;
def pointCompare(a, b):
	if isPoint(a) and isPoint(b):
		return int(a[0]) - int(b[0]) or int(a[1]) - int(b[1])
def lineContians(line, lineLine):
	for subLine in lineLine:
		if linesEqual(line, subLine):
			return True
	return False
class Line:
	def __init__(self,Q):
		self.arcs = Arcs(Q)
	def matchForward(self,b,arthur):
		i = 0
		n = len(arthur)
		if len(b) != n:
			return False
		while i < n:
			if pointCompare(arthur[i], b[i]):
				return False;
			i+=1
			self.lineArcs.append(b.index)
			return True;
	def matchBackward(self,b,arthur):
		i = 0
		n = len(arthur)
		if len(b) != n:
			return False
		while i<n:
			if pointCompare(arthur[i], b[n - i - 1]):
				return False
			i+=1
		self.lineArcs.append(~b.index)
		return True
	def arc(self,alice, last=False):
		n = len(alice)
		if last and not len(self.lineArcs) and n == 1:
			point = alice[0]
			index = self.arcs.getIndex(point)
			if len(index):
				self.lineArcs.append(index[0])
			else:
				index.append(self.arcs.length)
				self.lineArcs.append(index[0])
				self.arcs.push(alice)
		elif n > 1:
			self.lineArcs.append(self.arcs.check(alice))

	def line(self,points,opened):
		self.lineArcs = [];
		n = len(points)
		arthur = strut()
		k = 1
		p=False
		t=False
		if not opened:
			points.pop()
			n-=1
		while k < n:
			t = self.arcs.peak(points[k])
			if opened:
				break
			if p and not linesEqual(p, t):
				tInP = all(map(lambda line:line in p,t))
				pInT = all(map(lambda line:line in t,p))
				if tInP and not pInT:
					k-=1
				break
			p = t
			k+=1
		# If no shared starting point is found for closed lines, rotate to minimum.
		if k == n and len(p) > 1:
			point0 = points[0]
			i = 2
			k=0
			while i<n:
				point = points[i];
				if pointCompare(point0, point) > 0:
					point0 = point
					k = i
				i+=1
		i = 0
		if opened:
			m = n
		else:
			m = n+1
		while i < m:
			i+=1
			point = points[(i + k) % n]
			p = self.arcs.peak(point)
			if not linesEqual(p, t):
				tInP = all(map(lambda line: line in p,t))
				pInT = all(map(lambda line: line in t,p))
				if tInP:
					arthur.append(point);
				self.arc(arthur)
				if not tInP and not pInT and len(arthur):
					self.arc(strut([arthur[-1], point]))
				if pInT and len(arthur):
					arthur = strut([arthur[-1]])
				else:
					arthur = strut();
			if not len(arthur) or pointCompare(arthur[-1], point):
				arthur.append(point) # skip duplicate points
			t = p
		self.arc(arthur, True)
		return self.lineArcs
	def lineClosed(self,points):
		return self.line(points,False)
	def lineOpen(self,points):
		self.line(points,True)
	def mapFunc (self,arc):
		if len(arc)==2 and type(arc[0])==type(1):
			arc= [arc]
		i = 1
		n = len(arc)
		point = arc[0]
		x1 = point[0]
		x2= dx =y2 = dy=False
		y1 = point[1]
		points = [[int(x1), int(y1)]]
		while i < n:
			point = arc[i]
			if not isPoint(point):
				i+=1
				continue
			x2 = point[0]
			y2 = point[1]
			dx = int(x2 - x1)
			dy = int(y2 - y1)
			if dx or dy:
				points.append([dx, dy])
				x1 = x2
				y1 = y2
			i+=1
		return points
	def getArcs (self):
		return self.arcs.map(self.mapFunc)
