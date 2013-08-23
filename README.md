# TOPOJSON.PY

Port of [topojson](https://github.com/mbostock/topojson) more of a translation then a port at this point, licensed under same BSD license as original, current usage:

```python
from topojson import topojson
#give it a path in and out
topojson(inPath,outPath,options)
#or file in and path out
topojson(open(inPath),outPath,options)
#or file in and file out
topojson(open(inPath),open(outPath,'w'),options)
#or a dict in and filepath (or file like object) out
topojson(json.load(open(inPath)),outPath,options)
#options is optional
topojson(inPath,outPath)#etc
#or omit the outThing and it returns a dict
outTopojson = topojson(inPath)
outTopojson = topojson(open(inPath))
outTopojson = topojson(json.load(open(inPath)))
#options has a can be called by name
outTopojson = topojson(inPath,options={'name':'fancypants','quantization':1e3})
#combine files
topojson({'name1':load(open(path1)),'name1':load(open(name2))},'compined.topojson')
```

can also go the other way.

```python
from topojson import geojson
geojson(topojson,input_name=None,out_geojson=None)
```
`topojson` may be a dict, a path, or a file like object, `input_name` is a string and if omited
the first object in `topojson.objects` is used, `geojson` may be a file like object or
a path if omitied the dict is returned

known issues:
- coding style only a mother could love
- holds everything in memory, this could be bad
- should be able to incrementally add features to a topojson object
- should work with lines