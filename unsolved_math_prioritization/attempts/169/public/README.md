# Random translate covers at square root size

**Green Problem 39 · record 1789 · ID 169 · GREEN-081 · five-stage mathematical study, 14 October 2026**

**UNSOLVED.** Let p tend to infinity through primes and let A be a uniformly random floor(√p)-element subset of Z/pZ. Does the probability that at most floor(100√p) translates of A cover the whole group tend to one? The translating set may depend arbitrarily on all of A.

This study supplies partial theorems, exact reductions, conditional positive and negative bridges, and counterexamples to specified proof shortcuts. It supplies neither an affirmative proof nor a negative answer to that probability question. In particular, failure of a proposed algorithm or class of translating sets does not disprove the original assertion.

## Reading order

1. [Mathematical reader](RANDOM_TRANSLATE_COVERS_READER.md): executive explanation, the full model, strongest results, and remaining gap.
2. [Results index](RESULTS_INDEX.md): all 21 authored mathematical supplements and five mathematical audits.
3. [Status and scope](STATUS_AND_SCOPE.md): quantifiers, provenance, and what the diagnostics do not prove.
4. [Sources](SOURCES.md): scholarly dependencies and dated source-status limitations.
5. [Reproducibility](REPRODUCIBILITY.md): self-contained finite tests, optimization-mode replay, and negative controls.

Earlier conservative residual concentration bounds are preserved in the historical supplements. The final reader uses the improved exchange bound m and denominator 2km². Those changes strengthen constants, without establishing the missing expectation estimate.

All included examples and fixtures are synthetic finite mathematics. No external dataset contents, source PDFs, copied third-party source text, private coordination records, or user conversations are included. Historical source identities and the curated public editions are distinguished by their hashes. Mathematical acceptance means the recorded study audit, not external peer review or a priority claim.

## Local verification

Python 3.10 or newer; standard library only; no network required:

    python3 -I -B verify_package.py
    python3 -I -B run_checks.py
    python3 -I -B check_tamper_controls.py

The wrapper runs each included checker under normal Python, -O, and -OO in disposable directories, compares exact outputs, exercises active guards and formula mutations, and checks that the public package was not changed. The reproducibility guide distinguishes this lightweight public replay from the larger historical exhaustive enumerations.
