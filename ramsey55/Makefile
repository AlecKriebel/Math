CXX ?= clang++
CXXFLAGS ?= -O3 -std=c++17 -Wall -Wextra -pedantic

.PHONY: all test clean

all: build/bitset_verify build/search43 build/search43_incident_lns \
	build/search43_targeted_hamming3 build/extension_sat_proof_solver \
	build/core_completion_proof_solver

build:
	mkdir -p build

build/bitset_verify: verify/bitset_verify.cpp | build
	$(CXX) $(CXXFLAGS) $< -o $@

build/search43: src/search43.cpp | build
	$(CXX) $(CXXFLAGS) $< -o $@

build/search43_incident_lns: src/search43_incident_lns.cpp | build
	$(CXX) $(CXXFLAGS) $< -o $@

build/search43_targeted_hamming3: src/search43_targeted_hamming3.cpp \
		src/search43.cpp | build
	$(CXX) $(CXXFLAGS) $< -o $@

build/extension_sat_proof_solver: src/extension_sat_proof_solver.cpp | build
	$(CXX) $(CXXFLAGS) $< -o $@

build/core_completion_proof_solver: src/core_completion_proof_solver.cpp | build
	$(CXX) $(CXXFLAGS) $< -o $@

test: all
	python3 -m unittest discover -s tests -v
	python3 tests/core_completion_sat_tests.py
	python3 tests/core_completion_proof_tests.py
	python3 tests/core_completion_k2_tests.py
	python3 tests/residual_lns_tests.py
	python3 tests/residual_completion_tests.py
	python3 tests/direct_ramsey_cnf_tests.py
	python3 tests/core_radius_cnf_tests.py
	python3 tests/test_delta_formula.py --n 6
	build/search43 --self-test --seed 20260723 --trials 20
	build/search43_incident_lns \
		--seed-graph results/best_candidates/exoo_seed_20260724.g6 \
		--metadata certificates/residual_lns_incident_six.metadata.json \
		--seed 20260726 --self-check --self-check-random-flips 100

clean:
	rm -f build/bitset_verify build/search43 build/search43_incident_lns \
		build/search43_targeted_hamming3 \
		build/extension_sat_proof_solver build/core_completion_proof_solver
