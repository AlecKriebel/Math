# Independent final-referee minimality source check

Checkpoint: 2026-09-26T05:02:51Z. Completion estimate for this focused audit: 100%.

Scope: read the review manuscript's minimality proof and relevant definitions, then primary sources only. No round-one review or prior audit was read. No manuscript changes made.

**Finding: the cited inputs support the local-dimension-four minimum, conditional on the manuscript's dimension-four construction and tower identification. No missing hypothesis was found in the dimension-three exclusion.**

## Lechner input

[Lechner, arXiv:2603.20158v1](https://arxiv.org/html/2603.20158v1), Lemma 3.1, assumes a finite-dimensional unitary Yang–Baxter operator with exact spectrum {-1,q}, q unequal to ±1. Its tensor character is a positive Markov trace. No scalar-partial-trace or irreducibility assumption must be supplied separately: Proposition 2.4 deduces irreducibility from absence of opposite eigenvalues. Definition 2.2's footnote identifies its left-oriented Markov condition with the usual terminal-generator condition used in the manuscript. Theorem 3.4 gives precisely parameters 1/3, 1/2, 2/3 at q=exp(iπ/3), with dimensions divisible by 3, 2, 3 respectively.

## GHR input and generator normalization

[GHR, primary author PDF](https://people.tamu.edu/~rowell/GHRarx1.pdf), Definition 1.2 (preprint numbering, p. 2), requires injective algebra homomorphisms satisfying φ_n composed with ρ = ρ^(W,R). Section 5.6 (p. 25) explicitly gives eigenvalues -1 and exp(2πi/6), despite its separate inconsistent printed q convention. Lemma 5.26 rules out dimension two and checks the eigenvalue ratio even after arbitrary scalar rescaling. Its statement therefore applies to the manuscript's normalization. The manuscript already flags the q and Markov-parameter misprints in GHR.

## Independent inference and algebra check

For any hypothesized localization, evaluation at the braid identity forces φ_2(1)=I, even if “algebra homomorphism” were read without an a priori unital convention. Intertwining the literal braid generator forces φ_2(g_1)=F and hence its Hecke polynomial. The target's two nonzero spectral idempotents e_1 and 1-e_1 remain nonzero by injectivity. Thus F has both eigenvalues with the stated literal q; it cannot evade the theorem by losing a summand. Scalar rephasing would change the named sequence, and in any case preserves whether a localization of a given local dimension exists when applied uniformly.

The manuscript's elementary calculation is correct: for c=1/3 and T=e_1e_2e_1-ce_1, the Markov trace of T* T is (1-c)η(η-c). It vanishes at η=1/3 but equals 1/18 in the target η=1/2 quotient. Faithfulness of ordinary matrix trace on the represented image forces the hypothetical η=1/3 operator to kill T, contradicting localization injectivity. Complementing the projections replaces η by 1-η and gives the identical contradiction for η=2/3. At η=1/2, local dimension three would require rank 9/2. Dimension one cannot realize both eigenvalues.

There is no need to assume a localization preserves the target Markov trace: the candidate's trace is allowed to differ, and the two explicit kernel obstructions exclude the alternatives. This is the key distinction that makes the minimality proof work.

No remaining gap was identified within this audit's scope. The primary GHR document inspected is its author-hosted preprint; published-version numbering beyond Lemma 5.26 was not separately audited here.
