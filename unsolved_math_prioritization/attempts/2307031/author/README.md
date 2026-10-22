# Function Theory 7.31 partial results

This authored package concerns UnsolvedMath 2307031 / AMR-022-7031.

Main candidate result: the comparison between sum f(n^2) and
sum f(c_n/a_n) fails even when f is positive, entire, strictly decreasing,
strictly convex, and completely monotone on the positive real axis.
The proof uses a single explicitly specified recursive admissible sequence
and a single positive exponential mixture. It is an infinite proof, not
a numerical counterexample.

Additional candidate results are a uniform O_{a_1}(sqrt(T) log T) bound
on the number of c_n/a_n<=T, sharp in order over the admissible class, and
a sufficient weighted integral criterion beyond the source's power cases.

These are partial results on the open-ended classification. The broad
target is not claimed solved, and no novelty or priority is asserted.
Five substantive approaches are recorded. Independent audit is pending.

Files:

- PROOFS.md: complete authored mathematics and remaining gaps
- TARGET_SCOPE.md: primary target, exact quantifiers and status limits
- APPROACH_LOG.md: five approaches and bounded outcome
- SOURCE_VERIFICATION.json: public verification metadata and source limits
- verify.py: exact finite positive and negative controls, standard library only
- EXPECTED_CHECKS.json: expected deterministic verifier output
- verify_integrity.py: offline frozen-file and replay checker
- AUTHOR_MANIFEST.json: frozen authored-file hashes and byte counts

Replay from this directory:

    python3 verify.py
    python3 verify_integrity.py

Neither replay needs network access, source PDFs, copied scholarly text,
dataset content, or private coordination material. Publication eligibility
is limited to this authored directory after fresh independent audit.

Primary source: W. K. Hayman and E. F. Lingham, Research Problems in
Function Theory (New Edition), arXiv:1809.07200v2, Problem 7.31 and Update
7.31, printed page 169. https://arxiv.org/abs/1809.07200
