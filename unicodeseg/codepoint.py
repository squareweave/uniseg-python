"""Unicode codepoint

Copyright (c) 2012 Masaaki Shibata <mshibata@emptypage.jp>

Permission is hereby granted, free of charge, to any person obtaining 
a copy of this software and associated documentation files (the 
"Software"), to deal in the Software without restriction, including 
without limitation the rights to use, copy, modify, merge, publish, 
distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to 
the following conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__revision__ = '$Rev: 2191 $'


import re
from sys import maxunicode
from __builtin__ import ord as _ord, unichr as _unichr


__all__ = [
    'ord',
    'unichr',
    'code_points'
]

is_narrow_build = (maxunicode < 0x10000)


if is_narrow_build:
    # narrow unicode build
    
    def ord_impl(c, index):
        
        if isinstance(c, str):
            return _ord(c[index or 0])
        if not isinstance(c, unicode):
            raise TypeError('must be unicode, not %s' % type(c).__name__)
        i = index or 0
        len_s = len(c)-i
        if len_s:
            value = hi = _ord(c[i])
            i += 1
            if 0xd800 <= hi < 0xdc00:
                if len_s > 1:
                    lo = _ord(c[i])
                    i += 1
                    if 0xdc00 <= lo < 0xe000:
                        value = (hi-0xd800)*0x400+(lo-0xdc00)+0x10000
            if index is not None or i == len_s:
                return value
        raise TypeError('need a single Unicode code point as parameter')
    
    def unichr_impl(cp):
        
        if not isinstance(cp, int):
            raise TypeError('must be int, not %s' % type(c).__name__)
        if cp < 0x10000:
            return _unichr(cp)
        hi, lo = divmod(cp-0x10000, 0x400)
        hi += 0xd800
        lo += 0xdc00
        if 0xd800 <= hi < 0xdc00 and 0xdc00 <= lo < 0xe000:
            return _unichr(hi)+_unichr(lo)
        raise ValueError('illeagal code point')
    
    rx_codepoints = re.compile(ur'[\ud800-\udbff][\udc00-\udfff]|.',
                               re.DOTALL)
    
    def code_point_impl(s, index):
        
        m = rx_codepoints.match(s, index)
        return m.group()
    
    def code_points_impl(s):
        
        return rx_codepoints.findall(s)

else:
    # wide unicode build
    
    def ord_impl(c, index):
        return _ord(c[index])
    
    def unichr_impl(cp):
        return _unichr(cp)
    
    def code_point_impl(s, index):
        return s[index]
    
    def code_points_impl(s):
        return list(s)


def ord(c, index=None):
    
    r"""Return the integer value of the Unicode code point `c`
    
    NOTE: Some Unicode code points may be expressed with a couple of 
    other code points ("surrogate pair").  This function treats 
    surrogate pairs as representations of original code points; e.g. 
    ``ord(u'\ud842\udf9f')`` returns 134047 (0x20b9f).  ``u'\ud842\udf9f'`` is 
    a surrogate pair expression which means ``u'\U00020b9f'``:
    
    >>> ord(u'a')
    97
    >>> ord(u'\u3042')
    12354
    >>> ord(u'\U00020b9f')
    134047
    >>> ord(u'\ud842\udf9f')
    134047
    >>> ord(u'abc')
    Traceback (most recent call last):
      ...
    TypeError: need a single Unicode code point as parameter
    
    It returns the result of built-in ord() when `c` is a single str 
    object for compatibility:
    
    >>> ord('a')
    97
    
    When `index` argument is specified (to not None), this function 
    treats `c` as a Unicode string and returns integer value of code 
    point at c[index] (or may be c[index:index+2]):
    
    >>> ord(u'hello', 0)
    104
    >>> ord(u'hello', 1)
    101
    >>> ord(u'a\U00020b9f', 1)
    134047
    """
    
    return ord_impl(c, index)


def unichr(cp):
    
    r"""Return the unicode object represents the code point integer `cp`
    
    >>> unichr(0x61)
    u'a'
    
    Notice that some Unicode code points may be expressed with a 
    couple of other code points ("surrogate pair") in narrow-build 
    Python.  In those cases, this function will return a unicode 
    object of which length is more than one; e.g. ``unichr(0x20b9f)`` 
    returns ``u'\U00020b9f'`` while built-in ``unichr()`` may raise 
    ValueError.
    
    >>> unichr(0x20b9f)
    u'\U00020b9f'
    """
    
    return unichr_impl(cp)


def code_point(s, index=0):
    
    r"""Return code point at s[index]
    
    >>> code_point(u'ABC')
    u'A'
    >>> code_point(u'ABC', 1)
    u'B'
    >>> code_point(u'\U00020b9f\u3042')
    u'\U00020b9f'
    >>> code_point(u'\U00020b9f\u3042', 2)
    u'\u3042'
    """
    
    return code_point_impl(s, index)


def code_points(s):
    
    """Iterate every Unicode code points of the unicode string `s`
    
    >>> s = u'hello'
    >>> list(code_points(s))
    [u'h', u'e', u'l', u'l', u'o']
    
    The number of iteration may differ from the len(s), because some 
    code points may be represented as a couple of other code points 
    ("surrogate pair") in narrow-build Python.
    
    >>> s = u'abc\U00020b9f\u3042'
    >>> list(code_points(s))
    [u'a', u'b', u'c', u'\U00020b9f', u'\u3042']
    """
    
    return code_points_impl(s)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
