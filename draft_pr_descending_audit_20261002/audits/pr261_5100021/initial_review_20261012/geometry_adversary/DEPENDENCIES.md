# Local replay dependencies

The independent Python scripts use mpmath1.3.0 and sympy1.14.0 (ordinary arithmetic and polynomial reduction only). These were installed locally under the ignored `_python/` directory. For replay, install those packages there or change the scripts' import path. No author checker or reviewer checker is required. Python used: the Codex bundled runtime `/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.

The pre-exposure numerical script needs about15 seconds on the audit machine. `symbolic_four_phase.py` may take about2 minutes. All receipt files are plain JSON; exact certificates report polynomial remainders and rational/radical area values. Floating-point receipts provide diagnostics, not interval-arithmetic proof certificates.
