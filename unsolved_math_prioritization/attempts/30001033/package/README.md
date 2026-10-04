# Rank 610: finite width of the 14-triangle-complex group

Status: **unsolved, 5/5**. No complete proof or counterexample is claimed.

`PROOF.md` gives the exact normalized statement, rigorous partial proofs, and the remaining kernel obstruction. `APPROACH_LOG.md` records five distinct approaches. `PROVENANCE.md` distinguishes the source statement, published partials, finite evidence, and the literature-search limits.

The strongest results here are:

- G_ab ≅ C4 × C12 and γ1/γ2 ≅ C2.
- Every subsequent lower-central factor is a finite elementary abelian 2-group.
- The conjectured periodic dimensions are lower bounds at every index.
- The exact index formula holds at i=2 and i=3.
- Full resolution requires proving that the explicitly identified excess kernels vanish for every i≥4.

This package is a source-grounded partial analysis. The matrix mechanism is known; no novelty or solved status is claimed.

## Reproduce

Python 3.10+ and the standard library are sufficient. From this directory:

```sh
python3 controls.py --max-cutoff 5 > /tmp/rank610-controls.json
cmp controls-output.json /tmp/rank610-controls.json
python3 test_controls.py
sha256sum -c SHA256SUMS
```

The finite-image computation is deliberately bounded at five block diagonals and 65,536 elements. It does not calculate all universal nilpotent quotients. The periodic leading-image result instead uses an exact finite-state cycle and proves an all-index statement about the image only.

All eight tests passed in the recorded run, including an independent dense-matrix multiplication check and deliberately wrong relator/indexing controls. This is not a substitute for independent mathematical review.

No scholarly source PDF, source-corpus bulk data, or private coordination is included. No remote repository write was performed during preparation. Independent review and the release gate remain required before publication.
