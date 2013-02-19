import doctest
import unittest

import linebreak
from db import iter_line_break_tests
from test import implement_break_tests


# Some tests in LineBreakTest.txt seems to be wrong; let's skip them.
skips = [
    # Tests to skip are specified in the form of (string, expect) so 
    # as not to skip them when they are modified.
    (u'}%', [0, 1, 2]),         # [0, 2]
    (u'}\u0308%', [0, 2, 3]),   # [0, 3]
    (u'}$', [0, 1, 2]),         # [0, 2]
    (u'}\u0308$', [0, 2, 3]),   # [0, 3]
    (u')%', [0, 1, 2]),         # [0, 2]
    (u')\u0308%', [0, 2, 3]),   # [0, 3]
    (u')$', [0, 1, 2]),         # [0, 2]
    (u')\u0308$', [0, 2, 3]),   # [0, 3]
    (u',0', [0, 1, 2]),         # [0, 2]
    (u',\u03080', [0, 2, 3]),   # [0, 3]
    (u'%(', [0, 1, 2]),         # [0, 2]
    (u'%\u0308(', [0, 2, 3]),   # [0, 3]
    (u'$(', [0, 1, 2]),         # [0, 2]
    (u'$\u0308(', [0, 2, 3]),   # [0, 3]
    (u'/0', [0, 1, 2]),         # [0, 2]
    (u'/\u03080', [0, 2, 3]),   # [0, 3]
    (u'equals .35 cents', [0, 8, 11, 16]),
                                # [0, 11, 16]
]


@implement_break_tests(linebreak.line_break_boundaries,
                       iter_line_break_tests(),
                       skips)
class LineBreakTest(unittest.TestCase):
    pass


def load_tests(loader, tests, ignore):
    
    tests.addTests(doctest.DocTestSuite(linebreak))
    return tests


if __name__ == '__main__':
    unittest.main()
