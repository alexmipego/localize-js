import re, os, sys, fnmatch, getopt
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
            opts, args = getopt.getopt(argv[1:], "ho:", ["help", "output="])
        except getopt.error, msg:
            raise Usage(msg)
            # more code, unchanged
    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 2

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
                processFile(filePath, os.path.relpath(filePath, rootdir))

    for k in tables:
        po = polib.POFile()
        po.metadata = {}

        for string in sorted(tables[k].iterkeys()):
            po.append(polib.POEntry(
                msgid=string,
                #msgstr=string,
                comment='\n'.join(tables[k][string]['comments']),
                occurrences=tables[k][string]['occurrences']
            ))

        filename = os.path.join(output_dir, k + '.pot')

        po.save(filename)
        print 'Saved to ' + filename

jsStringRe = "(?:\s*)(?:"\
             "(?:'((?:(?:[^\\']|.'))*?)')|(?:\"((?:(?:[^\\\"]|.\"))*?)\")"\
             ")(?:\s*)(?:,*)(?:\s*)"
matcher = re.compile("Localize(?:\s*)\((?:" + jsStringRe + ")(?:" + jsStringRe + ")?(?:" + jsStringRe + ")?\)",
    re.VERBOSE)
doubleChecker = re.compile("Localize\s*\(")

def processFile(path, filename):
    file = open(path, "r")
    text = file.read()
    file.close()

    found = 0

    doubleCheckerMatches = doubleChecker.findall(text)

    for m in matcher.finditer(text):
        found += 1
        processMatch(m.groups(), filename, m.start())

    if found != len(doubleCheckerMatches):
        print >> sys.stderr, "Only found %d out of %d. %s" % (found, len(doubleCheckerMatches), path)


def processMatch(match, filename, position):
    string = match[0]
    comment = match[2]
    table = match[4]
    if not string is None and len(string) <= 0:
        string = match[1]
    if not comment is None and len(comment) <= 0:
        comment = match[3]
    if not table is None and len(table) <= 0:
        table = match[5]

    if string is None or len(string) == 0:
        return

    string = string.decode("string-escape")#string.replace(r"\\\\", r"\\")

    if table is None or len(table) <= 0:
        table = '__main'

    if not tables.has_key(table):
        tables[table] = {}

    if not tables[table].has_key(string):
        tables[table][string] = {'comments': [], 'occurrences': []}

    if not comment is None and not comment in tables[table][string]['comments']:
        tables[table][string]['comments'].append(comment)

    tables[table][string]['occurrences'].append((filename, position))

    return (string, comment, table)

if __name__ == "__main__":
    sys.exit(main())
