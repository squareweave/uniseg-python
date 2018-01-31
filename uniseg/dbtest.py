#!/usr/bin/env python


from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import sqlite3
import threading
import time
import unittest

from .db import sentence_break


class DatabaseTests(unittest.TestCase):
    def test_multithreaded_access(self):
        """
        Test that this library can be accessed from multiple threads without
        issue.
        """

        failures = []

        def access_db():
            try:
                sentence_break('a')
                time.sleep(0.2)
                sentence_break('b')
            except sqlite3.ProgrammingError as e:
                failures.append(e)

        t1 = threading.Thread(target=access_db)
        t2 = threading.Thread(target=access_db)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        if len(failures) != 0:
            raise failures[0]


if __name__ == '__main__':
    unittest.main()
