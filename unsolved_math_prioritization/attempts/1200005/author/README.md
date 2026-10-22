# Short laws for finite binary-tree automorphism groups

**Target:** 1200005 / AMR-011-0005, ranked 755.

**Disposition:** The full shortest-law problem is unresolved by this investigation after five substantive approach checkpoints. No complete candidate, general asymptotic determination, verified prior resolution, or historical novelty claim is made. Fresh independent review is required before publication.

The source is Miklós Abért's *Some questions*, dated November 2, 2010, Question 5, credited there to Abért and Bálint Virág. It concerns the full automorphism group of a finite rooted binary tree of depth n, equivalently the n-fold iterated permutational wreath product of C2. Its suggested optimum is the power law of length 2^n. The imported asymptotic wording is weaker than the exact-length question in the source.

## Results and limits

- Complete elementary proofs of exponent 2^n, the exponent-sum obstruction, evenness and monotonicity of the minimum, and centrality of all 2^(n-1)-st powers.
- A credited constructive lower bound: every nonempty reduced word of length at most n has a counterevaluation in depth n. Thus n < L_n <= 2^n.
- An exact recursive law criterion, including counterevaluation extraction and an independent leaf-permutation evaluator.
- L_1 = 2, L_2 = 4 and L_3 = 8, allowing any finite number of variables.
- An exact finite computation proves L_(4,2) = 16 for words in two variables. It does **not** prove L_4 = 16 when arbitrarily many variables are allowed.
- A literal claim that a nonempty root section can always be chosen with at most half the original word length fails for the commutator. The central-power commutator construction gives length 2^n + 2, which does not improve the power law.

The known linear lower bound and exponential upper bound remain far apart. Finite-depth computations do not establish an asymptotic law. All claims are scoped in `PROOFS.md` and `RESEARCH_LOG.md`.

## Reproduce

Python 3.10 or later, standard library only; no network is needed.

    python verify.py

This verifies the allowlist and all bound bytes, reruns the exact controls and requires byte-identical output. `python controls.py` prints the control results separately. The checker does not mechanically certify the written general proofs or worldwide literature status.

`SOURCE_VERIFICATION.json` contains public-source identities, inspected locations, public corpus hashes and bounded repository-search observations. It contains no PDF, extracted source text, raw imported record or private coordination.

This is AI-assisted, unrefereed research documentation, not external human peer review.
