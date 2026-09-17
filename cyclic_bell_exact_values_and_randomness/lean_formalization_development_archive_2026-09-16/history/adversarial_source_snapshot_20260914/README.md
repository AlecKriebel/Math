# Cyclic Bell Lean companion — source candidates only

**UNCOMPILED. No kernel-certified endpoint is claimed.** This archive contains
the accumulated d=4, all-dimensional, model-value, support, randomness, binary,
setting and appendix proof-source candidates, with an adversarial optimization
extension and a recorded source-dependency repair.

Start with `REVIEWER_GUIDE.md`, `COVERAGE.md`, `OFFLINE_HANDOFF.md` and the four
statement contracts. The canonical manuscript is not modified or bundled here.

From this directory, with the exact Lean/Lake toolchain installed:

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

Pinned Lean 4.19.0 and all dependency commits are included as lockfiles, not
binary distributions. The default build imports 76 Lean source/audit files.
1,479 generated axiom queries and 21 offline controls are prepared, not run.
Static and exact arithmetic logs cannot be substituted for kernel checking.

New endpoints give the actual model-indexed value-conditioned guessing lower
bounds for both families, fixed finite-Eve POVM maximum existence, its nested
finite-q supremum interpretation, d=4 entropy upper bounds and source Fourier
coefficient/qutrit identities. They do not determine the unknown worst-case
adversary or formalize every remaining appendix/model-inclusion statement.

The only old mathematical edit moves unchanged `dimension_pos` from the witness
module to a shared upstream module, repairing a detected missing dependency.
All other previous mathematical modules and dependency pins are preserved.
Previous delivery reports under `history/` describe their own snapshots.

No Lean invocation, remote push, external correspondence, manuscript/qubit edit,
GitHub release or DOI occurred in this continuation. The package remains for
explicit offline checking, repair and independent statement review.
