.PHONY: clean test upload docs

PROJ_NAME = uniseg

MKDIR = "mkdir"
MV = mv
RM = rm -v
CURL = curl --compressed
PYTHON = python
SQLITE3 = sqlite3
PIP = pip
SPHINX_BUILD = sphinx-build

UNICODE_VERSION = 6.2.0
URL_DOWNLOAD = http://www.unicode.org/Public/$(UNICODE_VERSION)/ucd
DIR_DOWNLOAD = data/$(UNICODE_VERSION)
DIR_SRC = uniseg
DIR_DIST = dist
UCD_DB = $(DIR_SRC)/ucd.sqlite3
DIR_DOCS = docs
DIR_DOCS_BUILD = docs/_build

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
	-$(RM) -r csv

cleanall: clean cleandocs
	-$(RM) $(UCD_DB)
	-$(RM) -r $(DIR_DOWNLOAD)
	-$(RM) MANIFEST
	-$(RM) -r dist
	-$(RM) -r data
	-$(RM) -r build

sdist:
	$(PYTHON) setup.py sdist -d $(DIR_DIST) --formats=zip

wheel:
	$(PYTHON) setup.py bdist_wheel -d $(DIR_DIST) --universal

release:
	$(PYTHON) setup.py \
	register \
	sdist -d $(DIR_DIST) --formats=zip \
	bdist_wheel -d $(DIR_DIST) --universal \
	upload

install:
	$(PIP) install -e .

docs:
	$(SPHINX_BUILD) -b html $(DIR_DOCS) $(DIR_DOCS_BUILD)/html

cleandocs:
	-$(RM) -r $(DIR_DOCS_BUILD)

csv/GraphemeClusterBreak.csv: $(DIR_DOWNLOAD)/auxiliary/GraphemeBreakProperty.txt
	-$(MKDIR) -p $(dir $@)
	$(PYTHON) tools/prop2csv.py -o $@ $<

csv/GraphemeClusterBreakTest.csv: $(DIR_DOWNLOAD)/auxiliary/GraphemeBreakTest.txt
	-$(MKDIR) -p $(dir $@)
	$(PYTHON) tools/test2csv.py -p GB -o $@ $<

csv/WordBreak.csv: $(DIR_DOWNLOAD)/auxiliary/WordBreakProperty.txt
	-$(MKDIR) -p $(dir $@)
	$(PYTHON) tools/prop2csv.py -o $@ $<

csv/WordBreakTest.csv: $(DIR_DOWNLOAD)/auxiliary/WordBreakTest.txt
	-$(MKDIR) -p $(dir $@)
	$(PYTHON) tools/test2csv.py -p WB -o $@ $<

csv/SentenceBreak.csv: $(DIR_DOWNLOAD)/auxiliary/SentenceBreakProperty.txt
	-$(MKDIR) -p $(dir $@)
	$(PYTHON) tools/prop2csv.py -o $@ $^

csv/SentenceBreakTest.csv: $(DIR_DOWNLOAD)/auxiliary/SentenceBreakTest.txt
	-$(MKDIR) -p $(dir $@)
	$(PYTHON) tools/test2csv.py -p SB -o $@ $<

csv/LineBreak.csv: $(DIR_DOWNLOAD)/LineBreak.txt
	-$(MKDIR) -p $(dir $@)
	$(PYTHON) tools/prop2csv.py -o $@ $^

csv/LineBreakTest.csv: $(DIR_DOWNLOAD)/auxiliary/LineBreakTest.txt
	-$(MKDIR) -p $(dir $@)
	$(PYTHON) tools/test2csv.py -p LB -o $@ $<

# Use 'mkdir -p' instead of --create-dirs option of curl because it 
# doesn't work well with path names with '/' on Windows.
$(DIR_DOWNLOAD)/%:
	-$(MKDIR) -p $(dir $@)
	$(CURL) -o $@ $(subst $(DIR_DOWNLOAD),$(URL_DOWNLOAD),$@)
