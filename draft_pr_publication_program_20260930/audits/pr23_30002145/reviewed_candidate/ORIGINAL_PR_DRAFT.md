# Proposed draft PR

Title: Audit 30002145: symmetric-gradient classification is already known

Head: dot/math-30002145
Base: main
Draft: true

## Summary

- Trace the imported question to its original Oberwolfach context
- Identify the complete signed-measure classification in De Philippis–Rindler (2020), Theorem 2.10, already cited by the dataset
- Record explicit formulas, scope caveats, primary-source locations, and exact symbolic checks
- Recommend source-status correction after independent review; make no new mathematical discovery claim

## Validation

`python3 unsolved_math_prioritization/attempts/30002145/verify.py`

All eight symbolic checks pass with SymPy 1.14.0. Necessity is established by the cited published theorem, not these computational checks. This source audit used zero new proof attempts.

## Scope

Only files under `unsolved_math_prioritization/attempts/30002145/`. No shared queue, catalog, assessment, or state edits. No merge or release requested.

## Independent review

A separate reviewer returned PASS for the exact frozen source artifact. The complete report, hashes, and eleven additional exact compatibility/nonorthogonal checks are under `review/`. This is a known whole-space/local blow-up classification and a source-status correction. No global claim on arbitrary nonconvex domains and no novel discovery is asserted.
