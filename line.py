from hashtable import hashtable
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
		self.coincidences = hashtable(Q * 10)
		self.arcsByPoint = hashtable(Q * 10)
		self.pointsByPoint = hashtable(Q * 10)
		self.arcs=[]
	def line(self,points, open):
		lineArcs = [];
		n = len(points)
		arthur = strut()
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
		def matchForward(b):
			i = 0
			if len(b) != n:
				return False
			while i < n:
				if pointCompare(arthur[i], b[i]):
					return False;
				i+=1
			lineArcs.append(b.index)
			print('forwards '+str(b.index))
			return True;

		def matchBackward(b):
			i = 0
			if len(b) != n:
				return False
			while i<n:
				if pointCompare(arthur[i], b[n - i - 1]):
					return False
				i+=1
			lineArcs.append(~b.index)
			print('backwards'+str(b.index))
			return True
		def arc(alice, last=False):
			n = len(alice)
			if last and not len(lineArcs) and n == 1:
				point = alice[0]
				index = self.pointsByPoint.get(point)
				if len(index):
					lineArcs.append(index[0])
				else:
					index[0] = len(self.arcs)
					lineArcs.append(index[0])
					self.arcs.append(alice)
			elif n > 1:
				a0 = alice[0]
				a1 = alice[-1]
				point = a0 if pointCompare(a0, a1) < 0 else a1
				pointArcs = self.arcsByPoint.get(point)
				if any(map(matchForward,pointArcs)) or any(map(matchBackward,pointArcs)):
					return
				pointArcs.append(alice)
				alice.index=len(self.arcs)
				lineArcs.append(alice.index)
				self.arcs.append(alice)
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
					arthur.append(point);
				arc(arthur)
				if not tInP and not pInT:
					arc(strut([arthur[-1], point]))
				if pInT and len(arthur):
					arthur = strut([arthur[-1]])
				else:
					arthur = strut();
			if not len(arthur) or pointCompare(arthur[-1], point):
				arthur.append(point) # skip duplicate points
			t = p
		arc(arthur, True)
		return lineArcs
	def lineClosed(self,points):
		return self.line(points,False)
	def lineOpen(self,points):
		self.line(points,True)
