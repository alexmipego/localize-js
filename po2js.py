import  os, sys, getopt
import polib
import json

tables = {}

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:l:", ["help", "output=", "locale="])
        except getopt.error, msg:
            raise Usage(msg)
            # more code, unchanged
    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 2

    pofilepath = os.path.expandvars(os.path.expanduser(args[0]))
    for opt, arg in opts:
        if opt in ('-o', '--output'):
            output_filename = arg
        elif opt in ('-l', '--locale'):
            locale = arg

    if locale is None:
        raise Usage('Locale is required.')

    if output_filename is None:
        output_filename = os.path.join(os.path.dirname(pofilepath), locale + '.js')

    output_filename = os.path.expandvars(os.path.expanduser(output_filename))

    jsonObject = {};
    po = polib.pofile(pofilepath)
    for entry in po.translated_entries():
        jsonObject[entry.msgid] = entry.msgstr

    jsonString = 'if(!window.localizations) { window.localizations={}; }\n'
    jsonString += 'window.localizations["' + locale + '"] = ' + json.dumps(jsonObject, sort_keys=True) + ';'

    file = open(output_filename, "w")
    text = file.write(jsonString)
    file.close()

    print 'Wrote js to ' + output_filename


if __name__ == "__main__":
    sys.exit(main())

