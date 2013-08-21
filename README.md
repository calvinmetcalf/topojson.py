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


known issues:
__init__.py
- coding style only a mother could love
- holds everything in memory, this could be bad
- should be able to incrementally add features