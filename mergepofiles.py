import os
import sys
import getopt
import subprocess
import polib
import copy

tables = {}


class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	if argv is None:
		argv = sys.argv

	try:
		try:
			opts, args = getopt.getopt(argv[1:], "hi:l:rj", ["help", "ignore=", "language=", "reverseIgnores", 'javaMode'])
		except getopt.error, msg:
			raise Usage(msg)
			# more code, unchanged
	except Usage, err:
		print >> sys.stderr, err.msg
		print >> sys.stderr, "for help use --help"
		return 2

	sourceDir = os.path.expandvars(os.path.expanduser(args[0]))
	outputDir = os.path.expandvars(os.path.expanduser(args[1]))
	projects = []
	language = 'en'
	ignores = []
	reverseIgnoresMode = False
	javaMode = False

	for arg in args[2:]:
		projects.append(arg)

	for opt, arg in opts:
		if opt in ('-i', '--ignore'):
			ignores.append(arg)
		elif opt in ('-l', '--language'):
			language = arg
		elif opt in ('-r', '--reverseIgnores'):
			reverseIgnoresMode = True
		elif opt in ('-j', '--javaMode'):
			javaMode = True
			
	# Start
	dirs = []
	for proj in projects:
		dirs.append(os.path.join(sourceDir, proj, language))

	merges = {}
	for dir in dirs:
		files = [ f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f)) ]
		for file in files:
			base = os.path.splitext(os.path.basename(file))[0]
			full = os.path.join(dir, file)
			if (not reverseIgnoresMode and base in ignores) or (reverseIgnoresMode and base not in ignores):
				continue
			elif base in merges:
				merges[base].append(full)
			else:
				merges[base] = [full]
	
	for m in merges:
		mergedPo = polib.POFile()
		for f in merges[m]:
			for entry in polib.pofile(f).translated_entries():
				if len(entry.msgstr)  <= 0:
					continue
				
				if not javaMode and not entry.msgid in [e.msgid for e in mergedPo]:
					mergedPo.append(entry)
					continue
				elif javaMode:
					for occurrence, _ignore in entry.occurrences:
						if not occurrence in [o[0][0] for o in [e.occurrences for e in mergedPo]]:
							clone = polib.POEntry(
								msgid=entry.msgid, 
								msgstr=entry.msgstr, 
								occurrences=[(occurrence, '')])

							mergedPo.append(clone)
					
		mergedPo.save(os.path.join(outputDir, m + '.po'))


if __name__ == "__main__":
	sys.exit(main())
