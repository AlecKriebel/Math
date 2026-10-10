# Independent mathematical audit: proper partial twists and Rouquier parity

## Verdict and exact target

**ACCEPT as a proved, narrowly scoped partial result for AIM problem 2.1 (20000079 / AIM-ALGEBRAIC_GEOMETRY-0079).** No unresolved mathematical gap was found in the audited theorem or the additional single-step Jucys–Murphy counterexample. This is not a novelty certificate and is not a solution of the general AIM question.

Audited proof title: *Positive partial twists can destroy parity permanently*.

The distributed [mathematical report](MATHEMATICAL_REPORT.md) has 14,199 bytes and SHA-256 `d6050364f352c57a26b6c80bc7ffe59b64b4760b726f1a00123ceebe747d86cf`. Its complete symbolic proof is preserved. This AI-assisted, unrefereed audit is not external human peer review, journal acceptance or formal proof-assistant certification.

This verdict applies to that exact proof, over **C**, for the raw Hogancamp–Mellit Rouquier/Hochschild-cohomology convention it specifies. Write s=σ1, r=σ2, γ=rsr²s²r², and γ_k=γs^(2k). The accepted conclusions are:

1. γ is even in Rouquier degree.
2. γ_k is mixed in Rouquier parity for every integer k≥1.
3. Every ordinary unreduced Euler series χ(γ_k), expanded in q at zero in the stated convention, is coefficientwise nonnegative.
4. Multiplication by the displayed fixed positive Jucys–Murphy braid fails to preserve parity in one explicitly identified example. No all-power Jucys–Murphy assertion is accepted or needed.

The twisting in items 1–3 is the proper two-strand full twist s² inside B3. Replacing it by the central full twist (sr)³ would change the theorem and is not justified.

## 1. Conventions, source dependencies, and local finiteness

I inspected Hogancamp–Mellit, *Torus link homology*, arXiv:1909.00418v1, particularly its PDF pages 3, 9 and 10, and Turner, arXiv:2410.03068v1, PDF page 1. These verify the positive-torus parity input, the degree-zero placement of R in the positive Rouquier complex, the positive Markov convention, and the independent variables q=Q² and a=AQ^−2. The parity variable is the original Rouquier variable T, rather than the derived variable t=T²Q^−2.

The proof uses Hochschild **cohomology** termwise. In the positive crossing complex D_i→R, D_i occurs in degree −1 and R in degree 0. Its Euler class is consequently 1−[D_i]. The unshifted bimodule D_i has tensor-square decomposition D_i⊕qD_i. This gives exactly

(g_i−1)(g_i+q)=0.

The trace normalization and the quadratic relation are therefore consistent. Neither an implicit crossing sign nor an A-dependent homological regrading has entered the calculation. All crossing complexes are bounded, with graded pieces locally finite; hence their coefficientwise Euler series and the expansion of (1−q)^−1 at zero are legitimate.

The source theorem supplies evenness of the starting torus braid. It does not assert that every positive braid is parity. Mixedness of later examples, once proved, is unchanged by any overall homological normalization shift.

## 2. The invariant-coordinate argument is sufficient

The proof avoids assuming that every operation called “reduction” has the required parity behavior. Let z=(x1+x2+x3)/3 and R0=C[x1−x2,x2−x3]. The displayed inverse coordinate transformation is correct. Both simple reflections preserve R0 and fix z. Consequently the invariant rings, Soergel bimodules, multiplication maps, and their tensor products split over the common factor C[z]. This establishes the stated factorization of positive Rouquier complexes.

The tensor product of the polynomial Koszul resolutions gives a natural termwise Hochschild-cohomology Künneth isomorphism. The C[z] factor has zero Hochschild differential after identifying its two actions. Its surviving factors are C[z] and an exterior generator θ with degree AQ^−2. Both have Rouquier degree zero. Taking Rouquier homology over a field preserves the tensor decomposition:

HHH_R(β) ≅ C[z]⊗Λ(θ)⊗HHH0(β).

Thus P=χ/U, U=(1+a)/(1−q), is genuinely the Euler characteristic of the explicitly constructed HHH0. It is not merely a convenient rational quotient. The tensor factor is nonzero, has a degree-zero unit, and carries only even Rouquier degree. Therefore HHH0 and ordinary HHH have exactly the same occurrence or nonoccurrence of each Rouquier parity. No knot-reduction nomenclature or identification theorem is needed for this implication.

This point is essential: the unreduced Euler series is nonnegative in this example, so its coefficients alone cannot establish mixedness.

## 3. Braid identities and knotness

Every RIII substitution in the five-word chain from (sr)^4 to γ checks exactly, and its only cyclic rotation is conjugation. Conjugation introduces no grading shift here. The starting closure is the positive (3,4) torus knot, so the credited torus theorem applies in the required convention.

All γ_k have the same permutation, the product of the two distinct adjacent transpositions, which is a 3-cycle. Appended squares do not alter it. All closures in the family are therefore knots. This check is independent of the coordinate-splitting argument.

The word γs² is a cyclic rotation of sr(sr²s)². I also inspected the K3 preliminary problem volume at page 38, where that braid is identified as the known positive knot 10_139. The proof does not depend on the source's nonparity assertion.

## 4. Independent exact trace calculation

The six trace values in the proof follow from the unlink value U³, positive Markov stabilization, cyclicity, and the quadratic relation. Their normalization checks, including the longest basis element:

τ(g1g2g1)=(1−q)U+qU².

For a separate algebraic replay, I used the two matrices

A=[[-q,1],[0,1]],  B=[[1,0],[q,−q]],

together with the one-dimensional characters g_i↦1 and g_i↦−q. These satisfy the braid and Hecke relations. A linear combination of their characters, determined from the identity, g1, and g1g2, reproduces all six basis trace values. The six-component representation consisting of the two scalar characters and four matrix entries has a nonzero basis determinant over Q(q), so it also checks the displayed six-basis expansion.

This replay verifies:

- Both factored six-basis coefficient columns in the report.
- Both explicit polynomials τ(Γ)/U and τ(Γg1²)/U before substituting U.
- The exact P0 and P1 after U=(1+a)/(1−q).
- D=P1−P0.

The multiplication table and trace polynomials make the initial values finite, hand-checkable identities. They are not assumptions justified only by a successful program run.

## 5. The infinite quantifier follows from an identity

The operator h=g1² satisfies (h−1)(h−q²)=0 directly from the original quadratic relation. Multiplication by Γh^k and application of the trace give

P_(k+2)=(1+q²)P_(k+1)−q²P_k.

The displayed solution P_k=P0+(Σ_(j=0)^(k−1)q^(2j))(P1−P0) obeys this recurrence and its two initial values. Induction therefore proves it for all k≥0. No interpolation, generic-specialization argument, eigenvalue division, or extrapolation from finite tests is necessary.

In Hochschild degree two it gives

[a²]P_k=q³Σ_(j=0)^(2k)(−q)^j.

For each k≥1, the coefficients at a²q³ and a²q⁴ are respectively +1 and −1. The change of variables sends these to distinct bidegrees A²Q² and A²Q⁴. A positive Euler coefficient requires a nonzero even class; a negative coefficient requires a nonzero odd class. The fact that both terms have the same A-degree also prevents the conventional replacement a↦−a from removing their sign disagreement. The coordinate factor then transfers both parities to ordinary HHH.

## 6. Unreduced sign coherence

The F0, F1 and F2 formulas in the report agree with the exact recurrence solution. Their decompositions show coefficientwise nonnegativity after division by 1−q:

- F0 already has nonnegative polynomial coefficients.
- Each potentially signed F1 block is 2q^m−q^(m+1), whose quotient by 1−q has nonnegative coefficients.
- Consecutive terms of F2 pair to yield q³Σ_(j=0)^(k−1)q^(2j)+q^(2k+3)/(1−q).

Multiplication by 1+a preserves nonnegativity. The k=0 case follows from the explicitly positive P0. This proves the third theorem assertion for every k, not merely the checked samples. It also correctly distinguishes the stronger obstruction from the reflection-reduced Euler polynomial from the weaker ordinary unreduced sign test.

## 7. Additional operation and scope

For L=sr²s, the word srL changes by two RIII moves to s³rs² and by cyclic rotation to s⁵r. Positive destabilization leaves the positive two-strand (2,5) torus knot without a homological shift. Appending one L yields srL², the known mixed k=1 case. Conjugation by the Garside half twist swaps s and r, proving the analogous single-step statement for rs²r. These are valid parity-preservation counterexamples.

The all-k result does not settle eventual central twisting. Nor does it contradict the adjacent pure-Coxeter/nested-initial-full-twist question: every product in that adjacent family is pure, whereas every γ_k has a 3-cycle permutation. No algebraic-knot assumption is made, and no general parity characterization is obtained. Distinct raw Euler polynomials are not asserted to prove distinct knot types without analyzing link-normalization shifts.

## 8. Review limits

**Remaining mathematical gaps in the stated partial theorem: none found.** Remaining open questions include the general characterization, central-full-twist preservation/eventual parity, and higher-rank nested-full-twist statements. The positive-torus theorem and known 10_139 example are credited prior work. The originality or publishability of this derived operation family has not been certified.
