# vim: set shiftwidth=4 tabstop=4 noexpandtab:
CURDIR	?= $(shell pwd)
ENVDIR	?= $(CURDIR)/env
PROJECT	?= $(notdir $(CURDIR))
PYTHON3_PATH ?= "$(shell which python3)"

ECHO    ?= echo
RM      ?= rm -f
PIP		:= "$(ENVDIR)/bin/pip"
PYTHON  := "$(ENVDIR)/bin/python"
FIND    ?= find
PYTEST  := py.test

.PHONY: help setdevelop test

help:
		@$(ECHO) "Make sure you have virtualenv installed: pip install virtualenv"
		@$(ECHO) ""
		@$(ECHO) "Use any of these targets"
		@$(ECHO) "============================================================"
		@$(ECHO) "Useful targets targets:"
		@$(ECHO) " setdevelop  - Set the environment to begin to work"
		@$(ECHO) " test        - Install test requirements and run the tests"
		@$(ECHO) "------------------------------------------------------------"
		@$(ECHO) "Housekeeping targets:"
		@$(ECHO) " clean            - Remove intermediate, and generated files"
		@$(ECHO) " maintainer-clean - As clean, but removing the env also."
		@$(ECHO) "============================================================"
		@$(ECHO) ""

setdevelop:
	virtualenv -p $(PYTHON3_PATH) ./env
	$(PIP) -q install -r "$(CURDIR)/requirements/requirements_test.txt"
	@$(ECHO) "/////////////////////////////////"
	@$(ECHO) "To activate the environment type:"
	@$(ECHO) "source env/bin/activate"

test: 
	@$(PYTEST) tests

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
