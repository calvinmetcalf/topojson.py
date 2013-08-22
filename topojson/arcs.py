from hashtable import hashtable

class Arcs:
	def __init__(self,Q):
		self.coincidences = hashtable(Q * 10)
		self.arcsByPoint = hashtable(Q * 10)
		self.pointsByPoint = hashtable(Q * 10)
		self.arcs=[]
		self.length=0
	def getIndex(self,point):
		return self.pointsByPoint.get(point)
	def getPointArcs(self,point):
		return self.arcsByPoint.get(point)
	def coincidenceLines(self,point):
		return self.coincidences.get(point)
	def peak(self,point):
		return self.coincidences.peak(point)
	def push(self,arc):
		self.arcs.append(arc)
		self.length+=1
	def map(self,func):
		return map(func,self.arcs)