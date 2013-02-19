.PHONY: clean test

PROJ_NAME = unicodeseg

MKDIR = mkdir
MV = mv
RM = rm -v
CURL = curl
PYTHON = python
SQLITE3 = sqlite3

UNICODE_VERSION = 5.2.0
URL_DOWNLOAD = http://www.unicode.org/Public/$(UNICODE_VERSION)/ucd
DIR_DOWNLOAD = data/$(UNICODE_VERSION)
DIR_SRC = unicodeseg
DIR_DIST = dist
UCD_DB = $(DIR_SRC)/ucd.sqlite3

CSV_FILES =\
    csv/GraphemeClusterBreak.csv\
    csv/GraphemeClusterBreakTest.csv\
    csv/WordBreak.csv\
    csv/WordBreakTest.csv\
    csv/SentenceBreak.csv\
    csv/SentenceBreakTest.csv\
    csv/LineBreak.csv\
    csv/LineBreakTest.csv

test: $(UCD_DB)
	$(PYTHON) -m $(DIR_SRC).test

$(UCD_DB): schema.sql $(CSV_FILES)
	-$(SQLITE3) $@ < schema.sql
	$(SQLITE3) -csv $@ ".import csv/GraphemeClusterBreak.csv GraphemeClusterBreak"
	$(SQLITE3) -csv $@ ".import csv/GraphemeClusterBreakTest.csv GraphemeClusterBreakTest"
	$(SQLITE3) -csv $@ ".import csv/WordBreak.csv WordBreak"
	$(SQLITE3) -csv $@ ".import csv/WordBreakTest.csv WordBreakTest"
	$(SQLITE3) -csv $@ ".import csv/SentenceBreak.csv SentenceBreak"
	$(SQLITE3) -csv $@ ".import csv/SentenceBreakTest.csv SentenceBreakTest"
	$(SQLITE3) -csv $@ ".import csv/LineBreak.csv LineBreak"
	$(SQLITE3) -csv $@ ".import csv/LineBreakTest.csv LineBreakTest"
	$(SQLITE3) $@ "vacuum"

clean:
	-$(RM) $(DIR_SRC)/*.pyc
	-$(RM) $(CSV_FILES)

cleanall: clean
	-$(RM) $(UCD_DB)
	-$(RM) -r $(DIR_DOWNLOAD)
	-$(RM) MANIFEST
	-$(RM) -r dist
	-$(RM) -r data
	-$(RM) -r build

sdist:
	$(PYTHON) setup.py sdist -d $(DIR_DIST) --formats=zip

archive:
	-$(MKDIR) -p $(DIR_DIST)
	svn up
	svn export . $(PROJ_NAME)-r`svnversion`
	zip -r -m $(PROJ_NAME)-r`svnversion`.zip $(PROJ_NAME)-r`svnversion`
	$(MV) $(PROJ_NAME)-r`svnversion`.zip $(DIR_DIST)

install:
	$(PYTHON) setup.py install --home=$(HOME)

csv/GraphemeClusterBreak.csv: $(DIR_DOWNLOAD)/auxiliary/GraphemeBreakProperty.txt
	$(PYTHON) tools/prop2csv.py -o $@ $<

csv/GraphemeClusterBreakTest.csv: $(DIR_DOWNLOAD)/auxiliary/GraphemeBreakTest.txt
	$(PYTHON) tools/test2csv.py -p GB -o $@ $<

csv/WordBreak.csv: $(DIR_DOWNLOAD)/auxiliary/WordBreakProperty.txt
	$(PYTHON) tools/prop2csv.py -o $@ $<

csv/WordBreakTest.csv: $(DIR_DOWNLOAD)/auxiliary/WordBreakTest.txt
	$(PYTHON) tools/test2csv.py -p WB -o $@ $<

csv/SentenceBreak.csv: $(DIR_DOWNLOAD)/auxiliary/SentenceBreakProperty.txt
	$(PYTHON) tools/prop2csv.py -o $@ $^

csv/SentenceBreakTest.csv: $(DIR_DOWNLOAD)/auxiliary/SentenceBreakTest.txt
	$(PYTHON) tools/test2csv.py -p SB -o $@ $<

csv/LineBreak.csv: $(DIR_DOWNLOAD)/LineBreak.txt
	$(PYTHON) tools/prop2csv.py -o $@ $^

csv/LineBreakTest.csv: $(DIR_DOWNLOAD)/auxiliary/LineBreakTest.txt
	$(PYTHON) tools/test2csv.py -p LB -o $@ $<

# Use 'mkdir -p' instead of --create-dirs option of curl because it 
# doesn't work well with path names with '/' on Windows.
$(DIR_DOWNLOAD)/%:
	-$(MKDIR) -p $(dir $@)
	$(CURL) -o $@ $(subst $(DIR_DOWNLOAD),$(URL_DOWNLOAD),$@)
