PYTHON ?= python3
CXX ?= c++
CXXFLAGS ?= -O2 -std=c++17 -Wall -Wextra -pedantic

.PHONY: verify audit pdf package
verify:
	mkdir -p build/certified
	$(PYTHON) src/verify_counterexample.py --outdir build/certified
	$(CXX) $(CXXFLAGS) src/verify_counterexample.cpp -o build/verify_counterexample_cpp
	./build/verify_counterexample_cpp build/certified/subgroups_cpp.txt
	$(PYTHON) src/compare_certificates.py build/certified/finite_certificate.json build/certified/subgroups_cpp.txt

audit: verify
	$(PYTHON) audit_2026_09_21/independent_check.py
	$(PYTHON) audit_2026_09_21/structural_check.py
	$(PYTHON) audit_2026_09_21/compare_independent.py

pdf:
	@if command -v pdflatex >/dev/null 2>&1; then \
	  pdflatex -interaction=nonstopmode -halt-on-error proof.tex && \
	  pdflatex -interaction=nonstopmode -halt-on-error proof.tex; \
	else tectonic proof.tex; fi

package:
	$(PYTHON) submission/build_package.py
