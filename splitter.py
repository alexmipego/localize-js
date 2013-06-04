from js2po import *
from jsParser import jsParser
import sys


class splitterParser(jsParser):
    splitMatcher = re.compile('^\[([a-zA-Z]*)]')

    def __init__(self):
        jsParser.__init__(self)

    def startFileProcessing(self, path, filename, file):
        pass

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
            tables.append(table + '.d')

        return tables


if __name__ == "__main__":
    sys.exit(main(parser=splitterParser()))
