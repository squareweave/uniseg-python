"""Text wrapping
"""


from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

from unicodedata import east_asian_width

from .codepoint import ord, code_point, code_points
from .graphemecluster import grapheme_clusters, grapheme_cluster_boundaries
from .linebreak import line_break_boundaries


__all__ = ['TextWrapper', 'TTWrapper']


class TextWrapper(object):
    
    """TextWrapper base class. """
    
    wrap_width = None
    tab_width = 0
    char_wrap = False
    
    def list_text_extents(self, s):
        
        """Return a list of logical widths from start of the string to 
        each character.
        
        (This is a place holder method to be implemented.)
        
        """
        
        raise NotImplemented
    
    def iter_wrap_boundaries(self, s):
        
        """Iterate indices of line breaking boundaries of a string. """
        
        if not s:
            return
        
        wrap_width = self.wrap_width
        if wrap_width is None:
            yield len(s)
            return
        
        if self.char_wrap:
            iter_boundaries = grapheme_cluster_boundaries
        else:
            iter_boundaries = line_break_boundaries
        
        widths = self.list_text_extents(s)
        if wrap_width < 1:
            wrap_width = 1
        
        total_width = 0
        prev_breakpoint = 0
        for breakpoint in iter_boundaries(s):
            if breakpoint > 0:
                width = widths[breakpoint-1] - total_width
                if prev_breakpoint and width > wrap_width:
                    yield prev_breakpoint
                    total_width = widths[prev_breakpoint-1]
            prev_breakpoint = breakpoint
        yield breakpoint
    
    def wrap(self, s):
        
        """Iterate strings of wrapped lines of s. """
        
        i = 0
        for j in self.iter_wrap_boundaries(s):
            yield s[i:j]
            i = j


class TTWrapper(TextWrapper):
    
    """Fixed-width TextWrapper class. """
    
    tab_width = 8
    legacy = False
    expand_tabs = False
    justify = False
    
    def list_text_extents(self, s):
        
        """Return a list of logical widths from start of the string to 
        each character.
        
        """
        
        tab_width = self.tab_width
        legacy = self.legacy
        
        widths = []
        width = 0
        prev_boundary = 0
        for boundary in grapheme_cluster_boundaries(s):
            if boundary:
                cp = code_points(s[prev_boundary:boundary])[0]
                if cp == '\t' and tab_width:
                    width = (width // tab_width + 1) * tab_width
                    widths.append(width)
                else:
                    eaw = east_asian_width(cp)
                    if eaw == 'W' or eaw == 'F' or (eaw == 'A' and legacy):
                        width += 2
                    else:
                        width += 1
                    for __ in range(prev_boundary, boundary):
                        widths.append(width)
            prev_boundary = boundary
        return widths
    
    def expandtabs(self, s):
        
        """Fill tabs with spaces. """
        
        widths = self.list_text_extents(s)
        L = []
        prev_width = 0
        for c, width in zip(s, widths):
            if c == '\t':
                c = ' ' * (width - prev_width)
            L.append(c)
            prev_width = width
        return ''.join(L)
    
    def justify_text(self, s):
        
        """Justify each line with padding spaces. """
        
        s = s.rstrip(' ')
        
        if ' ' not in s:
            return s
        
        widths = self.list_text_extents(s)
        if not widths:
            return s
        
        n_additional_spaces = self.wrap_width - widths[-1]
        if n_additional_spaces == 0:
            return s
        
        L = []
        tokens = s.split(' ')
        nspaces = len(tokens) - 1 + n_additional_spaces
        prev_x = 0
        for i, tok in enumerate(tokens):
            if i > 0:
                x = nspaces * i // (len(tokens)-1)
                L.append(' ' * (x - prev_x))
                prev_x = x
            L.append(tok)
            first = False
        return ''.join(L)
    
    def wrap(self, s):
        
        """Iterate strings of wrapped lines of s. """
        
        if self.expand_tabs:
            def _line(line):
                return self.expandtabs(line)
        else:
            def _line(line):
                return line
        
        next = iter(TextWrapper.wrap(self, s)).__next__
        line = next()
        while 1:
            try:
                next_line = next()
            except StopIteration:
                yield _line(line)
                break
            if self.justify:
                line = self.justify_text(line)
            yield _line(line)
            line = next_line


class TTWrapHandler(object):
    
    """Fixed-width text wrapping handler """
    
    tab_width = 8
    legacy = False
    expand_tabs = False
    justify = False
    
    def text_extents(self, s):
        
        """Return a list of logical widths from start of the string to 
        each character
        
        >>> 
        
        """
        
        tab_width = self.tab_width
        legacy = self.legacy
        
        widths = []
        width = 0
        prev_boundary = 0
        for boundary in grapheme_cluster_boundaries(s):
            if boundary:
                cp = code_points(s[prev_boundary:boundary])[0]
                if cp == '\t' and tab_width:
                    width = (width // tab_width + 1) * tab_width
                    widths.append(width)
                else:
                    eaw = east_asian_width(cp)
                    if eaw == 'W' or eaw == 'F' or (eaw == 'A' and legacy):
                        width += 2
                    else:
                        width += 1
                    for __ in range(prev_boundary, boundary):
                        widths.append(width)
            prev_boundary = boundary
        return widths
    
    def expandtabs(self, s):
        
        """Fill tabs with spaces. """
        
        widths = self.list_text_extents(s)
        L = []
        prev_width = 0
        for c, width in zip(s, widths):
            if c == '\t':
                c = ' ' * (width - prev_width)
            L.append(c)
            prev_width = width
        return ''.join(L)
    
    def justify_text(self, s):
        
        """Justify each line with padding spaces. """
        
        s = s.rstrip(' ')
        
        if ' ' not in s:
            return s
        
        widths = self.list_text_extents(s)
        if not widths:
            return s
        
        n_additional_spaces = self.wrap_width - widths[-1]
        if n_additional_spaces == 0:
            return s
        
        L = []
        tokens = s.split(' ')
        nspaces = len(tokens) - 1 + n_additional_spaces
        prev_x = 0
        for i, tok in enumerate(tokens):
            if i > 0:
                x = nspaces * i // (len(tokens)-1)
                L.append(' ' * (x - prev_x))
                prev_x = x
            L.append(tok)
            first = False
        return ''.join(L)
    
    def wrap(self, s):
        
        """Iterate strings of wrapped lines of s. """
        
        if self.expand_tabs:
            def _line(line):
                return self.expandtabs(line)
        else:
            def _line(line):
                return line
        
        next = iter(TextWrapper.wrap(self, s)).next
        line = next()
        while 1:
            try:
                next_line = next()
            except StopIteration:
                yield _line(line)
                break
            if self.justify:
                line = self.justify_text(line)
            yield _line(line)
            line = next_line


def tt_width(s, index=0, legacy=False):
    
    """Return logical width of the grapheme cluster at `s[index]` on 
    fixed-width typography
    
    Return value will be 1 (halfwidth) or 2 (fullwidth).
    
    Generally, the width of a grapheme cluster is determined by its 
    leading code point.
    
    >>> tt_width('A')
    1
    >>> tt_width('\u8240')
    2
    >>> tt_width('\x67\u0308')
    1
    
    If `legacy` is specified to True, some characters such as greek 
    alphabets are treated as they have fullwidth as well as 
    ideographics does.
    
    >>> tt_width('\u03b1')
    1
    >>> tt_width('\u03b1', legacy=True)
    2
    """
    
    c = code_point(s, index)
    eaw = east_asian_width(c)
    if eaw in ('W', 'F') or (eaw == 'A' and legacy):
        return 2
    return 1


def tt_text_extents(s, legacy=False):
    
    """Return a list of logical widths from start of the string to 
    each character on fixed-width typography
    
    >>> tt_text_extents('')
    []
    >>> tt_text_extents('abc')
    [1, 2, 3]
    >>> tt_text_extents('\u3042\u3044\u3046')
    [2, 4, 6]
    
    The meaning of `legacy` is the same as that of `tt_width()`.
    """
    
    widths = []
    total_width = 0
    for gc in grapheme_clusters(s):
        total_width += tt_width(gc, legacy)
        widths.extend(total_width for __ in gc)
    return widths


if __name__ == '__main__':
    import doctest
    doctest.testmod()
