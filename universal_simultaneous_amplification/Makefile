.PHONY: paper1 test verify clean-paper

PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

test:
	PYTHONPATH=. $(PYTHON) -m unittest discover -s tests -v

verify:
	PYTHONPATH=. $(PYTHON) verification/verify_obstruction.py

paper1: test verify
	cd paper && tectonic main.tex
	cp paper/main.pdf output/pdf/universal_simultaneous_amplification_obstruction.pdf

clean-paper:
	rm -f paper/main.pdf
