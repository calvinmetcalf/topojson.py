from topology import topology
from json import load,dump

def convert(inThing,outThing=None,options={}):
	if isinstance(inThing,dict):
		inpt = inThing
	elif isinstance(inThing,str) or isinstance(inThing,unicode):
		inFile = open(inThing)
		inpt = load(inFile)
		if not options.has_key('name') and inpt.has_key('type') and hasattr(inFile,'name') and inFile.name.lower().endswith('.geojson'):
			inpt = {inFile.name[:-8].split('/')[-1]:inpt}
	elif isinstance(inThing,file):
		inpt=load(inThing)
		if not options.has_key('name') and inpt.has_key('type') and hasattr(inThing,'name') and inThing.name.lower().endswith('.geojson'):
			inpt = {inThing.name[:-8].split('/')[-1]:inpt}
	out = topology(inpt,options)
	if isinstance(outThing,str) or isinstance(outThing,unicode):
		with open(outThing,'w') as f:
			dump(out,f)
	elif isinstance(outThing,file):
		dump(out,outThing)
	else:
		return out