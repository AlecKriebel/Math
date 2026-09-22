PYTHON ?= python3
CXX ?= c++
CXXFLAGS ?= -O2 -std=c++17 -Wall -Wextra -pedantic

.PHONY: verify pdf

verify:
	mkdir -p build/certified
	$(PYTHON) src/verify_counterexample.py --outdir build/certified
	$(CXX) $(CXXFLAGS) src/verify_counterexample.cpp -o build/verify_counterexample_cpp
	./build/verify_counterexample_cpp build/certified/subgroups_cpp.txt
	$(PYTHON) src/compare_certificates.py build/certified/finite_certificate.json build/certified/subgroups_cpp.txt

pdf:
	pdflatex -interaction=nonstopmode -halt-on-error proof.tex
	pdflatex -interaction=nonstopmode -halt-on-error proof.tex
