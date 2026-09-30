# Independent review: K-trivial oracle depth reductions (30004669)

**Verdict: PASS_SCOPED_TT_TRANSFER_AND_SIMULATION_OBSTRUCTION.** No mandatory correction. Preserve **unsolved, 2/5** for the original noncomputable-oracle question.

Reviewed `PARTIAL.md` SHA256:
`38fd590eac83acc56e457f0ff761a65f8fe3ad3f947f42cb3519a8a7ced6ae16`.

This is an independent AI proof/source audit, not human peer review or a priority determination. The reviewer retained its inherited runtime; its exact model identifier was not exposed.

## 1. Definitions and quantifiers

I checked the original OWR contribution and the full published BDRM article, especially Definitions2.1,2.10 and3.1. The artifact uses prefix-free K and **ordinary computable nondecreasing time bounds depending on output length**. It does not permit arbitrary A-computable bounds. BDRM Section3 explicitly distinguishes that alternative. The source also assumes an efficient universal simulator; the artifact correctly allows a new computable bound after simulation rather than identifying machine deadlines.

For a fixed t, failure of the gap to tend to infinity means that some finite b bounds the gap at infinitely many lengths. Thus the stated shallowness formula has exactly the required order

    exists t, exists b, for infinitely many n.

Neither an eventually-everywhere bound nor a uniform choice of near-optimal descriptions is required. K^A(σ)=K(σ)+O(1) is uniform in finite σ but has constants depending on the fixed oracle A. It is not a time-bounded simulation theorem.

The computable-oracle equality follows by effective oracle-answer simulation. Consequently a literal assertion of strictness for every K-trivial oracle would already fail on computable oracles; the unresolved cases under discussion are noncomputable ones. The artifact makes this distinction rather than claiming that a new noncomputable example is known.

## 2. Truth-table transfer direction

The hypotheses A<=tt B and K^A<=K^B+d imply that A-shallowness transfers to B-shallowness. Indeed, BDRM Lemma2.2(ii) gives, for the chosen A-time bound t, a fixed ordinary computable s and fixed description overhead c. Along the infinitely many witness lengths,

    K^(B,s) <= K^(A,t)+c <= K^A+b+c <= K^B+b+c+d.

All constants are independent of n. Taking contrapositives gives D^B subset D^A, in the direction stated in the artifact. K-triviality of both oracles supplies the needed unbounded comparison via lowness for K. It is not supplied by A<=T B alone: that reducibility directly gives the opposite complexity inequality.

The consequences also have the correct directions. If D^B=D and D^B subset D^A subset D, then D^A=D. If X belongs to D but not D^A, it also fails membership in D^B. This is the same witness, not an existence argument requiring a new X. Equality does not automatically transfer upward.

## 3. The c.e. cover is genuinely truth-table

I read and visually checked Nies's Theorem7.4 on printed p.301. It states that every K-trivial A is truth-table reducible to a c.e. K-trivial D; the source even states a polynomial-time truth-table reduction under its encoding. This is strong enough for the time-bounded simulation. The proof's bounded change-record construction and parity convention agree with the artifact's use.

By contrast, the later Solovay-function proof's Corollary4.13 gives Turing reducibility. Its introduction explicitly calls this weaker than Nies's truth-table theorem. The artifact does not substitute that weaker cover.

The resulting equivalences of the two existential/universal questions are sound. A c.e. cover of a noncomputable A cannot be computable, since A<=tt B implies A<=T B. This remains an existential reduction; no effective uniform procedure choosing covers or lowness constants for all A is asserted. The earlier cost-function and golden-run results are credited dependencies and were not independently reconstructed in this review.

## 4. Nonuniform comparison versus a uniform compiler

Condition(7) is sufficient for the missing class inclusion, exactly as proved. Its quantifiers allow s and c to depend on the fixed t and oracle. No effective procedure mapping t to s is assumed. On an A-shallowness witness, K^A<=K+O(1), obtained simply by ignoring the oracle, completes the implication to ordinary shallowness. Necessity is neither proved nor needed.

The output-preserving compiler obstruction is also correct. The unary programs p_n form a computable prefix-free family. A single oracle machine prints the first n oracle bits within an ordinary time bound uniform over all oracle answers; the universal simulation adds a computable overhead. If a partial computable translator were defined on every p_n and produced an ordinary halting program with that same output, computing A(j) would require only computing p_(j+1), running the translator, running its output program and reading bit j. Each stage halts under the assumption, contradicting noncomputability of A.

This argument does not depend on an upper bound for output program length. Conversely, an existential inequality between minimum program lengths supplies no computable translator. Thus the compiler obstruction does **not** refute condition(7), class equality, or every possible depth-preservation proof. The artifact preserves all three distinctions.

The correct-stage variant uses a uniformly computable approximation (A_s), as its proof expressly requires when inspecting A_(g(n)). For computable unbounded u, searching for some n with u(n)>j terminates even without monotonicity. A computable g providing the exact prefix at that stage would then compute A. This rules out that uniform mechanism only.

## 5. Restriction on a strictness witness

Nies Theorem6.1 gives downward closure of K-triviality under Turing reducibility. Moser–Stephan Theorem4.6 shows K-trivial sequences are not O(1)-deep_K. I checked that their Definition1 defines O(1)-deep_K using every constant significance and eventual domination, matching the depth notion here. Therefore a witness X in D minus D^A cannot satisfy X<=T A. The fact that a sequence is A-shallow does not furnish a uniform oracle procedure for its prefixes; the artifact does not make that erroneous inference.

## 6. Controls, verdict and remaining gap

All **6,534** author assertions replay byte-identically. A separate checker passes **6,200** bounded assertions, including four-point inclusion models, additive-gap chains, adaptive truth-table composition, variable change-record blocks, prefix-free codes, and nonmonotone unbounded-use search. An abstract countercontrol confirms that simulation inequalities alone, without the unbounded-complexity comparison, do not imply the gap inequality. It is not an actual oracle counterexample.

These finite controls evaluate no genuine Kolmogorov complexity and decide no infinite depth property. The substantive conclusions rest on the written quantifier arguments and credited source theorems. They give no noncomputable oracle with equality or strictness, no necessity theorem for condition(7), and no uniform cover-selection algorithm. No gap was found in the stated partial deductions; the original classification remains unresolved.

### Primary sources

- Original OWR contribution: https://ems.press/content/serial-article-files/46899
- BDRM, published *Relativized depth*: https://iris.uniroma1.it/bitstream/11573/1713789/1/relativized-depth.pdf
- Nies, *Lowness properties and randomness*: https://www.cs.auckland.ac.nz/~nies/papers_till_09/Nies_LownessPropertiesRandomness.pdf
- Solovay-function cover comparison: https://arxiv.org/abs/1603.08351
- Moser–Stephan, *Depth, highness and DNR degrees*: https://dmtcs.episciences.org/4012
