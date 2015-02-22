``unibreak.py``
===============

::

  usage: unibreak.py [-h] [-e ENCODING] [-l] [-m {c,g,l,s,w}] [-o OUTPUT] [file]

  positional arguments:
    file                  input text file

  optional arguments:
    -h, --help            show this help message and exit
    -e ENCODING, --encoding ENCODING
                          text encoding of the input (UTF-8)
    -l, --legacy          legacy mode (makes sense only with '--mode l')
    -m {c,g,l,s,w}, --mode {c,g,l,s,w}
                          breaking algorithm (w) (c: code points, g: grapheme
                          clusters, s: sentences l: line breaking units, w:
                          words)
    -o OUTPUT, --output OUTPUT
                          leave output to specified file
                          