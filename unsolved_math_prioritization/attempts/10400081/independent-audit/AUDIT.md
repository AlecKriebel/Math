# Independent audit: boundary-parallel surfaces and integral skein torsion

## Verdict

**PASS WITH TWO SCOPE CORRECTIONS. Recommended disposition: unsolved, five substantive approaches.**

The eight numbered propositions and the abstract-module countercontrols withstand this audit. The manuscript does not resolve Ohtsuki Conjecture 4.3 and does not exhibit a manifold counterexample. Two unnumbered applications need their compactness hypotheses made explicit; exact replacement text is in `CORRECTIONS.json`. These corrections leave all finite controls and the unsolved disposition unchanged.

This audit concerns the author manifest with SHA-256 `5f6837c610501e405a7698acb4e5b66a2535a397157aec35fbabae371e8c4479`, and the 23,640-byte author archive with SHA-256 `e876882ef9e4ae229fd4110bd1390e021db3726b7423ee44816c294efdbbb44d`. All nine listed payload files match their lengths and hashes; all ten archive entries, including the manifest, match the corresponding frozen files exactly. The author originals were not modified.

## Target and convention

The original source uses the integral Laurent ring `R = Z[A,A^-1]`, unoriented framed links in an oriented three-manifold, the crossing coefficients `A,A^-1`, and the circle value `-A^2-A^-2`. The printed page 446 was independently rendered and visually checked, including the diagram and conjecture. Its preceding discussion includes essential spheres; omitting them would admit the known torsion example `S^1 x S^2`. Conversely, ordinary spheres bounding balls cannot reasonably be treated as forbidden incompressible surfaces. The packet states its two-sided interpretation and does not silently infer a one-sided convention or compactness from the original sentence. [Ohtsuki, Section 4.1](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf)

The weaker properties “atoroidal” and “non-Haken” without a separate irreducibility condition are not substituted for the full surface condition. For the closed reduction, the stated conclusion is irreducible and non-Haken, with two-sided surfaces understood.

## Mathematical checks

### 1. Surface-product normal forms

The state-sum construction defines mutually inverse maps between the skein module of `F x I` and the free module on essential multicurves. The Reidemeister-II coefficient is `A^2+A^-2+delta=0`; the Reidemeister-III residual coefficient is `A+A^-1 delta+A^-3=0`; the framing multipliers are units. No nonunit is divided out. The result agrees with the product theorem in Przytycki, Theorem 2.3(b). The manuscript correctly identifies arbitrary two-handle slide quotients as the obstruction to extending this proof. [Przytycki](https://arxiv.org/abs/math/9809113)

### 2. Spherical filling and directed exhaustions

The three-handle invariance agrees with Przytycki, Proposition 2.2(2)(i). The topological forward reduction is valid: move a compact surface away from each filling center and into the original manifold; any compressing disk there would also be a compressing disk after filling. A sphere parallel to a capped sphere would bound a ball after filling. A positive-genus boundary-parallel surface remains parallel to an uncapped boundary component. Thus spherical boundary filling preserves the stated hypothesis in the asserted direction.

For directed exhaustions, generators and any finite certificate of a relation have compact support. The asserted filtered-colimit description follows. If a nonzero `f` kills a colimit class, the equality is witnessed at a later stage; torsion-freeness at that stage makes the representative zero. No injectivity of bonding maps is needed. Nested solid-torus exhaustions therefore give a genuine noncompact special case. They do not imply freeness, nor do they handle every compact small manifold. Arbitrary puncturing is correctly not claimed to preserve the literal sphere hypothesis.

### 3. Specialization and invisible torsion

Over `P = Q[A,A^-1]`, each cyclic torsion block contributes one dimension at a root of its annihilator, independently of its exponent. The proof and Jordan-block controls are correct. In particular, `P/(A+1)^e` has fiber dimension one but rational vector-space dimension `e`. This distinction avoids the unjustified identification appearing in a displayed step in the inspected proof of DKS-small, Theorem 3.1. The reduced-case conclusion used here remains justified by the generic-rank lower bound together with the correct fiber-block count.

The literature application must expressly retain **closed M**, as specified by DKS-small, Theorems 1.1 and 3.1. That is correction C1. The `A -> -A` symmetry is supported by DKS-small, Remark 2.3, citing Barrett; a pinpoint citation would improve the manuscript. [DKS-small](https://arxiv.org/abs/2305.16188v3); [Barrett](https://arxiv.org/abs/gr-qc/9512041)

The diagnostic examples are exact:

- `R/(A-2)` is the nonzero ring `Z[1/2]`. It has no integer torsion, but its nonzero generator is killed by `A-2`. Every root-of-unity fiber and the rational formal fibers at `A=+/-1` erase this summand.
- `R/(2,A-1)` is `F_2`. Its nonzero generator is integral torsion and vanishes after every characteristic-zero base change, including all complex fibers.
- `P[x]/(x^2-(A+1))` is free on `1,x`, although its `A=-1` fiber has a nonzero nilpotent.

None is presented as the skein module of a manifold satisfying the hypothesis. Consequently these are failures of algebraic inference, not counterexamples to the topological conjecture.

### 4. Rank-matched integral generators

For a surjection `D^r -> N` over a domain with generic rank `r`, the localized map is an isomorphism. Its kernel lies in `D^r` and maps to zero in `Frac(D)^r`, whose natural inclusion is injective. The kernel is therefore zero. This does not require a PID or finite presentation.

For figure-eight `1/q` fillings, `q != 0`, DKS-small Theorem 1.3 excludes none of these slopes from rational-Laurent finite generation and includes them in reducedness. Its Theorem 1.5 gives `4|q|` after including the odd-numerator correction and abelian contribution. The packet's simplified arithmetic is correct. An integral spanning set of exactly that size would prove freeness; a generic basis alone does not provide such a set.

The Seifert source separates integral finite generation, freeness, and torsion-freeness in Proposition 2.1; the independently rendered diagram has no implication from finite generation to torsion-freeness. Theorem 5.15 supplies a basis over `Q(A)`. These coefficient restrictions are preserved. [DKS-Seifert](https://arxiv.org/abs/2405.18557v2)

### 5. Saturation, arithmetic torsion, and determinants

For any free module `F`, including infinite rank, the equalities `Tor(F/J)=J_sat/J` and `J_sat=F intersect (K tensor J)` are correct: membership in the fraction-field span is a finite expression whose denominators can be cleared. Absence of both integer torsion and polynomial torsion after rationalization is exactly equivalent to integral torsion-freeness. Over the Laurent UFD, injectivity of multiplication by each irreducible is sufficient and necessary.

The height-one-localization warning is important and correct. No height-one prime contains both `2` and `A-1`, so `R/(2,A-1)` disappears at every height-one localization despite being nonzero. Coprimality of annihilators is not a unit-ideal certificate in this ring.

For a full relation matrix of fraction-field rank `q`, a selected nonzero `q x q` minor gives an integral adjugate certificate annihilating every torsion class. The remaining rows are valid because the selected columns span the full fraction-field column space. The zero-rank case is separately free. Unit maximal-minor ideal is sufficient, not necessary: the cokernel of the column `(A-1,2)` is the proper nonprincipal ideal `(2,A-1)`, hence torsion-free but not free.

A terminating confluent monic rewriting system for the full relation submodule also gives the claimed free normal form. A rational rewriting system obtained by dividing by `A-2` does not have this integral consequence.

The handlebody-slide formulation must expressly retain **compact M**. For a possibly noncompact M, use its free framed-link presentation instead. That is correction C2; Proposition 6 itself needs no change.

## Primary-source status checks

All nine available source PDFs were independently hash-checked against the frozen metadata. Text was independently extracted again from their bytes and matched the corresponding author extraction. The audit separately inspected the assumptions and relevant theorem statements, rather than treating hash equality as mathematical evidence. No source PDF, source text, or rendered source page is included in this audit package.

- Belletti–Detcherry's inspected Theorem 1.5 and its Section 6 prove an implication from the existence of a closed non-boundary-parallel surface to torsion. The arXiv and publisher abstracts advertise an equivalence. The publisher body is purchase-restricted; the audit does not infer a verified converse from that abstract. The original conjecture's direction was visually checked independently. [Preprint](https://arxiv.org/abs/2406.17454v1); [publisher metadata and abstract](https://academic.oup.com/imrn/article/2025/21/rnaf333/8315094)
- The August 2026 Kalfagianni examples explicitly have a nonseparating incompressible surface. They are outside the target's hypothesis, and their generic rank computations are over `Q(A)`. [Primary record](https://arxiv.org/abs/2608.12668v1)
- Detcherry's September 24, 2026 revision is indeed version 2, with an order-two-deformation correction. The inspected result concerns nonreduced character schemes, not a universal integral torsion-freeness theorem. [Primary record](https://arxiv.org/abs/2602.08760)
- Belletti–Detcherry's effective finiteness theorem localizes both the coefficient parameter and chosen boundary curves. Its own Remark 1.4 explains that a nonzero module can become zero. It does not supply integral localization injectivity. [Primary record](https://arxiv.org/abs/2507.02589)
- The inspected Farajzadeh-Tehrani–Frohman–Kania-Bartoszynska preprint concerns root-of-unity localizations and generic dimensions. The publisher abstract's broader hypotheses were not promoted to an uninspected final theorem. [Preprint](https://arxiv.org/abs/2402.17037); [publisher abstract](https://ems.press/journals/qt/articles/14298917)
- Chen's abstract targets the atoroidal question. It does not establish that the examples have no non-boundary-parallel closed surfaces of every genus. No such implication is imported. [Primary record](https://arxiv.org/abs/2311.01177)

Current primary records were rechecked on 2026-10-04. These checks provide bounded status evidence, not an assertion that every possible later source or final journal proof has been inspected.

## Computational evidence

1. The frozen verifier was run independently and passed **7,396** assertions. Its complete stdout is byte-identical to the frozen `CONTROL_RESULTS.json`, with SHA-256 `0cf2ee1d6b17e934e6037ae9928b91cc9f166ad15b901d906395a148b100d292`.
2. A separate standard-library verifier, importing no author code, passed **13,864** assertions. It uses geometric-series Bezout certificates rather than the author's cyclotomic implementation; finite-field residue tests include negative Laurent exponents and several characteristics; rectangular determinantal tests consider all nonzero rank-two row/column selections; and an explicit polynomial presentation contains genuine integer torsion. It also checks the free deformation with a nonreduced fiber and the nonprincipal-ideal syzygy.
3. These are exact finite controls. They neither compute an unknown manifold skein module nor prove the completeness of a proposed manifold presentation. Numerical counts are not a substitute for the arguments audited above.

## Required action and stopping point

Apply C1 and C2 to any revised proof, or distribute the correction overlay with the frozen packet. Preserve the distinction between the audit verdict and the conjecture's mathematical status. The remaining bridge is a theorem deriving full integral saturation, or an equally strong injectivity/normal-form criterion, from the all-closed-surfaces hypothesis. No such bridge and no admissible manifold counterexample has been produced.
