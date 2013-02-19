#!/usr/bin/env python


from unicodeseg import (code_points,
                        grapheme_clusters,
                        words,
                        sentences,
                        line_break_units)


def main():
    
    import argparse
    from locale import getpreferredencoding
    from sys import stdin, stdout, stderr
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--encoding',
                        default=getpreferredencoding(),
                        help="""text encoding of the input <%(default)s>""")
    parser.add_argument('-l', '--legacy',
                        action='store_true',
                        help="""legacy mode (makes sense only with
                        '--mode l')""")
    parser.add_argument('-m', '--mode',
                        choices=['c', 'g', 'l', 's', 'w'],
                        default='w',
                        help="""breaking algorithm <%(default)s>
                        (c: code points, g: grapheme clusters,
                        s: sentences l: line breaking units, w: words)""")
    parser.add_argument('-o', '--output',
                        type=argparse.FileType('w'),
                        default=stdout,
                        help="""leave output to specified file""")
    parser.add_argument('file',
                        nargs='?',
                        type=argparse.FileType('r'),
                        default=stdin,
                        help="""input text file""")
    args = parser.parse_args()
    
    fin = args.file
    fout = args.output
    encoding = args.encoding
    _words = {'c': code_points,
              'g': grapheme_clusters,
              'l': lambda x: line_break_units(x, args.legacy),
              's': sentences,
              'w': words,
              }[args.mode]
    for line in fin:
        line = line.decode(encoding)
        for w in _words(line):
            print >>fout, w.encode(encoding)


if __name__ == '__main__':
    main()
