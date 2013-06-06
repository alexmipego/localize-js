import sys
import re


class jsParser:
    jsStringRe = "(?:\s*)(?:"\
        "(?:'((?:(?:[^\\']|.'))*?)')|(?:\"((?:(?:[^\\\"]|.\"))*?)\")"\
        ")(?:\s*)(?:,*)(?:\s*)"

    doubleChecker = re.compile("Localize\s*\(")
    tables = {}

    def __init__(self):
        self.matcher = re.compile("Localize(?:\s*)\((?:" + self.jsStringRe + ")(?:" + self.jsStringRe + ")?(?:" + self.jsStringRe + ")?\)", re.VERBOSE)

    def startFileProcessing(self, contents):
        pass

    def tablesForData(self, string, comment, table):
        return [table]

    def processFile(self, path, filename):
        file = open(path, "r")
        text = file.read()
        file.close()

        self.startFileProcessing(text)

        found = 0

        doubleCheckerMatches = self.doubleChecker.findall(text)

        for m in self.matcher.finditer(text):
            found += 1
            self.processMatch(m.groups(), filename, m.start())

        if found != len(doubleCheckerMatches):
            print >> sys.stderr, "Only found %d out of %d. %s" % (found, len(doubleCheckerMatches), path)

    def processMatch(self, match, filename, position):
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

        string = string.decode("string-escape")

        if table is None or len(table) <= 0:
            table = 'Default'

        for table in self.tablesForData(string, comment, table):
            if not table in self.tables:
                self.tables[table] = {}

            if not string in self.tables[table]:
                self.tables[table][string] = {'comments': [], 'occurrences': []}

            if not comment is None and not comment in self.tables[table][string]['comments']:
                self.tables[table][string]['comments'].append(comment)

            self.tables[table][string]['occurrences'].append((filename, position))

        return (string, comment, table)
