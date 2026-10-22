# Bahri Xu inequality research and audit package

Problem 30000263 / OWR-1050-014. Author freeze, 2026-10-05.

**Verdict: partial results, no full resolution.** Read RESEARCH_REPORT.md for
the precise question, five approaches, proofs, literature audit and remaining
gap. A new-to-this-investigation cubic-virial argument independently proves
collinear zero exclusion; no novelty is asserted. The uniformity step is
credited to the published collision/escape theorem. The general conjecture
is not proved.

This package contains authored analysis, authored code, authored numerical
outputs, and public verification metadata. It contains no primary-source
PDFs, copied extracts, screenshots, dataset contents, or private coordination
material. No remote repository mutation or outreach was performed.

## Replay

Python 3.10 or later, standard library only:

    python verify_release.py
    python -O verify_release.py
    python test_verifier.py

The verifier checks all manifest hashes and sizes, exact rational certificates,
algebraic identities, the source-review pins, and independent scalar replay of
all 24 stored numerical outcomes. A pass is an artifact check, not an automated
proof of the general conjecture. The full mathematical arguments require a
human or independent mathematical audit.

To repeat the complete-source checks when the three full input corpora are
available, supply their files in this order:

    python verify_release.py --corpora CATALOG.json PROBLEMS.json REPORTS.json

All three hashes, byte counts and record counts must match; the verifier then
extracts the entire target problem record, uses {} for its absent research
report, and recomputes the exact prescribed JSON review hash. Omitted external
inputs are explicitly reported as NOT_PROVIDED, never as verified.

To verify retrieved PDF bytes, use --source-dir with a directory containing
the five retrieval filenames in SOURCE_METADATA.json. The public source URLs
are provided so an auditor can independently obtain the papers. These PDFs
are deliberately outside the ZIP.

## Optional numerical rerun

The exploratory search requires NumPy and SciPy; the recorded run used
NumPy 2.3.5 and SciPy 1.17.0. To rerun without altering the frozen package,
write the result outside this directory:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python search_numeric.py --starts 6 --budget 500 --output ../rerun.json

Floating-point optimizer trajectories can vary across platforms. Stored
coordinates and charges can be checked without these dependencies by the
standard-library verifier. Positive observed ratios do not constitute global
lower bounds. Budget exhaustion is explicitly recorded in NUMERIC_SUMMARY.json.

## Integrity and scope

freeze.py rebuilds the manifest and produces a deterministic, flat ZIP from
an explicit filename allowlist. Run it only on an intentionally edited author
copy, not as a substitute for checking the frozen manifest:

    python freeze.py --output ../recreated.zip

The parent-supplied ZIP SHA-256 authenticates a specific freeze; a manifest by
itself only provides internal integrity. The test suite checks ordinary and
optimized Python, missing files, altered bytes, corrupted semantic fields,
and nonfinite JSON rejection. No validation depends on Python assert.

This is the author package, awaiting uninvolved review. No independent
acceptance is claimed here.
