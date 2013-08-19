# TOPOJSON.PY

Port of [topojson](https://github.com/mbostock/topojson) more of a translation then a port at this point, licensed under same BSD license as original, current usage:

```python
from topojson import topology
from json import load,dump
inJson = load(open('StateRepDistricts.geojson'))
outJson = topology(inJson)
dump(outJson,open('StateRepDistricts.topojson','w'))
```

In theory topology takes a super unpythonic options dict as a second argument, 
haven't tested this yet. Help and pull requests appreciated (especially from those
more fluent at python then I).

**OMFG THIS IS SUPER ALPHA DON'T USE ANYWHERE YOU DON'T MIND EXPLODING**