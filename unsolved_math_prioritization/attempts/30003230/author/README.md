# Problem 30003230: divisorial contractions

**Result: UNRESOLVED in general. Five substantive approaches completed.**

This packet studies rank 732, OWR-14754-017, the strict decrease of the **algebraic** stringy Euler invariant under a divisorial Mori contraction. It does not claim a new solution or counterexample.

The primary projective, complex, normal, Q-Gorenstein, log-terminal setting is essential. The short dataset statement inherits that domain from the surrounding definition. The known finite-orbit-resolution and spherical results are not general results. A recent counterexample concerning stringy Hodge coefficients is a different question. The separate stringy-smoothness problem in PR #682 is not this problem.

## Included work

- `PROOFS.md`: five routes, proved special cases, exact reductions, and the remaining gap.
- `SOURCE_AUDIT.json`: public source metadata, exact statement hash and retrieval limits, prior-work checks.
- `CLAIMS.json`: machine-readable scope restrictions.
- `verify.py`: standard-library-only, exact rational arithmetic and determinant checks, with rejected false shortcuts.
- `RESULTS.json`: actual retained verifier output.
- `check_packet.py` and `MANIFEST.json`: byte-integrity and deterministic replay checks.

Run from any working directory:

    python /path/to/release/check_packet.py
    python -O /path/to/release/check_packet.py

The computations check formulas and finite examples, not the geometric hypotheses of arbitrary varieties. They are not formal proof certificates. The geometric arguments use explicitly identified standard results, including resolution independence, the smooth blowup cohomology decomposition, the toric stringy-volume formula, surface resolution/factorization, and the negativity lemma.

Only these authored files and public verification metadata are intended for review or later publication. No PDFs, extracted paper text, raw dataset rows, private history, or coordination material are included. No branch, commit, push, or PR was created for this packet. Fresh independent audit is pending.
