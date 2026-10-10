# Independent audit A: statistical embedding problem 6000001

**Verdict: PASS. No correction of the frozen mathematical proof is required.**

The full reconstruction and scope analysis are in `GLOBAL_AUDIT.md`. The exact accepted statement, limitations, proof identity, and review coverage are recorded in `ACCEPTANCE.json`. This is independent audit A only; it makes no journal-acceptance or historical-novelty claim.

The author proof is exactly 17,635 bytes with SHA-256 `a26c1755bc6f61085db4c01b6579701ff380822f2cc58a3ffbfb4acfa49370a2`. Its original manifest SHA-256 is `7df56d745e4c57a30d0303388b1adda3e52d1c99190d2f96fe50b6d616b1cf3f`. Neither was modified. The original full audit and independent control program are preserved byte for byte; rerunning the controls reproduced the original result byte for byte.

## What was checked

The audit checks the entire finite-dimensional global construction: scalar jet transformations, a proper polynomial feature embedding, a smooth global coefficient lift, an exact pair with no period obstruction, a normal-bundle Hessian extension, nonuniform pointwise positivity, properness in the restricted target, dual flatness, and the metric and both induced connections. It does not infer arbitrary-manifold existence from finite symbolic tests.

The primary definition in Amari 1997 and the original FMU question support the theorem's torsion-free flat-connection interpretation. The target may be nonconvex and incomplete. A finite probability simplex, global injectivity of the gradient, an optimal dimension, and historical novelty are outside the accepted claim.

## Reproduce the controls and integrity check

From this directory, with Python 3 and SymPy installed, run:

```sh
python independent_controls.py
python verify_audit_packet.py
```

The first command checks six groups comprising 63 exact algebraic or integrity conditions. It expects the unchanged author packet at `../../public` and reproduces `INDEPENDENT_CONTROLS.json`. The second checks the audit inventory, author packet identities, all author manifest entries, and consistency of the acceptance record. An alternative author-packet directory can be supplied to the second command with `--author-public`.

`SOURCE_METADATA.json` records public citations, exact inspected PDF hashes and sizes, inspection history, and access limitations. No copied scholarly PDF, extracted source text, dataset content, or private coordination record is included. `MANIFEST.json` inventories the public audit files but excludes itself; its digest must be authenticated separately.
