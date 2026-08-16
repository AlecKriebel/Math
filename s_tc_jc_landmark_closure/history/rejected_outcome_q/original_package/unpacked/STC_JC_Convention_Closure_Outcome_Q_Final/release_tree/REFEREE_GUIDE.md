# Referee guide: convention closure

The baseline `sd0` classification is frozen.  The only new mathematical question is whether the broader cleanup convention changes the theorem class.

## Load-bearing steps

1. **Root zipper lemma.** Cleanup is needed only when the root children are adjacent.  In a tree-child rooting they are a tree vertex and its reticulation child, and their external children are nonreticulate.
2. **Constructive quotient.** Contracting the zipper gives a binary LSA-valid tree-child `sd0` rooting of the same final mixed graph.
3. **Exact JC equality.** The zipper has nonzero Fourier multiplier `u v (lambda alpha beta + (1-lambda) gamma)` and has a strict analytic section over every edge multiplier in `(0,1)`.
4. **Class quantifiers.** Weak classes agree; the cleanup-strong class is a proper subset of the already-simple strong class because cleanup has more admissible rootings.
5. **Parallel frontier.** `(1,1,2)` is LSA-impossible; `(1,1,3)` has no tree-child rooting; longer cases clean to existing cycle factors.
6. **Sharpness.** The Theta pair is already simple, so cleanup changes neither graph nor model.

Run `bash reproducibility/verify_full.sh`, then inspect `docs/THEOREM_Q_PROOF.md` and the two independent C++ sources.
