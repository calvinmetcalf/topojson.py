def clock(geo,area):
    if geo.has_key('features') and isinstance(geo['features'],list):
        clockCollection(geo['features'],area)
        return map(lambda x:clockFeatures(x,area),geo['features'])
    elif geo.has_key('features') and isinstance(geo['features'],list):
        return clockCollection(geo,area)
    else:
        out = {}
        for feature in geo:
            out[feature] = clock(geo[feature],area)
        return out
clockCollection = lambda geo,area : map(lambda x:clockFeatures(x,area),geo)
def clockFeatures(geo,area):
    if geo.has_key('type'):
        if geo['type']=='Polygon':
            clockwisePolygon(geo['coordinates'],area)
        if geo['type']=='MultiPolygon':
            map(lambda x:clockwisePolygon(x,area),geo['coordinates'])
def clockwisePolygon(rings,area):
    i=0
    n=0
    r = rings[i]
    if len(rings):
        n=len(rings)
        if area(r)<0:
            r=reversed(r)
    i+=1
    while i<n:
        r=rings[i]
        if area(rings[i]) > 0:
            r=reversed(r)
    return rings
