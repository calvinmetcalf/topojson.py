from topology import topology
from json import load,dump

def convert(inThing,outThing=None,object_name=False, *args, **kwargs):
  if isinstance(inThing,dict):
    inpt = inThing
  elif isinstance(inThing,str) or isinstance(inThing,unicode):
    inFile = open(inThing)
    inpt = load(inFile)
    if not object_name and inpt.has_key('type') and hasattr(inFile,'name') and inFile.name.lower().endswith('.geojson'):
      inpt = {inFile.name[:-8].split('/')[-1]:inpt}
  elif isinstance(inThing,file):
    inpt=load(inThing)
    if not object_name and inpt.has_key('type') and hasattr(inThing,'name') and inThing.name.lower().endswith('.geojson'):
      inpt = {inThing.name[:-8].split('/')[-1]:inpt}
  if 'type' in inpt:
   if object_name:
    inpt = {object_name:inpt}
   else:
    inpt = {'name':inpt}
  out = topology(inpt, *args, **kwargs)
  if isinstance(outThing,str) or isinstance(outThing,unicode):
    with open(outThing,'w') as f:
      dump(out,f)
  elif isinstance(outThing,file):
    dump(out,outThing)
  else:
    return out
