# vim: set shiftwidth=4 tabstop=4 noexpandtab:
CURDIR	?= $(shell pwd)
ENVDIR	?= $(CURDIR)/env
PROJECT	?= $(notdir $(CURDIR))
PYTHON3_PATH ?= "$(shell which python3)"
DICS_DIR ?= $(CURDIR)/jgrampro/dic

ECHO    ?= echo
WGET    ?= wget
TAR     ?= tar
CP      ?= cp
RM      ?= rm -f
PIP		:= "$(ENVDIR)/bin/pip"
PYTHON  := "$(ENVDIR)/bin/python"
FIND    ?= find
PYTEST  := py.test

.PHONY: help setdevelop test version

help:
	@$(ECHO) "Make sure you have virtualenv installed: pip install virtualenv"
	@$(ECHO) ""
	@$(ECHO) "Use any of these targets"
	@$(ECHO) "============================================================"
	@$(ECHO) "Useful targets targets:"
	@$(ECHO) " setdevelop  - Set the environment to begin to work"
	@$(ECHO) " test        - Install test requirements and run the tests"
	@$(ECHO) " version     - Change header of every file to reflect"
	@$(ECHO) "               current year and provided version"
	@$(ECHO) "------------------------------------------------------------"
	@$(ECHO) "Housekeeping targets:"
	@$(ECHO) " clean            - Remove intermediate, and generated files"
	@$(ECHO) " maintainer-clean - As clean, but removing the env also."
	@$(ECHO) "============================================================"
	@$(ECHO) ""

setdevelop:
	virtualenv -p $(PYTHON3_PATH) ./env
	$(PIP) -q install -r "$(CURDIR)/requirements/requirements_test.txt"
	@$(ECHO) "Getting and patching dictionary files..."
#
#   Getting dictionaries	
	@$(WGET) -q --show-progress -P $(CURDIR)/temp https://googledrive.com/host/\
	0B_NO47cRQb6_fkJ1Z25MMHdUTDBqNHhsNU1JNzdXMGwxdF9qd3k3QWk3em5DRDJGREhNNVk/\
	mecab-ipadic-2.7.0-20070801_bin.tar.gz
	@$(WGET) -q --show-progress -P $(CURDIR)/temp https://googledrive.com/host/\
	0B_NO47cRQb6_fkJ1Z25MMHdUTDBqNHhsNU1JNzdXMGwxdF9qd3k3QWk3em5DRDJGREhNNVk/\
	mecab-jumandic-7.0-20130310_bin.tar.gz
	@$(WGET) -q --show-progress -P $(CURDIR)/temp https://googledrive.com/host/\
	0B_NO47cRQb6_fkJ1Z25MMHdUTDBqNHhsNU1JNzdXMGwxdF9qd3k3QWk3em5DRDJGREhNNVk/\
	unidic-mecab-2.1.2_bin.tar.gz
#
#	Extracting dictionaries
	@$(TAR) -zxf $(CURDIR)/temp/mecab-ipadic-2.7.0-20070801_bin.tar.gz \
	-C $(CURDIR)/jgrampro/dic/
	@$(TAR) -zxf $(CURDIR)/temp/mecab-jumandic-7.0-20130310_bin.tar.gz \
	-C $(CURDIR)/jgrampro/dic/
	@$(TAR) -zxf $(CURDIR)/temp/unidic-mecab-2.1.2_bin.tar.gz \
	-C $(CURDIR)/jgrampro/dic/
#
#	Deleting temp directory
	@$(RM) -r $(CURDIR)/temp/
#
#   Patching dictionaries
	@$(CP) $(CURDIR)/jgrampro/dic/custom_files/ipadic/dicrc \
	$(CURDIR)/jgrampro/dic/ipadic/
	@$(CP) $(CURDIR)/jgrampro/dic/custom_files/jumandic/dicrc \
	$(CURDIR)/jgrampro/dic/jumandic/
	@$(CP) $(CURDIR)/jgrampro/dic/custom_files/unidic/dicrc \
	$(CURDIR)/jgrampro/dic/unidic/
#
	@$(ECHO) "Done"
	@$(ECHO) "/////////////////////////////////"
	@$(ECHO) "To activate the environment type:"
	@$(ECHO) "source env/bin/activate"
	@$(PYTHON) ./setup.py develop

test: 
	@$(PYTEST) -vv tests

version:
	./devtools/new_version_bump.sh

.PHONY: clean maintainer-clean maintainerclean
clean:
	@$(ECHO) "Removing intermediate files."
	- $(FIND) . -name '*.py[co]' -delete
	@$(ECHO) "Removing cached files and reports."
	- $(FIND) . -name '__pycache__' -delete
	- $(RM) -r dist build *.egg *.egg-info

maintainer-clean maintainerclean: clean
	@$(ECHO) "Removing environments."
	- $(RM) -r env*
