#!/usr/bin/env python


from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import re


rx_csv_special_characters = re.compile(r'[,"\n]')


def split_record(line, separator=';'):
    
    """Split `line` to a list of fields and a comment
    
    >>> split_record('0000..0009 ; XXX # some value')
    (['0000..0009', 'XXX'], 'some value')
    
    """
    
    try:
        i = line.index('#')
    except ValueError:
        record_line = line
        comment = ''
    else:
        record_line = line[:i]
        comment = line[i+1:]
    
    fields = [x.strip() for x in record_line.split(separator)]
    comment = comment.strip()
    
    return fields, comment


def codepoint_range(data, separator='..'):
    
    """Return the list of code point integers described in `data`
    
    >>> list(codepoint_range('000D'))
    [13]
    >>> list(codepoint_range('0000..0009'))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    """
    
    if separator in data:
        start, end = data.split(separator)
    else:
        start = end = data
    start = int(start, 16)
    end = int(end, 16)
    return range(start, end+1)


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
    
    s = str(value)
    if rx_csv_special_characters.search(s):
        s = '"%s"' % s.replace('"', '""')
    
    return s


def main():
    
    import argparse
    from sys import stdin, stdout, stderr
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--testmod',
                        action='store_true',
                        help='do doctest.testmod() and exit')
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
    for line in fin:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        fields, comment = split_record(line)
        cprange = fields[0]
        for cp in codepoint_range(cprange):
            fields[0] = cp
            print(','.join(csv_escape(x) for x in fields), file=fout)


if __name__ == '__main__':
    main()
