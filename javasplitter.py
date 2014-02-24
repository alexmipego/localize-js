import os, sys, getopt
import polib
import json

tables = {}

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def appendToMap(projMap, proj, entry):
	if not proj in projMap:
		projMap[proj] = {}
		
	if not entry.msgid in projMap[proj]:
		projMap[proj][entry.msgid] = entry

def main(argv=None):
	if argv is None:
		argv = sys.argv

	try:
		try:
			opts, args = getopt.getopt(argv[1:], "ho:l:f:", ["help"])
		except getopt.error, msg:
			raise Usage(msg)
			# more code, unchanged
	except Usage, err:
		print >> sys.stderr, err.msg
		print >> sys.stderr, "for help use --help"
		return 2

	pofile = os.path.expandvars(os.path.expanduser(args[0]))
	outdir = os.path.expandvars(os.path.expanduser(args[1]))
	
	defaultProj = args[2]
	projs = {}
	projMap = { }
	lastProj = None
	
	for arg in args[3:]:
		if lastProj is None:
			lastProj = arg
		else:
			projs[lastProj] = arg
			lastProj = None
	
	po = polib.pofile(pofile)
	
	for entry in po:
		newOccList = []
		for (loc, line) in entry.occurrences:
			done = False
			for proj in projs.keys():
				if loc.startswith(proj + '_'):
					newOccList.append((loc[len(proj + '_'):], ''))

					appendToMap(projMap, projs[proj], entry)
					done = True
					break
			
			if not done:
				appendToMap(projMap, defaultProj, entry)
				newOccList.append((loc, ''))
				
		entry.occurrences = newOccList
					
	outtpl = os.path.join(outdir, os.path.splitext(os.path.basename(pofile))[0])
	
	for (proj, entryMap) in projMap.items():
		newPo = polib.POFile()
		newPo.extend(entryMap.values())
		
		newPo.save(outtpl + '.' + proj + '.pot')	


if __name__ == "__main__":
	sys.exit(main())

