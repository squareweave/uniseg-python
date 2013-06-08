#!/usr/bin/env python
"""Unicode-aware text wrapping.

Masaaki Shibata <mshibata@emptypage.jp>
http://www.emptypage.jp/
"""


from uniseg import TTWrapper


def main():
    
    import argparse
    from sys import stdin, stdout, stderr
    from locale import getpreferredencoding
    
    encoding = getpreferredencoding()
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--encoding',
                        default=encoding,
                        help='file encoding <%(default)s>')
    parser.add_argument('-x', '--expand-tabs',
                        action='store_true',
                        help='expand tabs to spaces')
    parser.add_argument('-j', '--justify',
                        action='store_true',
                        help='justify lines')
    parser.add_argument('-r', '--ruler',
                        action='store_true',
                        help='show ruler')
    parser.add_argument('-t', '--tab-width',
                        type=int,
                        default=8,
                        help='tab width <%(default)d>')
    parser.add_argument('-l', '--legacy',
                        action='store_true',
                        help='treat ambiguous-width letters as wide')
    parser.add_argument('-o', '--output',
                        type=argparse.FileType('w'),
                        default=stdout,
                        help='leave output to specified file')
    parser.add_argument('-w', '--wrap-width',
                        type=int,
                        default=60,
                        help='wrap width <%(default)s>')
    parser.add_argument('-c', '--char-wrap',
                        action='store_true',
                        help="""wrap on grapheme boundaries instead of 
                        line break boundaries""")
    parser.add_argument('file',
                        nargs='?',
                        type=argparse.FileType('r'),
                        default=stdin,
                        help='input file')
    args = parser.parse_args()
    
    wrapper = TTWrapper()
    wrapper.expand_tabs = args.expand_tabs
    wrapper.justify = args.justify
    wrapper.tab_width = tab_width = args.tab_width
    wrapper.legacy = args.legacy
    wrapper.wrap_width = wrap_width = args.wrap_width
    wrapper.char_wrap = args.char_wrap
    encoding = args.encoding
    fin = args.file
    fout = args.output
    if args.ruler:
        if tab_width:
            rul = ('+' + '-' * (tab_width - 1)) * (wrap_width / tab_width + 1)
            ruler = rul[:wrap_width]
        else:
            ruler = '-' * wrap_width
        print >>fout, ruler
    
    for para in fin:
        para = para.decode(encoding)
        for line in wrapper.wrap(para):
            print >>fout, line.rstrip('\n').encode(encoding)


if __name__ == '__main__':
    main()
