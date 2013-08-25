def point_compare(a, b):
    if is_point(a) and is_point(b):
        return a[0] - b[0] or a[1] - b[1]
def is_point(p):
    try:
        float(p[0]), float(p[1])
    except (TypeError, IndexError):
        return False
class Strut(list):
    def __init__(self,ite=[]):
        self.index=0
        list.__init__(self,ite)
def is_infinit(n):
    return abs(n)==float('inf')
E = 1e-6
def lines_equal(a, b):
    if not (type(a) == type(b) == type([])):
        return True
    n = len(a)
    i = 0
    if len(b) != n:
        return False
    while i < n:
        if a[i] != b[i]:
            return False
        i += 1
    return True
#def lines_equal(a, b):
#    for arg in (a, b):
#        if not isinstance(arg, list):
#            return False
#    return a == b
