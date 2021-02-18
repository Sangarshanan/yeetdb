VENV_NAME ?=.venv
PYTHON=$(VENV_NAME)/bin/python

.PHONY: help
.DEFAULT: help
help:
	@ echo "Salutations ! Welcome to YeetDB \n"
	@ echo "	make install -> To set up the environment"
	@ echo "	make run -> To spin up the REPL"

install:
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME);
	$(PYTHON) -m pip install -r requirements.txt

run:
	@ $(PYTHON) src/repl.py
