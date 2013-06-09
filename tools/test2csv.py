#!/usr/bin/env python


from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import os.path
import re
import sys


def csv_escape(value):
    
    '''Return escaped string suitable as a CSV field
    
    >>> csv_escape(1)
    '1'
    >>> csv_escape('hello')
    'hello'
    >>> csv_escape(',')
    '","'
    >>> csv_escape('"hi"')
    '"""hi"""'
    
    '''
    
    s = '%s' % value
    if re.search(r'[,"\n]', s):
        s = '"%s"' % s.replace('"', '""')
    
    return s


def split_comment(line):
    
    if '#' in line:
        data, comment = line.split('#', 1)
    else:
        data = line
        comment = ''
    return data.strip(), comment.strip()


def main():
    
    import argparse
    from sys import stdin, stdout, stderr
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--testmod',
                        action='store_true',
                        help='do doctest.testmod() and exit')
    parser.add_argument('-p', '--prefix',
                        default='TEST')
    parser.add_argument('-o', '--output',
                        type=argparse.FileType('w'),
                        default=stdout)
    parser.add_argument('file',
                        nargs='?',
                        type=argparse.FileType('r'),
                        default=stdin)
    args = parser.parse_args()
    
    if args.testmod:
        import doctest
        doctest.testmod()
        exit()
    
    fin = args.file
    fout = args.output
    name_prefix = args.prefix
    test_num = 1
    for line in fin:
        line = line.decode('utf-8')
        data, comment = split_comment(line)
        if not data:
            continue
        name = '%s%04d' % (name_prefix, test_num)
        fields = [name, data, comment]
        print(','.join(csv_escape(x) for x in fields).encode('utf-8'), file=fout)
        test_num += 1


if __name__ == '__main__':
    main()
