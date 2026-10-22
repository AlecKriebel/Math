# Reproducibility

Recorded environment: Python 3.12.14, SymPy 1.14.0, NumPy 2.3.5. Exact dependencies are listed in requirements.txt. Python's fractions and integer arithmetic are used for independent exact checks. NumPy floating-point arithmetic guides only the exploratory frozen-first search.

Run from the package directory, or pass the absolute script path from another directory:

    python computation/check_attempt_1.py
    python computation/check_attempt_2.py
    python computation/check_attempt_3.py
    python computation/check_attempt_5.py
    python computation/check_audit.py
    python computation/verify_countercontrols.py
    python computation/cyclic_search.py --trials 30
    python computation/frozen_search.py

Scripts producing JSON default to sibling result files next to the script, not the current working directory. cyclic_search.py also accepts --output. Run in a disposable package copy to preserve the shipped results. Search seeds and finite ranges are in the scripts and accompanying documents. Attempt 4 is analytic and has no separate checker. Runtime and timing measurements are not mathematical outputs and are not compared as evidence.

Recorded source results include ATTEMPT_3_RESULTS.txt, ATTEMPT_5_RESULTS.txt and the three JSON result files. All eight commands above passed in an isolated copy, invoked with absolute script paths from an unrelated working directory. Each corresponding stdout log is included in computation/. All fields of all three parsed JSON outputs exactly matched the shipped source results, and check_attempt_3/check_attempt_5 stdout byte-matched ATTEMPT_3_RESULTS.txt/ATTEMPT_5_RESULTS.txt respectively. This also verifies that default result destinations are independent of the working directory. Exact output equality is a reproducibility check in the recorded environment, not a general guarantee for different library versions or floating-point implementations. No negative search result proves nonexistence beyond its stated tested set.

The small randomized scalar-ideal exploratory experiment described in CYCLIC.md has no standalone saved script in this package and is not claimed as independently reproduced. Its accompanying scalar-ideal upper bound is analytic and does not depend on that experiment. check_attempt_2.py runs the t=5/7 search; the separately reported t=3/4 exploratory counts are not its default reproduction target.
