# Proposed supported verification interface for PR 445

This additive package addresses reproduction finding **R1 / repair RR1** at
frozen head `3242c84e06db7e99012c7fe581adde5c3f89fc89`, problem 30002737.
It requires Python **3.10 or later** and only the standard library.
The repair is proposed for independent adversarial inspection; it does not
constitute that inspection's acceptance or certify the infinite theorem.

Run the supported entry point from any working directory:

```sh
python3 "/absolute/path/to/verification_repair/verify.py"
PYTHONOPTIMIZE=1 python3 "/absolute/path/to/verification_repair/verify.py"
```

The package is relocatable, including to a directory whose path contains spaces.
It writes no files and prints one JSON PASS only after every integrity and
mathematical guard executes. Any failed guard produces a nonzero exit, an error
on stderr, and no stdout success. The entry point launches no subprocess.

`frozen_history/` contains exact copies of all twelve original package files.
**Both historical assertion scripts remain unsafe under optimized Python.**
They are never imported or executed by this supported interface. Do not use the
old README's reproduction commands as the supported interface. Their saved
outputs, historical PASS text and historical isolated-replay sentence remain
unchanged and are checked as stored history; this runner does not claim to
replay those scripts robustly or to repair their frozen bytes.

`verify.py` is the trust anchor to review and preserve. It contains a literal
SHA-256 pin for `SOURCE_MANIFEST.json` and literal hashes for both supported
control modules. It checks the frozen identity, complete twelve-file inventory,
canonical safe paths, absence of symlinks, SHA-256 hashes, byte lengths, both
historical manifests and both saved JSON outputs. It verifies history again
after the controls. A fixture with a self-consistent re-sealed manifest cannot
become a different accepted source snapshot. Altering the trusted `verify.py`
itself changes the verifier and requires a new review; fixture metadata is not
an authority to approve that change. `PUBLIC_FILES.json` is publication seal
metadata, not the input trust anchor and not an independent approval.

The fresh controls check all original finite families. They retain the exact
original finite ranges for author moment/weighted/overlap fields and repeat the
original deterministic substitution/recursion/physical-pair/local-marker/flow
families without importing the historical scripts. Physical membership counts
are compared with separate factorized counts that retain finite boundaries and
sign imbalance; observed density is allowed to differ from its infinite limit.
Additional guarded controls cover translated marker decoding, polynomial
moments, planar sections, equal-sequence negative-index pairs, physical
representative gluing and the suspension cocycle.

The original author saved result agrees in every field with newly evaluated
finite controls plus its frozen checker digest. All finite fields in the
independent saved result agree with fresh deterministic controls. Its historical
replay and proof-limit sentences are checked as text, with their historical
meaning explicitly retained. No new robust replay claim is attached to them.

To reproduce the subprocess test matrix, choose a new checkpoint name:

```sh
python3 "/absolute/path/to/verification_repair/test_suite.py" --records records/my_normal_checkpoint
PYTHONOPTIMIZE=1 python3 "/absolute/path/to/verification_repair/test_suite.py" --records records/my_optimized_checkpoint
```

Existing record directories are refused. Each actual child uses the launching
`sys.executable`, is run from an arbitrary working directory, and receives
either an environment with optimization removed or inherited
`PYTHONOPTIMIZE=1`. The baseline runs a relocated package with spaces in its
path; a hostile PATH `python3` trap would fail any unpinned child selection.
Disposable fixtures stay under `private/` and are removed; their raw subprocess
stdout/stderr, command, return code and rejection reason are preserved in the
selected records directory before the suite assesses success.

The `--diagnostic-fault` options deliberately alter actual calculations or the
parsed saved record, while leaving all literal integrity pins enabled. They
must fail the explicit mathematical/semantic guards; they cannot approve a
fixture or bypass an integrity check. These mathematical failures are recorded
separately from corrupted-input/code integrity failures, including saved bytes
and a complete re-seal of both historical manifests and the source manifest.

`controls_exact.py` adapts the independently authored
`/root/pr445_reproduction/exact_controls.py`, original digest
`8f10069458d02fe866aaccf5653bd2511f90939a9efc50e1d5286917bbcadb30`.
The mathematical logic is intact; its CLI became a return-value API.
`controls_deterministic.py` is newly authored after reading the frozen checker
and independent geometry/spectral controls. `ATTRIBUTION.json` records those
inputs without bundling foreign primary PDFs or private review fixtures.

Finite verification supplements the analytic proof and credited infinite
Rudin–Shapiro input. It proves neither the infinite correlations nor hull
strict ergodicity by sampling, historical novelty, priority, human peer review,
or a separately restricted one-dimensional result. The frozen author attempt
count remains **1/5**; this repair performs **zero original proof-search attempts**.
