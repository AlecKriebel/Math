# Reviewed counterexample to the literal numerical threshold classification

**Current disposition: claimed_solved, author turn 1/5, for the literal numerical classification only. Separate full adversarial AI review PASS.**

The unchanged proof gives a connected colored Gaussian graphical model on K4,4, with two concentration diagonals tied, for which I(G,4)=0, I(G,3) is nonzero, and WMLT=2. The singleton-color model is also a counterexample and additionally has the known classical MLT=4. The source's proposed numerical scenarios at n=3 require weak threshold 3 or 4, so they are not exhaustive as stated.

The proof does not refute or settle a repaired pure Boolean SOS-versus-positive-definite-intersection alternative: the example lies in the second intersection and refutes its numerical threshold conclusion. It also does not settle an unstated restriction to colored four-cycles. The displayed source definitions and proposition do not impose that restriction, although nearby examples concern four-cycles. These are mandatory scope boundaries.

The sample convention is a zero-mean Gaussian with rank-indexed sample scatter, up to irrelevant positive scaling. The positive-probability assertion uses an open data box with strictly positive Gaussian density, not just an exceptional rank-two witness. Exact Jacobian minors establish vanishing of I(G,4), and a nonzero cross-block determinant belongs to I(G,3).

The independent audit is `independent_review/FINAL_REVIEW.md`. The 188 author checks replay byte-for-byte; a separate checker passes 1,808 exact assertions. No numerical simulation is used. Blekherman and Sinn's ordinary K4,4 MLT theorem and the classical likelihood-completion criterion are credited. This is a source correction/classical consequence, with no novelty or human-peer-review claim.

Frozen pending-review language records the earlier checkpoint; this file gives the current reviewed disposition. PUBLICATION_MANIFEST.json binds the assembled package. Completion estimate: 100% of the source-literal counterexample and independent-review draft deliverable.
