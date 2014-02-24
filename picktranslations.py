import	os, sys, getopt
import polib

tables = {}

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	if argv is None:
		argv = sys.argv

	try:
		try:
			opts, args = getopt.getopt(argv[1:], "", [])
		except getopt.error, msg:
			raise Usage(msg)
			# more code, unchanged
	except Usage, err:
		print >> sys.stderr, err.msg
		print >> sys.stderr, "for help use --help"
		return 2
		
	translations = {}
	for arg in reversed(args[1:]):
		for entry in polib.pofile(os.path.expandvars(os.path.expanduser(arg))).translated_entries():
			translations[entry.msgid] = entry.msgstr
	
	filePath = os.path.expandvars(os.path.expanduser(args[0]))
	file = polib.pofile(filePath)
	for entry in file.untranslated_entries():
		if entry.msgid in translations:
			entry.msgstr = translations[entry.msgid]
		else:
			print 'Still untranslated: "%s"' % (entry.msgid)
			
	file.save(filePath)


if __name__ == "__main__":
	sys.exit(main())

