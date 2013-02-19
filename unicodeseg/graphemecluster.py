"""Unicode grapheme cluster breaking

UAX #29: Unicode Text Segmentation (Revision 15)
http://www.unicode.org/reports/tr29/tr29-15.html
"""


from breaking import boundaries, break_units
from codepoint import code_point, code_points
from db import grapheme_cluster_break as _grapheme_cluster_break


__revision__ = '$Rev: 2193 $'

__all__ = [
    'grapheme_cluster_break',
    'grapheme_cluster_breakables',
    'grapheme_cluster_boundaries',
    'grapheme_clusters',
]

Other = 0
CR = 1
LF = 2
Control = 3
Extend = 4
Prepend = 5
SpacingMark = 6
L = 7
V = 8
T = 9
LV = 10
LVT = 11

names = [
    'Other',        # 0
    'CR',           # 1
    'LF',           # 2
    'Control',      # 3
    'Extend',       # 4
    'Prepend',      # 5
    'SpacingMark',  # 6
    'L',            # 7
    'V',            # 8
    'T',            # 9
    'LV',           # 10
    'LVT',          # 11
]

# cf. http://www.unicode.org/Public/5.2.0/ucd/auxiliary/GraphemeBreakTest.html
# 0: not break, 1: break
break_table = [
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
    [1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1],
]

def grapheme_cluster_break(c, index=0):
    
    r"""Return the Grapheme_Cluster_Break property of `c`
    
    `c` must be a single Unicode code point string.
    
    >>> grapheme_cluster_break(u'\x0d')
    'CR'
    >>> grapheme_cluster_break(u'\x0a')
    'LF'
    >>> grapheme_cluster_break(u'a')
    'Other'
    
    If `index` is specified, this function consider `c` as a unicode 
    string and return Grapheme_Cluster_Break property of the code 
    point at c[index].
    
    >>> grapheme_cluster_break(u'a\x0d', 1)
    'CR'
    """
    
    return _grapheme_cluster_break(code_point(c, index))


def grapheme_cluster_breakables(s):
    
    """Iterate grapheme cluster breaking opportunities for every 
    position of `s`
    
    1 for "break" and 0 for "do not break".  The length of iteration 
    will be the same as ``len(s)``.
    
    >>> list(grapheme_cluster_breakables(u'ABC'))
    [1, 1, 1]
    >>> list(grapheme_cluster_breakables(u'\x67\u0308'))
    [1, 0]
    >>> list(grapheme_cluster_breakables(u''))
    []
    """
    
    if not s:
        return
    
    prev_gcbi = 0
    i = 0
    yield 1
    for c in code_points(s):
        gcb = grapheme_cluster_break(c)
        gcbi = names.index(gcb)
        if i > 0:
            breakable = break_table[prev_gcbi][gcbi]
            for j in range(len(c)):
                yield int(j==0 and breakable)
        prev_gcbi = gcbi
        i += len(c)


def grapheme_cluster_boundaries(s, tailor=None):
    
    """Iterate indices of the grapheme cluster boundaries of `s`
    
    This function yields from 0 to the end of the string (== len(s)).
    
    >>> list(grapheme_cluster_boundaries(u'ABC'))
    [0, 1, 2, 3]
    >>> list(grapheme_cluster_boundaries(u'\x67\u0308'))
    [0, 2]
    >>> list(grapheme_cluster_boundaries(u''))
    []
    """
    
    breakables = grapheme_cluster_breakables(s)
    if tailor is not None:
        breakables = tailor(s, breakables)
    return boundaries(breakables)


def grapheme_clusters(s, tailor=None):
    
    r"""Iterate every grapheme cluster token of `s`
    
    Grapheme clusters (both legacy and extended):
    
    >>> list(grapheme_clusters(u'g\u0308'))
    [u'g\u0308']
    >>> list(grapheme_clusters(u'\uac01'))
    [u'\uac01']
    >>> list(grapheme_clusters(u'\u1100\u1161\u11a8'))
    [u'\u1100\u1161\u11a8']
    
    Extended grapheme clusters:
    
    >>> list(grapheme_clusters(u'\u0ba8\u0bbf'))
    [u'\u0ba8\u0bbf']
    >>> list(grapheme_clusters(u'\u0e40\u0e01'))
    [u'\u0e40\u0e01']
    >>> list(grapheme_clusters(u'\u0937\u093f'))
    [u'\u0937\u093f']
    
    Empty string leads the result of empty sequence:
    
    >>> list(grapheme_clusters(u''))
    []
    
    You can customize the default breaking behavior by modifying 
    breakable table so as to fit the specific locale in `tailor` 
    function.  It receives `s` and its default breaking sequence 
    (iterator) as its arguments and returns the sequence of customized 
    breaking opportunities:

    >>> def tailor_grapheme_cluster_breakables(s, breakables):
    ...     
    ...     for i, breakable in enumerate(breakables):
    ...         # don't break between 'c' and 'h'
    ...         if s.endswith('c', 0, i) and s.startswith('h', i):
    ...             yield 0
    ...         else:
    ...             yield breakable
    ... 
    >>> s = u'Czech'
    >>> list(grapheme_clusters(s))
    [u'C', u'z', u'e', u'c', u'h']
    >>> list(grapheme_clusters(s, tailor_grapheme_cluster_breakables))
    [u'C', u'z', u'e', u'ch']
    """
    
    breakables = grapheme_cluster_breakables(s)
    if tailor is not None:
        breakables = tailor(s, breakables)
    return break_units(s, breakables)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
