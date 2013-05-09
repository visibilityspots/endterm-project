#!/usr/bin/env python
from optparse import OptionParser, Option, IndentedHelpFormatter

class PosOptionParser(OptionParser):
    def format_help(self, formatter=None):
        class Positional(object):
            def __init__(self, args):
                self.option_groups = []
                self.option_list = args

        positional = Positional(self.positional)
        formatter = IndentedHelpFormatter()
        formatter.store_option_strings(positional)
        output = ['\n', formatter.format_heading("Positional Arguments")]
        formatter.indent()
        pos_help = [formatter.format_option(opt) for opt in self.positional]
        pos_help = [line.replace('--','') for line in pos_help]
        output += pos_help
        return OptionParser.format_help(self, formatter) + ''.join(output)

    def add_positional_argument(self, option):
        try:
            args = self.positional
        except AttributeError:
            args = []
        args.append(option)
        self.positional = args

    def set_out(self, out):
        self.out = out
def main():
    usage = "usage: %prog [options] bar baz"
    parser = PosOptionParser(usage)
    parser.add_option('-f', '--foo', dest='foo',
                      help='Enable foo')
    parser.add_positional_argument(Option('--bar', action='store_true',
                                   help='The bar positional argument'))
    parser.add_positional_argument(Option('--baz', action='store_true',
                                   help='The baz positional argument'))
    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("incorrect number of arguments")
    pass

if __name__ == '__main__':
    main()

