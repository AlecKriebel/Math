# Additive editorial clarifications after independent audit

The frozen author and audit files are preserved byte-for-byte. These notes clarify two points without changing a mathematical conclusion or adding a sixth research approach.

1. **Homology verifier comment.** The comment at checks/check.py line 46 says the relation matrix is “row-equivalent” to its diagonal form. The code actually right-multiplies by an integral determinant-one matrix, hence performs a **column operation**. “Column-equivalent” or “unimodularly equivalent” is the correct description. The implemented calculation, the cokernel, and the proof in RESULT.md are unchanged.

2. **Proposition 4.3 hypotheses.** Restate explicitly the hypotheses inherited there from the preceding setup: `W` is a real `4 x 2` matrix of **rank two**, `A` belongs to **GL(2,Z)** (so `det(A)=+1` or `-1`), `P` is a permutation matrix, and both real scaling factors are nonzero. Under these assumptions, `t W=s P W A` implies `|t|=|s|` and that `A` has finite order. Rank-one models or nonunimodular matrices are outside the proposition.

The full arbitrary-gluing problem remains **unsolved 5/5**. The independent audit's verdict is PASS_SCOPED_PARTIAL, not a full-solution certificate.
