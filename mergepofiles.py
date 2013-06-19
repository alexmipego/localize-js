import os
import sys
import getopt


tables = {}


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hi:l:", ["help", "ignore=", "language="])
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

    for arg in args[2:]:
        projects.append(arg)

    for opt, arg in opts:
        if opt in ('-i', '--ignore'):
            ignores.append(arg)
        elif opt in ('-l', '--language'):
            language = arg

    # Start
    dirs = []
    for proj in projects:
        dirs.append(os.path.join(sourceDir, proj, language))

    for dir in dirs:
        files = [ f for f in os.listdir(dir) if isfile(join(dir,f)) ]
        print files


if __name__ == "__main__":
    sys.exit(main())
