from hashtable import hashtable
isPoint = lambda x : type(x)==type([]) and len(x)==2
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

class Line:
	def __init__(self,Q):
		self.coincidences = hashtable(Q * 10)
		self.arcsByPoint = hashtable(Q * 10)
		self.pointsByPoint = hashtable(Q * 10)
		self.arcs=[]
	def line(self,points, open):
		lineArcs = [];
		n = len(points)
		a = []
		k = 1
		p=False
		t=False
		if not open:
			points.pop()
			n-=1
		while k<n:
			t = self.coincidences.peak(points[k])
			if open:
				break
			if p and not linesEqual(p, t):
				tInP = all(map(lambda line: line in p,t))
				pInT = all(map(lambda line: line in t,p))
				if tInP and not pInT:
					k-=1
				break;
			p = t;
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
		def matchForward(b,index):
			i = 0;
			if len(b) != n:
				return False
			while i < n:
				if pointCompare(a[i], b[i]):
					return False;
				i+=1
			lineArcs.append(b[index])
			return True;

		def matchBackward(b,index):
			i = 0
			if len(b) != n:
				return False
			while i<n:
				if pointCompare(a[i], b[n - i - 1]):
					return False
				i+=1
			lineArcs.append(~b[index])
			return True
		def arc(a, last=False):
			n = len(a)
			point=False
			index=-1
			if last and not len(lineArcs) and n == 1:
				point = a[0]
				index = self.pointsByPoint.get(point)
				if len(index):
					lineArcs.append(index[0])
				else:
					index[0] = len(self.arcs)
					lineArcs.append(index[0])
					self.arcs.append(a)
			elif n > 1:
				a0 = a[0]
				a1 = a[-1]
				point = a0 if pointCompare(a0, a1) < 0 else a1
				pointArcs = self.arcsByPoint.get(point)
				if any(map(lambda x:matchForward(x,index),pointArcs)) or any(map(lambda x:matchBackward(x,index),pointArcs)):
					return
				pointArcs.append(a)
				a[index]=len(self.arcs)
				lineArcs.append(a[index])
				self.arcs.append(a)
		i = 0
		if open:
			m = n
		else:
			m = n+1
		while i < m:
			i+=1
			point = points[(i + k) % n]
			p = self.coincidences.peak(point)
			if not linesEqual(p, t):
				tInP = all(map(lambda line: line in p,t))
				pInT = all(map(lambda line: line in t,p))
				if tInP:
					a.append(point);
				arc(a)
				if not tInP and not pInT:
					arc([a[-1], point])
				if pInT and len(a):
					a = [a[-1]]
				else:
					a = [];
			if not len(a) or pointCompare(a[-1], point):
				a.append(point) # skip duplicate points
			t = p
		arc(a, True)
		return lineArcs
	def lineClosed(self,points):
		return self.line(points,False)
	def lineOpen(self,points):
		self.line(points,True)