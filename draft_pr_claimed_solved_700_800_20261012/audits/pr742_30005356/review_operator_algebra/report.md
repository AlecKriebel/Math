# Independent operator-algebra audit — PR 742 / problem 30005356

**Verdict: the frozen governing proof gives a valid counterexample to the literal, unrestricted-characteristic integral polynomial assertion.** I found no fatal algebraic gap and no characteristic-zero restriction in the designated original sources. The strongest verified conclusion is a negative universal answer plus an injective inclusion Z[1/p][θ] into the definable multiplicative endomorphism ring in positive characteristic. The proof does not classify that ring and does not resolve the characteristic-zero question. Novelty and exhaustive priority remain unassessed.

The audit inspected `author/PROOF.md` first, then reconstructed the deductions and consulted the designated primary sources. No old audit report or code was read. The frozen input SHA-256 and source receipts are in `input_receipt.json` and `source_metadata.json`. All authored artifacts are contained in this review folder; no outside communication, Git mutation, PR action, or publication occurred.

## Exact target and scope

The target tested was: for every ACFH model (K,θ), every first-order definable multiplicative group endomorphism of K× belongs to the image of Z[X] under X↦θ. A valid negative result needs one admissible model and one admissible definable endomorphism outside that image. The proof actually supplies such an endomorphism in every positive characteristic and every model in that characteristic.

The [OWR contribution, printed pp.97–98](https://ems.press/content/serial-article-files/46996) defines the base theory using algebraically closed fields with a multiplicative map and states the integral polynomial question without a characteristic condition. Its surrounding discussion does not restrict the question to characteristic zero.

The [versioned d’Elbée paper](https://arxiv.org/pdf/2212.02115v4), notation pp.6–7 and §3.3, treats positive characteristics; Corollaries 3.15–3.16 identify existentially closed models and ensure admissible extensions. Section 5.1, pp.22–23, defines the ring using definable group endomorphisms of K×. Corollary 5.7 and Question 5.8, p.25, supply faithfulness and the equality question. I found no nearby or global characteristic-zero convention. The notation change to Endd(K,θ) in the question is read using that explicit preceding definition.

This source reading does not establish unstated author intent. If the intended research target is the characteristic-zero classification or a repaired positive-characteristic equality, the PR must be described as the narrower negative result. No direct known-resolution statement was found in the inspected primary passages; no broader priority search was performed.

## Mathematical verification

The essential issue is the characteristic of the **endomorphism ring**, not the characteristic of the field. The ring's additive zero is x↦1 and its integer p is x↦x^p. On an infinite algebraically closed field these integer operators embed Z faithfully. In particular, p is a nonzero central unit in the full endomorphism ring in characteristic p, while p is not a unit of the faithfully embedded Z[θ]≅Z[X]. Its definable inverse must therefore lie outside Z[θ].

I independently proved the following in `derivation.md`:

1. Unique p-th roots define a parameter-free field automorphism ρ. It commutes with every multiplicative group endomorphism, including a noninjective and nonadditive θ.
2. If ρ=P(θ), then pP−1 annihilates the group. Integral polynomial faithfulness makes this impossible because its constant coefficient is −1 modulo p.
3. A direct existential monomial witness proves nonmembership without quoting faithfulness. A divisible-group extension constructs an admissible operator extension with any finite independent orbit t₀,…,t_d. The relation demanded by ρ=P(θ) then has exponent pa₀−1 on t₀ and cannot hold.
4. The same construction proves the claimed faithful evaluation in every characteristic. Its group-extension proof does not require θ to be additive, injective, or onto, and handles every integer exponent and degree zero.
5. Inversion of p forces the faithful inclusion Z[1/p][X]→E. Scalar units are exactly ±p^r in positive characteristic; other primes have nontrivial root-of-unity kernels. This supplies a necessary coefficient enlargement, with no surjectivity/classification claim.
6. A valuation argument distinguishes pure-field definability of ρ from rationality or regularity. The source ring admits first-order definable functions, so the inverse map's failure to be rational is irrelevant to its admissibility.

No circular use of the desired classification is present. The only model-theoretic assumption used in the independently reconstructed monomial proof is existential closedness in the stated base theory. An arbitrary algebraically closed extension with a multiplicative operator is sufficient; it need not already satisfy ACFH. Negative coefficients are ordinary inverses in K×, not fractional powers. Characteristic two does not collapse operator [-1] with [1].

## Adversarial mechanisms and exact gaps

| Mechanism | Evidence and status | Remaining gap |
|---|---|---|
| Central scalar unit obstruction | Complete deduction: p is invertible in E and a nonunit in faithful Z[θ] | None for the counterexample |
| Direct independent orbit construction | Complete existential witness; all integer signs and d=0 checked | None for faithfulness/nonmembership |
| Definability versus regularity | Quantifier-free graph; rational-function valuation obstruction | None for source's definability interpretation |
| Inverting primes besides p | Nontrivial ℓ-th roots for ℓ≠p rule out scalar inverse | No classification of possible nonscalar endomorphisms |
| Nongeneric θ=ρ | Exact algebraically closed base-theory counterexample to dropping genericity | Shows the extension/faithfulness input is essential |
| Characteristic-zero route | Unique p-th roots no longer available | Full characteristic-zero equality remains open in this work |
| Equality after replacing Z by Z[1/p] | Necessary inclusion established | Equality with E is completely unproved |
| Priority/novelty | Designated sources checked; no direct resolution statement there | Exhaustive literature audit not assigned or performed |

A route claiming a full endomorphism classification from centrality/localization alone is blocked: it simply replaces the central difficulty by an unsupported assertion that all definable group homomorphisms lie in the localized polynomial subring. No such route is used by the governing proof.

## Reproducible negative controls

Run `python3 controls.py`. The saved receipt covers GF(4), GF(8), GF(9), and GF(25), exhaustively checking the finite-field arithmetic relevant to the tested identities, inverse Frobenius, centrality under all finite power endomorphisms, and integer powers −7 through 7. It also checks 14,000 bounded coefficient examples of the nonzero constant coefficient of pP−1.

These finite structures deliberately fail the ACFH/genericity requirement. In every finite case inverse Frobenius is an integral power, and choosing θ=ρ makes pX−1 vanish. In GF(9) and GF(25), θ(x)=x² is both nonadditive and noninjective. Thus the controls would catch a proof that improperly inferred faithfulness from multiplicativity, reduced coefficient integers modulo the field characteristic, or promoted finite computations into ACFH evidence. The unrestricted integer congruence and existential construction, not these tests, prove the theorem.

## Disposition

Accept the proof as a rigorous negative answer to the literal unrestricted-characteristic Z[θ] question, while retaining its explicit limits. Do not promote it as a full characteristic-wise classification or as a novelty certificate. No mathematical repair is required for its stated counterexample. No outside input or outreach was used or prepared. Private downloaded PDFs/text were removed after metadata extraction and scope verification.
