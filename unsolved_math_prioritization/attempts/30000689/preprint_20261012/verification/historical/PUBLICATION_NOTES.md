# Audited candidate: missing-middle-face embedding obstruction

Target 30000689 / OWR-1455-008. Prepared 3 October 2026 UTC.

## Result and exact scope

The [complete affirmative candidate](release/PROOF.md) establishes that adjoining a missing d-face to the d-skeleton of **any finite triangulation of a topological 2d-sphere** prevents **any topological embedding** into S^{2d}. The source is not restricted to standard PL spheres, and the prohibited embedding is not restricted to linear, PL, or tame embeddings.

The algebraic argument uses a Koszul dimension jump together with published Karu–Xiao Lefschetz consequences and the Adiprasito–Patáková ambient-extension theorem. Weber's metastable existence theorem supplies the topological conclusion for d>=3. Dimension four is covered by an explicitly checked extension of Nevo–Wagner's local bistellar proof, using a flag-subdivision base and a contractible-complement lemma. The proof does not assume that an exotic PL 4-sphere is standard or invoke four-dimensional PL Schoenflies.

## Review status

The [fresh independent whole-packet audit](audit/AUDIT_REPORT.md) returned PASS: no substantive mathematical gap was found in the exact frozen argument. This is independent AI-assisted checking, not formal verification or independent human peer review. The [explanatory addendum](EXPLANATORY_ADDENDUM.md) records all four nonblocking exposition improvements requested by that audit.

The author's README and research log preserve their historical 'audit pending' wording because they are frozen reviewed inputs. This file records the subsequent review status without altering them. The author freeze is [hash-bound](release/FROZEN_AUTHOR_MANIFEST.json), and the audit has its own [manifest](audit/AUDIT_MANIFEST.json).

## Reproduce the finite controls

From this directory:

    python3 release/check_exact.py > author_replay.json
    cmp author_replay.json release/exact_results.json
    python3 audit/check_independent.py > independent_replay.json
    cmp independent_replay.json audit/independent_results.json

Both checkers use Python's standard library. The independent controls include 100 bistellar transitions, 3,542 complementary-homology checks, 824 common-missing-triangle checks, and 70 explicit deleted-product witnesses with odd intersection evaluation. These finite controls support the reasoning; they do not replace the universal proof or its cited theorems.

## Attribution and limits

Published inputs and the original Nevo–Wagner PL-source result are credited explicitly. The dimension-four extension is presented as a deduction, not falsely attributed as their verbatim theorem. No novelty, first-priority, external human review, or formal-certification claim is made. The bounded source and duplicate checks are in [SOURCE_GATE.md](release/SOURCE_GATE.md).

Three substantive approaches produced a complete candidate within the five-approach budget. The queue status remains `claimed_solved`, with `3/5` recorded; publication of this draft does not imply mathematical acceptance. No source PDF, complete foreign article, source corpus, private context, or credential is included. This draft publication does not merge the pull request, create a release, or create a DOI.
