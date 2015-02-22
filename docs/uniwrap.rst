``uniwrap.py``
==============

::

  usage: uniwrap.py [-h] [-e ENCODING] [-r] [-t TAB_WIDTH] [-l] [-o OUTPUT]
                    [-w WRAP_WIDTH] [-c]
                    [file]

  positional arguments:
    file                  input file

  optional arguments:
    -h, --help            show this help message and exit
    -e ENCODING, --encoding ENCODING
                          file encoding (UTF-8)
    -r, --ruler           show ruler
    -t TAB_WIDTH, --tab-width TAB_WIDTH
                          tab width (8)
    -l, --legacy          treat ambiguous-width letters as wide
    -o OUTPUT, --output OUTPUT
                          leave output to specified file
    -w WRAP_WIDTH, --wrap-width WRAP_WIDTH
                          wrap width (60)
    -c, --char-wrap       wrap on grapheme boundaries instead of line break
                          boundaries
