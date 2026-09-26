PYTHON ?= python3
CXX ?= c++
CXXFLAGS ?= -O2 -std=c++17 -Wall -Wextra -pedantic

.PHONY: verify
verify:
	mkdir -p build
	$(PYTHON) src/verify_counterexample.py --outdir build > build/verification_python.log
	$(CXX) $(CXXFLAGS) src/verify_counterexample.cpp -o build/verify_counterexample_cpp
	./build/verify_counterexample_cpp build/subgroups_cpp.txt > build/verification_cpp.log
	$(PYTHON) src/compare_certificates.py build/finite_certificate.json build/subgroups_cpp.txt
	$(PYTHON) independent_exact.py --subgroups-output build/independent_subgroups.json > build/independent_exact.json
	$(PYTHON) src/compare_results.py
