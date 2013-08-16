from math import ceil, log

def hasher(size):
    mask = int(size) - 1;
    def retFunc(point):
        key = (int(point[0]) + 31 * int(point[1])) | 0
        return (~key if key < 0 else key) & mask
    return retFunc

def hashtable(size):
    size = 1 << int(ceil(log(size)/log(2)))
    table = tuple(map(lambda x:False,range(0,size)))
    h = hasher(size)
    r = {}
    r['size']=size
    def peak(key):
        matches = table[h(key)]
        if matches:
            for match in matches:
                if equal(match['key'], key):
                    return match['values']
        return None
    r['peak']=peak
    def get(key):
        index = h(key)
        matches = table[index]
        if (matches):
            for match in matches:
                if equal(match['key'], key):
                    return match['values']
        else:
            matches = table[index] = []
        values = []
        matches.append({'key': key, 'values': values});
        return values;
    r['get']=get
    return r
def equal(keyA, keyB):
    return keyA[0] == keyB[0] and keyA[1] == keyB[1]