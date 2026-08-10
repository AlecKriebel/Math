# Final hard-cover clean-room review

## Active verdicts

- **VERIFIED:** corrected schema-3 n=4 theta-2 minimum-support base hard
  cover.  See `SCHEMA3_N4_THETA2_REVIEW.md`.
- **UNRESOLVED:** active p/q probe closure.  The only existing probe evidence
  binds a superseded n=4 base and is quarantined under `history/`.
- **UNRESOLVED:** n=3 merged hard-cover gate until its separate clean-room
  replay and report are complete.
- **UNRESOLVED:** the landmark global JC identifiability and one-sided
  containment theorem.

The n=4 verdict is bound to summary SHA-256
`915bed0a3add001c1a94d6d862a2359e6ad75b3489f8d71b7adf006952b5ce37`.
It independently closes 132 fixed roots, 2,106 states, 1,860 polynomial
separations, 114 refinements, and 132 labelled-isomorphism terminals.

The implementation regenerates exact rooted graph reductions, every path's
child set, complement-normalized displayed-tree descriptors, JC Fourier
tensors, and target-zero/source-nonzero polynomial pullbacks.  It does not
accept primary classification or sign flags as evidence.  Thirteen mutations
are rejected, including provenance merges, relation/polynomial swaps, and
both removal and incorrect application of split-complement normalization.
