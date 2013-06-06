from js2po import *
from jsParser import jsParser
import sys


class splitterParser(jsParser):
    defaultSplitMatcher = re.compile('^// DefaultTable \[([a-zA-Z]*)]')
    splitMatcher = re.compile('^\[([a-zA-Z]*)]')
    defaultTables = ['d']

    def __init__(self):
        jsParser.__init__(self)

    def startFileProcessing(self, contents):
        matches = self.defaultSplitMatcher.search(contents)

        if matches is None:
            self.defaultTables = ['d']
        else:
            self.defaultTables = []
            for t in matches.group(1):
                self.defaultTables.append(t)

    def tablesForData(self, string, comment, table):
        tables = []
        m = None

        if comment is not None:
            m = self.splitMatcher.search(comment)

        if m:
            comment = comment[m.end(0):].strip()

            for split in m.group(1):
                tables.append(table + '.' + split)
        else:
            for t in self.defaultTables:
                tables.append(table + '.' + t)

        return tables


if __name__ == "__main__":
    sys.exit(main(parser=splitterParser()))
