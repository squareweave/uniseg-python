import os.path
import sqlite3

from codepoint import ord


_dbpath = os.path.join(os.path.dirname(__file__), 'ucd.sqlite3')
_conn = sqlite3.connect(_dbpath)


def grapheme_cluster_break(u):
    
    cur = _conn.cursor()
    cur.execute('select value from GraphemeClusterBreak where cp = ?',
                (ord(u),))
    for value, in cur:
        return str(value)
    return 'Other'


def iter_grapheme_cluster_break_tests():
    
    cur = _conn.cursor()
    cur.execute('select name, pattern, comment from GraphemeClusterBreakTest')
    return iter(cur)


def word_break(u):
    
    cur = _conn.cursor()
    cur.execute('select value from WordBreak where cp = ?',
                (ord(u),))
    for value, in cur:
        return str(value)
    return 'Other'


def iter_word_break_tests():
    
    cur = _conn.cursor()
    cur.execute('select name, pattern, comment from WordBreakTest')
    return iter(cur)


def sentence_break(u):
    
    cur = _conn.cursor()
    cur.execute('select value from SentenceBreak where cp = ?',
                (ord(u),))
    for value, in cur:
        return str(value)
    return 'Other'


def iter_sentence_break_tests():
    
    cur = _conn.cursor()
    cur.execute('select name, pattern, comment from SentenceBreakTest')
    return iter(cur)


def line_break(u):
    
    cur = _conn.cursor()
    cur.execute('select value from LineBreak where cp = ?',
                (ord(u),))
    for value, in cur:
        return str(value)
    return 'Other'


def iter_line_break_tests():
    
    cur = _conn.cursor()
    cur.execute('select name, pattern, comment from LineBreakTest')
    return iter(cur)

