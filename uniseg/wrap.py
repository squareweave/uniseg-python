"""unicode-aware text wrapping """


from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import re
from unicodedata import east_asian_width

from .codepoint import ord, code_point, code_points
from .graphemecluster import grapheme_clusters, grapheme_cluster_boundaries
from .linebreak import line_break_boundaries


__all__ = ['Wrapper',
           'TTFormatter', 'tt_width', 'tt_text_extents', 'tt_wrap']


### Wrap

class Wrapper(object):
    
    """text wrapper class """
    
    def __init__(self, formatter=None, char_wrap=False):
        
        """init instance """

        self._formatter = formatter
        self._char_wrap = char_wrap
        self.reset()

    def _get_formatter(self):
        return self._formatter
    def _set_formatter(self, value):
        self._formatter = value
    formatter = property(
        _get_formatter, _set_formatter,
        doc="""formatter instance """)

    def _get_char_wrap(self):
        return self._char_wrap
    def _set_char_wrap(self, value):
        self._char_wrap = value
    char_wrap = property(
        _get_char_wrap, _set_char_wrap,
        doc="""specify string should be wrapped in grapheme cluster 
        boundaries not in line break boundaries """)

    def reset(self):
        
        """reset all states """

        if self._formatter is not None:
            self._formatter.reset()

    @staticmethod
    def _partial_extents(extents, start, stop=None):

        """(internal) return partial extents of `extents[start:end]` """
        
        if stop is None:
            stop = len(extents)
        extent_offset = extents[start-1] if start > 0 else 0
        return [extents[x] - extent_offset for x in range(start, stop)]

    def wrap(self, s, cur=0, offset=0, formatter=None, char_wrap=None):
        
        """wrap string `s` with given formatter and call appropriate 
        formatter methods

        `s`:
            string to be wrapped.
        `cur`:
            starting position of the string in logical length.
        `offset`:
            left-side offset of wrapping string in logical length.
            NOTE: This parameter is only used for calculating tab-stopping 
            positions for now.
        """

        if formatter is None:
            formatter = self.formatter
        if char_wrap is None:
            char_wrap = self.char_wrap
        _partial_extents = self._partial_extents

        iter_boundaries = line_break_boundaries
        if char_wrap:
            iter_boundaries = grapheme_cluster_boundaries
        
        for para in s.splitlines(True):
            for field in re.split('(\\t)', para):
                if field == '\t':
                    tw = formatter.tab_width
                    field_extents = [tw - (offset + cur) % tw]
                else:
                    field_extents = formatter.text_extents(field)
                prev_boundary = 0
                prev_extent = 0
                breakpoint = 0
                for boundary in iter_boundaries(field):
                    extent = field_extents[boundary-1]
                    w = extent - prev_extent
                    if cur + w > formatter.wrap_width:
                        line = field[breakpoint:prev_boundary]
                        line_extents = _partial_extents(field_extents,
                                                        breakpoint,
                                                        prev_boundary)
                        formatter.handle_text(line, line_extents)
                        formatter.handle_new_line()
                        cur = 0
                        breakpoint = prev_boundary
                    cur += w
                    prev_boundary = boundary
                    prev_extent = extent
                line = field[breakpoint:]
                line_extents = _partial_extents(field_extents, breakpoint)
                formatter.handle_text(line, line_extents)
            formatter.handle_new_line()
            cur = 0


### TT

class TTFormatter(object):
    
    """fixed-width wrapping formatter """

    def __init__(self, wrap_width,
                 tab_width=8, tab_char=' ', ambiguous_as_wide=False):
        
        """init instance """

        self.wrap_width = wrap_width
        self.tab_width = tab_width
        self.ambiguous_as_wide = ambiguous_as_wide
        self.tab_char = tab_char

        self._lines = ['']

    def _get_ambiguous_as_wide(self):
        return self._ambiguous_as_wide
    def _set_ambiguous_as_wide(self, value):
        self._ambiguous_as_wide = value
    ambiguous_as_wide = property(
        _get_ambiguous_as_wide, _set_ambiguous_as_wide,
        doc="""treat code points with its East_Easian_Width property is 
        'A' as those with 'W'; having double width as alpha-numerics """)
    
    def _get_tab_char(self):
        return self._tab_char
    def _set_tab_char(self, value):
        if (east_asian_width(value) not in ('N', 'Na', 'H')):
            raise ValueError("""only a narrow code point is available 
                             for tab_char""")
        self._tab_char = value
    tab_char = property(
        _get_tab_char, _set_tab_char,
        doc="""character to fill tab spaces with """)
    
    def _get_wrap_width(self):
        return self._wrap_width
    def _set_wrap_width(self, value):
        self._wrap_width = value
    wrap_width = property(
        _get_wrap_width, _set_wrap_width,
        doc="""wrapping width """)

    def _get_tab_width(self):
        return self._tab_width
    def _set_tab_width(self, value):
        self._tab_width = value
    tab_width = property(
        _get_tab_width, _set_tab_width,
        doc="""forwarding size of tabs """)

    def reset(self):
        
        """reset all states of the formatter """
        
        del self._lines[:]

    def text_extents(self, s):
        
        """return a list of the logical lengths from start of the 
        string to each characters in `s` """

        return tt_text_extents(s, self.ambiguous_as_wide)

    def handle_text(self, text, extents):
        
        """handler method which is called when a text should be put 
        on the current position """

        if text == '\t':
            text = self.tab_char * extents[0]
        self._lines[-1] += text

    def handle_new_line(self):

        """handler method which is called when the current line is over 
        and a new line begins """

        self._lines.append('')
    
    def lines(self):

        """iterate every wrapped line strings """

        return iter(self._lines)


def tt_width(s, index=0, ambiguous_as_wide=False):
    
    """return logical width of the grapheme cluster at `s[index]` on 
    fixed-width typography
    
    Return value will be 1 (halfwidth) or 2 (fullwidth).
    
    Generally, the width of a grapheme cluster is determined by its 
    leading code point.
    
    >>> tt_width('A')
    1
    >>> tt_width('\\u8240')  # U+8240: CJK UNIFIED IDEOGRAPH-8240
    2
    >>> tt_width('g\\u0308') # U+0308: COMBINING DIAERESIS
    1
    >>> tt_width('\\U00029e3d')
    2
    
    If `ambiguous_as_wide` is specified to True, some characters such 
    as greek alphabets are treated as they have fullwidth as well as 
    ideographics does.
    
    >>> tt_width('\\u03b1')  # U+03B1: GREEK SMALL LETTER ALPHA
    1
    >>> tt_width('\\u03b1', ambiguous_as_wide=True)
    2
    """
    
    cp = code_point(s, index)
    eaw = east_asian_width(cp)
    if eaw in ('W', 'F') or (eaw == 'A' and ambiguous_as_wide):
        return 2
    return 1


def tt_text_extents(s, ambiguous_as_wide=False):
    
    """return a list of logical widths from the start of `s` to 
    each character (*!= code point*) on fixed-width typography
    
    >>> tt_text_extents('')
    []
    >>> tt_text_extents('abc')
    [1, 2, 3]
    >>> tt_text_extents('\\u3042\\u3044\\u3046')
    [2, 4, 6]
    >>> import sys
    >>> s = '\\U00029e3d'    # test a code point out of BMP.
    >>> actual = tt_text_extents(s)
    >>> expect = [2] if sys.maxunicode > 0xffff else [2, 2]
    >>> len(s) == len(expect)
    True
    >>> actual == expect
    True
    
    The meaning of `ambiguous_as_wide` is the same as that of `tt_width()`.
    """
    
    widths = []
    total_width = 0
    for gc in grapheme_clusters(s):
        total_width += tt_width(gc, ambiguous_as_wide)
        widths.extend(total_width for __ in gc)
    return widths


def tt_wrap(s, wrap_width, tab_width=8, cur=0, offset=0,
            ambiguous_as_wide=False, char_wrap=False):
    
    wrapper = Wrapper()
    formatter = TTFormatter(wrap_width, tab_width,
                            ambiguous_as_wide=ambiguous_as_wide)
    wrapper.wrap(s, cur, offset, formatter, char_wrap)
    return formatter.lines()


### Main

if __name__ == '__main__':
    import doctest
    doctest.testmod()
