# Reproduction and exact verification scope

The mathematical bridge is a proof, not a numerical experiment. Read publication/main.tex and proofs/bridge_independent.md. No numerical approximation establishes the Riesz constant.

The standalone manuscript requires Tectonic (tested 0.16.9), or a current LaTeX distribution with the named packages. Its bibliography is embedded in main.tex. From publication, run `tectonic main.tex` to obtain main.pdf; the deposited copy is named paper.pdf. Rebuilt PDF metadata can differ while the source and content agree.

To reproduce the computational dependency checks without modifying the upstream clone, use Python 3 with python-flint==0.9.0 and an unmodified checkout at commit adc7f1241b42e322a6451854ab7e4b4c146bf78a:

```sh
python3 -m venv /tmp/riesz-checker-environment
/tmp/riesz-checker-environment/bin/python -m pip install python-flint==0.9.0
/tmp/riesz-checker-environment/bin/python reproducibility/reproduce.py \
  --upstream /path/to/pinned/openai-math \
  --run-upstream --receipt /tmp/riesz-clean-receipt.json
```

The runner verifies the SHA-256/size of all 34 recorded source/configuration files, copies the two exact manuscript source trees into a clean temporary directory, compiles the standalone note, checks PDF validity and TeX warnings, runs the main interval and scalar checkers, and runs the atomic exact checker. It never builds or writes to the input clone. Source copies are temporary and are not redistributed in this package. Python 3.14.6 was used for the recorded checks. The main numerical checker uses 256-bit Arb intervals and its scalar checker uses 512-bit Arb or exact rational/integer arithmetic. Atomic checks use Python's standard library.

Recorded receipts under audit_runs/upstream_main/certificate_results and verification/atomic_checker_execution.json bind actual successful executions. Finite checks concern explicit arithmetic, matrix and polynomial inequalities. Their analytic propagation to infinite interpolation, all radii and all Gaussian parameters, and the density/mixture theorem was reviewed separately in the two manuscript audits. The runner does not prove those analytic arguments or the follow-on theorem.

Actual Lean source semantics and the reachable 227-module source closure were examined. A pinned compatible Lean/Mathlib build was not completed; no kernel axiom audit or Comparator pass is claimed. Formal source inspection is recorded in agent_notes/formal_audit.md and verification/formal_source_*.json. The paper, finite transfer and surface theorem are not formalized here.

All third-party manuscripts and Lean sources are referenced by immutable links/hashes; the deposit does not include their PDFs, caches, toolchains or copied sources. The supplied upstream citation blocks are retained in sources/UPSTREAM_CITATIONS.md. Review records are automated adversarial audits, not conventional human refereeing.
