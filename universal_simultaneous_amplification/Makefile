.PHONY: paper1 test verify directed triangle n4 phase3-check clean-paper

PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
export PYTHONDONTWRITEBYTECODE := 1
# Pin PDF metadata so independent release builds are byte-for-byte stable.
export SOURCE_DATE_EPOCH := 1785542400

test:
	PYTHONPATH=. $(PYTHON) -m unittest discover -s tests -v

verify:
	PYTHONPATH=. $(PYTHON) verification/verify_obstruction.py

directed:
	PYTHONPATH=. $(PYTHON) phase1_directed/verify_directed_db_strong.py

triangle:
	PYTHONPATH=. $(PYTHON) phase2_triangle/derive_certificate.py
	PYTHONPATH=. $(PYTHON) phase2_triangle/crosscheck_exact_solver.py
	PYTHONPATH=. $(PYTHON) phase2_triangle/audit/independent_triangle_audit.py

n4:
	PYTHONPATH=. $(PYTHON) phase2_n4/derive_lumped_certificates.py
	PYTHONPATH=. $(PYTHON) phase2_n4/crosscheck_full_chain.py

phase3-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) phase3_asymptotic/verify_lumping.py

paper1: test verify directed triangle n4 phase3-check
	cd paper && tectonic main.tex
	cp paper/main.pdf output/pdf/no_universal_death_birth_amplifier.pdf

clean-paper:
	rm -f paper/main.pdf
