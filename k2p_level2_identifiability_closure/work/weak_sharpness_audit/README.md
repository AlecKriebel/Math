# Independent weak-sharpness audit

This directory is a clean-room replay of the three-leaf weak-tree-child K2P
sharpness construction and its identical-cherry induction.  It imports neither
the primary sharpness graph builder nor the four-port atlas.

The audit checks:

- all edge rootings under the standard semi-directed convention, including
  rooting on each reticulation edge;
- weak-but-not-strong tree-child status;
- exact labelled mixed-graph nonisomorphism and the ordinary-triangle quotient;
- the four displayed-tree K2P expansion over the rationals;
- both exact rank-nine minors and the shared strict continuous-time tensor;
- the four-dimensional cherry block, local inverse, rooting lift, and pruning
  induction; and
- 20 targeted corruptions plus optimized-mode refusal.

Create an isolated Python environment, install `requirements.txt`, and run:

```sh
python audit_weak_sharpness.py
python test_mutations.py
```

Expected markers are
`K2P_WEAK_SHARPNESS_INDEPENDENT_AUDIT_PASS` and
`K2P_WEAK_SHARPNESS_AUDIT_MUTATIONS_PASS`.

The audit's maximum resident set size in the recorded M1 Pro replay was below
50 MB.
