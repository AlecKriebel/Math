# Reproduction and verification package

Locally finite p-groups in Golod groups and an AT section

Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.
Version 1.0.0; 24 October 2026. Paper, prose and accompanying code: CC BY 4.0.

The paper gives an affirmative answer to Kourovka Notebook21.131 (A.V.Timofeenko). For every prime p it constructs a countable infinite locally finite original-definition AT p-group, and an epimorphism onto it from a subgroup of a classical homogeneous residually finite Golod group. A general theorem embeds every countably infinite locally finite p-group in a canonical nil-adjoint Golod group in the exact9.76 definition. The latter embedding does not assert residual finiteness; the stronger homogeneous source is used via an epimorphism and an inverse-image subgroup.

## Contents

- `paper.pdf` and `main.tex`: the full research note and LaTeX source.
- `verification/run_all.py`: the standard-library reproduction entry point.
- `verification/lib/`: independently authored finite tree, matrix, wreath and augmentation evaluators, plus the construction family's finite-level evaluator.
- `verification/expected_results.json`: deterministic finite results for independent comparison.
- `audits/`: mathematical, scope and priority reviews. Reports are dated historical checkpoints; later reports record the disposition of earlier pending questions.
- `source_manifest.json` and `algebra_sources.json`: source URLs and checksums. Third-party papers and primary-page images are not redistributed.
- `MANIFEST.json`: file sizes and SHA-256 checksums for the complete package except the manifest itself.

## Reproduce

Run `python3 verification/run_all.py` from the unpacked package. Python3.10 or later and its standard library suffice. The runner deliberately refuses optimized Python because the finite evaluators use assertions. It prints a summary and writes `verification/latest_results.json`. No network, GAP, SageMath or external packages are needed.

The finite checks comprise11,778 common-zero section/portrait comparisons;63 named noncommutative matrix checks;348,516 fresh tree-section comparisons and3,516 fresh algebra assertions; the construction family's stored finite-level images and transitivity checks; and nonabelian wreath/augmentation calculations for UT3 over F2 and F3. The two matrix evaluators include negative controls showing that the diagonal auxiliary map is not a homomorphism. A bad tree cutoff and invalid wreath wraparound are also checked as negative controls.

These are supplemental exact finite checks. They do not prove local finiteness of every generated subgroup, universal embeddings, absolute nilness, the external embedding theorems, or originality. Those claims are justified by the paper's infinite proofs and explicitly cited external theorems.

Compile `main.tex` with `tectonic -X compile main.tex`, or a normal LaTeX distribution with lmodern, amsmath, amssymb, amsthm, mathtools, microtype, geometry, enumitem and hyperref. For conventional LaTeX run twice to resolve references.

## Established inputs and exact hypotheses

AAJZ's stable-nil algebra embedding theorem was published in2017 (Theorem6 of the announcement); detailed numbering here refers to Theorem4.3 of arXiv1703.08734v2, subsequently published in2019. The first clause preserves stable nil. The paper verifies that the particular construction preserves stable nil over every extension field for the augmentation input. This is what permits Hammoudi2003Theorem3, whose hypothesis is **absolutely nil**, to be applied. Stable nil alone is not substituted for that hypothesis.

The original Rozhkov1986 definition requires each selected longitudinal mutation to have infinite level support. The construction satisfies that requirement and does not use finitary generators as substitutes. C is a subgroup of rooted mutations and D a subset of longitudinal mutations; infinite D is permitted. The exact authoritative21.131 statement is in the official twenty-first Notebook,20October2026 revision, printed199, and explicitly refers to9.76.

Primary AT text was inspected through the indexed original1986 article. Its original PDF bytes were not acquired despite repeated attempts; this source-custody limitation is recorded. The official Notebook, AAJZ author manuscript and Hammoudi publisher PDF were acquired and inspected. The2019AAJZ version of record was inaccessible; the author manuscript supplies the cited numbering and checked proof.

## Review, priority and AI disclosures

AI tools were used extensively in discovery, development, writing and mathematical verification, including separate independent adversarial AI reviewers. Review approval does not replace the proofs. This preprint has not undergone independent human peer review. No formal proof-assistant verification is claimed.

The extensive bounded priority search through24October2026 found no earlier complete same-scope solution. It credits Phillips's periodic-group embeddings, AAJZ's established algebra theorem, Hammoudi's homogeneous cover and original AT theory. It does not claim first discovery certified by an exhaustive literature search. Authenticated MathSciNet, some zbMATH results and some publisher full text were unavailable; indexing lag and unpublished work cannot be excluded.

The general statement does not resolve Notebook13.55 or assert a finitely generated AT target. No journal submission has been initiated.
