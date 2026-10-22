# Resolution record: quadratic random-permutation universality

Frozen record dated 2026-10-21 UTC. Queue row 1841; problem ID 30003131;
source key OWR-14604-008. Adjudication: **already_solved**, turn **1/5**.
This package does not modify the queue and makes no new-proof priority claim.

## Accepted conclusion and attribution

Yu Chen and Yiting Wang, *Quadratic-size Random Permutations are Universal*,
arXiv:2610.13530v1, submitted 9 October 2026, prove that there exist absolute
constants c>0 and k₀ such that, for every integer k≥k₀, a uniform permutation
of length 32k² is simultaneously universal for all k! patterns with failure
probability at most exp(−ck/log k). Patterns use increasing, not necessarily
consecutive, positions. The result is asymptotic, not an assertion for every
finite k. Source: https://arxiv.org/abs/2610.13530v1.

The relative order of the first 32k² positions of a uniform permutation of
length 1000k² is uniform. All patterns found in that subpermutation remain in
the full permutation. Thus the same failure bound settles Alon's original
1000k² sufficiency question, printed p.1218 of Oberwolfach Report 22/2016,
https://ems.press/journals/owr/articles/14604. The iid continuous model there
and the finite uniform permutation model agree through ranks.

The sharp asymptotic coefficient 1/4 remains open in the inspected manuscript.
The optional Section 4.1 sketch for every fixed coefficient greater than 1 is
not needed or claimed as the basis of this adjudication. Journal acceptance
is not established by the inspected arXiv record. Independent mathematical
acceptance is not peer review or community consensus. Priority belongs to the
cited authors, not this audit or package.

## Evidence and boundaries

- SOURCE_GATE.md recovers the exact original target, distinguishes the older
  He–Kwan near-total-pattern result from full universality, and records source priority.
- INDEPENDENT_ACCEPTANCE_REPORT.md reconstructs the analytic proof, including
  deterministic-support independence, adaptive queries, all-pattern uniformity,
  and He–Kwan's coupling. Its c=1/2352, log k≥32 regime is conservative and
  audit-derived, not an author-optimized constant.
- SOURCE_METADATA.json identifies inspected public artifacts by public URL,
  bytes, SHA-256 and retrieval time. Artifact names are identifiers, not included files.
- DATASET_METADATA.json records freshly hashed existing corpora and match
  results, not fresh upstream retrievals or copied dataset contents.
- check_audit.py and CHECK_RESULTS.json supply finite sanity checks only.
  CHECKER_PROVENANCE.json records hardening of the prior authored checker.
- REPRODUCIBILITY.json records byte-identical normal and optimized runs.
- INTEGRITY_TESTS.json records normal/optimized tamper and live-predicate controls.
- INDEPENDENT_PACKAGE_REVIEW.md records a separate package review.

No copied scholarly PDF, HTML, extracted source text, dataset contents,
private source, private coordination file, or private filesystem path is included.

## Reproduce and verify

From this directory, using Python 3 and its standard library:

    python check_audit.py > /tmp/universality-normal.json
    python -O check_audit.py > /tmp/universality-optimized.json
    cmp CHECK_RESULTS.json /tmp/universality-normal.json
    cmp /tmp/universality-normal.json /tmp/universality-optimized.json
    python verify_package.py
    python -O verify_package.py

MANIFEST.json enumerates every package file except itself, with byte lengths
and SHA-256 hashes. The verifier rejects extra/missing files and symlinks,
checks all manifest hashes, then compares both checker modes against the
frozen result. It is deliberately read-only. A separately retained hash of
MANIFEST.json is the integrity anchor: coordinated alteration of both files
and manifest cannot be detected without that external anchor. Hash integrity
and finite sanity checks do not establish the infinite analytic theorem.
