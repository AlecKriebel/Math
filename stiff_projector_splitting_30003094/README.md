# Direct projector splitting for stiff PDE discretizations

Problem **30003094**, source **OWR-14226-001**, queue row **1829**.
Research date: **20 October 2026**. Overall status: **UNSOLVED, 5/5 substantive
research avenues completed**. This is a partial-results package, not a claim
to resolve the original PDE error-analysis question.

## Accepted results

- Exact affine endpoint identities and homogeneous/invariant-subspace
  exactness for the original exact-subflow K–S–L projector splitting.
- Order-one error counterexamples for direct KSL and standard symmetric
  KSL-half/LSK-half Strang, despite vanishing step, normal defect and
  Hilbert-norm initialization error under the specified weak assumptions.
  The smooth-target example has a **rough numerical initializer**, not exact
  spatially projected smooth data.
- A two-sided heat-family counterexample that distinguishes direct full-field
  splitting from the modified stiff/nonstiff algorithm analyzed in 2019.
- A conditional left-affine global estimate
  δ + Tε + TτΓ‖C‖/2, with explicitly assumed defect and regularity bounds
  at the **actual numerical stages**, plus Fourier-Galerkin spatial tails.

No inverse retained singular value occurs explicitly in that estimate, but
rank preservation and uniform numerical-subspace regularity remain genuine
assumptions. No unconditional general PDE or robust second-order theorem is
claimed.

## Reading order

1. [Acceptance report](ACCEPTANCE_REPORT.md): exact accepted scope and limits.
2. [Five avenues](FIVE_AVENUE_SUMMARY.md): concise research account.
3. [Research report](RESEARCH_REPORT.md): direct-method counterexamples,
   rank-preserving projected dynamics, and honest PDE embeddings.
4. [Conditional subclass bounds](SUBCLASS_BOUNDS.md): complete positive
   proofs and the Fourier-Galerkin corollary.
5. [Strang obstruction](STRANG_OBSTRUCTION.md): symmetric-composition proof
   and rank checks.
6. [Mathematical audit](AUDIT_COUNTEREXAMPLE.md) and
   [machine-readable acceptance](AUDIT_ACCEPTANCE.json): independent
   mathematical rederivation and frozen manuscript hashes.
7. [Source gate](SOURCE_GATE.md): original source, later literature, and
   distinctions between direct, modified and stabilized methods.

The audit is a separate mathematical verification within this research
process, not external peer review or a literature-priority certificate.
The four manuscripts and audit are preserved byte-for-byte at the accepted
versions. Statements in them that no publication or queue change was made
describe their research/audit stage, not the eventual location of this copy.

## Reproduce the numerical corroborations

With the installed dependencies in [requirements.txt](requirements.txt), run
from this directory:

    python3 -I -S -B verify_manifest.py
    python3 -I -B run_checks.py

The first command checks the payload inventory, SHA-256 values, byte counts,
and accepted manuscript hashes. The second replays all four numerical
scripts in a fresh temporary directory without modifying this package.
It requires NumPy, SciPy and mpmath; it is **not** a standard-library-only,
exact-arithmetic, interval, symbolic or formal proof check. See
[reproducibility instructions](REPRODUCIBILITY.md) for versions, tolerances,
precision schedules, and limitations. The recorded run is
[REPLAY_VERIFICATION.json](REPLAY_VERIFICATION.json).

## Provenance and contents

[SOURCE_METADATA.json](SOURCE_METADATA.json) records public scholarly titles,
URLs, source-PDF hashes and sizes, and retrieval/inspection history.
[CORPUS_VERIFICATION.json](CORPUS_VERIFICATION.json) records dataset hashes,
byte counts and match results, not dataset contents. Those corpus copies
were recovered locally and freshly hashed; no fresh upstream fetch is
claimed. [MANIFEST.json](MANIFEST.json) inventories every payload file except
itself. Integrity checks do not authenticate an external author or prove
mathematical correctness.

No source PDF, raw extracted source text, source-page image, dataset,
private-source material, private coordination file, credential, or cache is
included. Public citations and short attributed discussion remain in the
authored mathematical reports.
