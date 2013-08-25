from hashtable import hashtable
import shelve
from os import getcwd,remove
from hashlib import sha1
isPoint = lambda x : type(x)==type([]) and len(x)==2
def pointCompare(a, b):
    if isPoint(a) and isPoint(b):
        return int(a[0]) - int(b[0]) or int(a[1]) - int(b[1])
class Arcs:
    def __init__(self,Q):
        self.coincidences = hashtable(Q * 10)
        self.arcsByPoint = hashtable(Q * 10)
        self.pointsByPoint = hashtable(Q * 10)
        self.arcs= shelve.open(getcwd()+'/arcDB')
        self.length=0
        self.db = shelve.open(getcwd()+'/storage')
    def getIndex(self,point):
        return self.pointsByPoint.get(point)
    def getPointArcs(self,point):
        return self.arcsByPoint.get(point)
    def coincidenceLines(self,point):
        return self.coincidences.get(point)
    def peak(self,point):
        return self.coincidences.peak(point)
    def push(self,arc):
        self.arcs[str(self.length)]=arc
        self.length+=1
        return self.length
    def map(self,func):
        self.db.close()
        remove(getcwd()+'/storage')
        out = []
        for num in range(0,self.length):
            out.append(func(self.arcs[str(num)]))
        self.arcs.close()
        remove(getcwd()+'/arcDB')
        return out
    def getHash(self,arc):
        ourhash = sha1()
        ourhash.update(str(arc))
        return ourhash.hexdigest()
    def check(self,arcs):
        a0 = arcs[0]
        a1 = arcs[-1]
        point = a0 if pointCompare(a0, a1) < 0 else a1
        pointArcs = self.getPointArcs(point)
        h = self.getHash(arcs)
        if self.db.has_key(h):
            return int(self.db[h])
        else:
            index = self.length
            pointArcs.append(arcs)
            self.db[h]=index
            self.db[self.getHash(list(reversed(arcs)))]=~index
            self.push(arcs)
            return index
        
