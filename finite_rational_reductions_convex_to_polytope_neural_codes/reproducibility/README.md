# Reproducibility package

The exact scripts replay finite rational calibrations supporting the manuscript.  They do **not** constitute machine proofs of the universal geometric theorems.  Those theorems are proved in the manuscript.

The replay checks:

1. maximal-intersection and binary-meet combinatorics;
2. a rational interval bridge with a simultaneous endpoint class;
3. fixed-arrangement cells including lower-dimensional and tangent cases;
4. the exact sequential-repair failure and synchronized repair;
5. the stronger one-round three-neuron failure and its second common-core resolution;
6. manuscript and technical-appendix compilation;
7. package manifests and artifact hashes.

Run from the publication root with:

```bash
./reproducibility/replay.sh
```

No network access, shell escape, or nonstandard Python package is required.
