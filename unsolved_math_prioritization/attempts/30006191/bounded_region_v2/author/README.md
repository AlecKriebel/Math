# Bounded-region continuum-fermion counterexample

Problem 30006191 / OWR-14299085-005, revision 2.

`BOUNDED_REGION_PROOF.md` is a self-contained author-stage proof for a fixed bounded interaction region and a smooth compactly supported potential. It covers the density-density and normal-ordered conventions. The norm discontinuity is witnessed by explicit varying Slater states, with maximal limiting norm difference 2.

This replaces the earlier blanket prior-result disposition: a full-space theorem alone did not settle the bounded-region formulation. The earlier author packet is preserved separately and has not been silently rewritten. The new proof does not depend on that theorem. Background credit and the original problem's public sources are retained.

Run `python verify.py` for finite Slater-moment, phase, algebraic, scaling and integrity checks. Optional source-byte validation is available with `--source-dir DIRECTORY`, pointing to PDFs with the filenames in `SOURCE_MANIFEST.json`. The checks are sanity tests; the analytic proof establishes the infinite-dimensional statement.

`AUTHOR_MANIFEST.json` freezes the author files. The proof is one substantive mathematical approach and remains subject to two independent audits before publication. No priority claim or publication action is contained in this packet.
