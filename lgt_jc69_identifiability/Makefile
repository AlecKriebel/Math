PYTHON ?= python3
LATEXMK ?= latexmk

EXACT_SCRIPTS = \
	environment_audit.py \
	exhaustive_measure_audit.py \
	symbolic_audit.py \
	jc_transition_audit.py \
	analytic_identity_audit.py \
	scope_topology_audit.py \
	source_formula_audit.py \
	verify_table_double_point.py

.PHONY: verify-exact audit-simulation verify pdfs wording-audit manifest-check clean

verify-exact: wording-audit
	@set -e; \
	cd verifier; \
	for script in $(EXACT_SCRIPTS); do \
		$(PYTHON) $$script; \
	done; \
	echo "ALL EXACT CHECKS PASSED"

wording-audit:
	@$(PYTHON) tools/wording_audit.py .

audit-simulation:
	@set -e; cd verifier; $(PYTHON) simulate_process_audit.py

verify: verify-exact audit-simulation
	@echo "ALL CHECKS PASSED"

pdfs:
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error -file-line-error main_manuscript.tex
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error -file-line-error technical_summary.tex
	@$(PYTHON) tools/check_latex_log.py main_manuscript.log technical_summary.log

manifest-check:
	@sha256sum -c MANIFEST.sha256

clean:
	$(LATEXMK) -C main_manuscript.tex >/dev/null 2>&1 || true
	$(LATEXMK) -C technical_summary.tex >/dev/null 2>&1 || true
	rm -f *.aux *.log *.out *.toc *.fls *.fdb_latexmk *.synctex.gz
