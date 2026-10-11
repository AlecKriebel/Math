# 10400117: known answer already stated after Problem 7.2

**Source-status correction, 0/5 proof-search approaches. Separate adversarial AI source review passed; see [the report](review/REVIEW.md). This has not undergone human peer review.**

The [audit](SOURCE_STATUS.md) recovers the omitted Hansen–Takata remark: L(25,4) and L(25,9) have equal LMO invariants and different SU(2) quantum invariants at shifted level 5. Bar-Natan–Lawrence's complete lens-space formula verifies full-LMO equality. This is prior knowledge, not a new solution.

The package distinguishes this item from campaign target 10400120, which concerns absolute values and fundamental groups.

Run the elementary controls with Python 3:

```sh
python3 unsolved_math_prioritization/attempts/10400117/verify.py
```

All 112 exact assertions pass. They check Dedekind sums, lens-space modular classes and surgery arithmetic. They do not recompute the quantum invariant; its exact inequality is credited to the original primary source, with the numerical Freed–Gompf table only corroborating it. See `sources.json` for precise locations and hashes.

The frozen source-status artifact retains its original pre-review header for hash reproducibility. The completed audit covers that unchanged text. Its 112 author controls replay byte-identically, and 2,331 independent controls pass.
