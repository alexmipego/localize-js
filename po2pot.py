import os
import sys
import getopt
import subprocess
import polib

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	if argv is None:
		argv = sys.argv

	try:
		try:
			opts, args = getopt.getopt(argv[1:], "h", ["help"])
		except getopt.error, msg:
			raise Usage(msg)
			# more code, unchanged
	except Usage, err:
		print >> sys.stderr, err.msg
		print >> sys.stderr, "for help use --help"
		return 2

	po = polib.pofile(os.path.expandvars(os.path.expanduser(args[0])))
	pot = polib.POFile()

	for entry in po:
		if len(entry.msgstr) > 0:
			entry.msgid = entry.msgstr
			entry.msgstr = ''

		pot.append(entry)

	pot.save(os.path.expandvars(os.path.expanduser(args[1])))


if __name__ == "__main__":
	sys.exit(main())
