#!/usr/bin/env python


import doctest
import unittest

import wrap


def load_tests(loader, tests, ignore):
    
    tests.addTests(doctest.DocTestSuite(wrap))
    return tests


if __name__ == '__main__':
    unittest.main()
