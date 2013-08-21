# TOPOJSON.PY

Port of [topojson](https://github.com/mbostock/topojson) more of a translation then a port at this point, licensed under same BSD license as original, current usage:

```python
from topojson import topology
#give it a path in and out
topology(inPath,outPath,options)
#or file in and path out
topology(open(inPath),outPath,options)
#or file in and file out
topology(open(inPath),open(outPath,'w'),options)
#or a dict in and filepath (or file like object) out
topology(json.load(open(inPath)),outPath,options)
#options is optional
topology(inPath,outPath)#etc
#or omit the outThing and it returns a dict
outTopojson = topology(inPath)
outTopojson = topology(open(inPath))
outTopojson = topology(json.load(open(inPath)))
#options has a can be called by name
outTopojson = topology(inPath,options={'name':'fancypants','quantization':1e3})
#combine files
topology({'name1':load(open(path1)),'name1':load(open(name2))},'compined.topojson')
```


known issues:

- coding style only a mother could love
- holds everything in memory, this could be bad
- should be able to incrementally add features