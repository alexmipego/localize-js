import os
import fnmatch
import getopt
import polib
import sys
from jsParser import *


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None, parser=jsParser()):
    if argv is None:
        argv = sys.argv

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:", ["help", "output="])
        except getopt.error, msg:
            raise Usage(msg)
            # more code, unchanged
    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 2

    parser.doubleChecker = re.compile("{{do-localize\s*")
    parser.matcher = re.compile("{{do-localize(?:\s*)(?:" + parser.jsStringRe + ")(?:" + parser.jsStringRe + ")?(?:" + parser.jsStringRe + ")?(.*)}}", re.VERBOSE)

    output_dir = None
    for opt, arg in opts:
        if opt in ('-o', '--output'):
            output_dir = arg

    if output_dir is None:
        raise Usage('Output directory is required.')

    output_dir = os.path.expandvars(os.path.expanduser(output_dir))

    rootdir = os.path.expandvars(os.path.expanduser(args[0]))
    filterexpr = args[1]
    for root, subfolders, files in os.walk(rootdir):
        for file in files:
            if fnmatch.fnmatch(file, filterexpr):
                filePath = os.path.join(root, file)
                parser.processFile(filePath, os.path.relpath(filePath, rootdir))

    for k in parser.tables:
        po = polib.POFile()
        po.metadata = {}

        for string in sorted(parser.tables[k].iterkeys()):
            po.append(polib.POEntry(
                msgid=string.decode("utf-8"),
                #msgstr=string,
                comment=('\n'.join(parser.tables[k][string]['comments'])).decode("utf-8"),
                occurrences=parser.tables[k][string]['occurrences']
            ))

        filename = os.path.join(output_dir, k + '.pot')

        po.save(filename)
        print 'Saved to ' + filename

if __name__ == "__main__":
    sys.exit(main())
