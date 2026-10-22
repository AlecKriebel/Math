# Independent audit: affine–Virasoro blowup normalization

Problem 30005075 / OWR-9790367-005. Audit date: 2026-10-03.

## Disposition

**PASS_PARTIAL:** the repaired finite-character normalization, all-integer sign/norm identification, and four-point sewing are correct as generic meromorphic/formal statements, conditional on the published BFT conformal-block relation (4.59) and the stated compatible multiplicative regularization.

**HOLD for a full, convention-specific certification of the gauge-theory equation.** The frozen packet does not identify the particular gauge partition functions, their four masses, defect coordinate, abelian factor, and perturbative normalization with its newly defined full conformal blocks. This is a genuine uncompleted identification, not a falsification of the intended blowup formula.

**Prior-work conclusion:** the original research direction is directly addressed by Bershtein–Feigin–Trufanov (BFT), published in 2025, whose introduction and section 4.6.2 explicitly claim the surface-defect blowup proof via AGT. It must be credited as substantive affirmative prior work. The result should not be described as newly solved here, or as demonstrably still open. This audit distinguishes that published coverage from an independently checked exact gauge-convention bridge. If “already solved” only records the existence of a directly applicable published result, BFT is the relevant result; if it certifies the entire displayed target in fixed conventions, this packet has not reached that standard.

No mathematical error was found in the repaired author equations (6), (9)–(18). One additional printed-source mismatch, B.7's interchange of the second and third weights, should be disclosed explicitly in any future revision. The author already uses the correct ordering, so this does not invalidate its derivation.

## 1. Frozen input and reproduction

The SHA-256 of the author MANIFEST.json is

`6c1444e73c64c5b5a2e9eaebda234d3befb997fbf209c7522377c02b0c4bbf4a`.

All 14 listed file lengths and hashes match. The author packet was not edited. Its verifier was run with bytecode writing disabled and reproduced:

- 42 finite-triangle character checks;
- 686 three-point product comparisons;
- 9 separate Laurent-character evaluations;
- 11 four-point sewing checks;
- the character residual, repaired splitting, grading, degree, and parity checks.

The new verifier `verify_independent.py` imports no author code. It independently transcribes the source coefficient formula and constructs the two chart numerators as sparse Laurent polynomials. It verifies their cleared-denominator equality to the finite-character expression on all 729 flux triples in [-4,4]^3, compares the resulting Euler products to the source formula at 1,458 exact parameter instances, and checks 17 sewings through flux ±8. One parameter set has positive K and the other negative K. These are exact rational computations, not floating-point comparisons.

The portable check requires Python 3 and SymPy, but no PDFs, network, or private corpus. Its adjacent-author integrity check is optional when distributed separately. `results.json` records its successful run. Finite checks supplement, rather than establish, the arbitrary-integer arguments below.

## 2. Primary-source verification

The original report was checked in extracted text and in a rendered image of printed p. 837, PDF page 21. It explicitly includes a surface operator. The target is the N_f=4 SU(2) relation with a defect on the affine factor. Its question is whether coset conformal-block identities, with suitable normalization, can replace the localization derivation.

BFT's publisher PDF was checked directly at Appendix B, PDF pages 50–51. Corollary 3.18, the signed triangle definition (3.47), Theorem 4.5, and equation (4.59) were checked against their extracted formulas. Publisher and arXiv pages independently confirm the article, publication date, and its stated relation to the surface-defect blowup formula.

The local Nekrasov PDF is arXiv:2007.03646v2, dated 5 October 2021, of the work subsequently published in 2024. It should not be represented as a separately checked 2024 publisher PDF. Its equation (1) is the target relation; equation (228) makes the U(2)/SU(2) prefactor distinction explicit.

### 2.1 The B.4/B.10 mismatch is real

Let S_pr denote B.4 exactly as printed and V denote B.3. Direct rational-function subtraction gives

\[
 S_{pr}(u;p,q)-S_{pr}(u;p,q/p)-V(u;p/q,q)
 =-\frac{p^2q(u_1^2-u_3^2)}{(p-q)(q-1)}.
\]

For example, at (p,q,u1,u2,u3)=(2,3,5,7,11), this is -576. This is a nonzero rational character, not generally a finite Laurent polynomial. It disproves the displayed rational-character splitting argument. It does not by itself prove a falsehood of the representation-theoretic theorem or of every conceivable regularized interpretation.

Replacing the affine pair -u1²-u2² by -u2²-u3² restores the splitting exactly. This is an explicit repair, not a faithful transcription of the publication.

### 2.2 The B.6 flux reversal is also substantive

The printed affine flux order is (l,n,m); the printed Virasoro order is (m,n,l). With the repaired B.4 numerator but this reversal retained, even the triple (l,n,m)=(1,0,0) gives a character with a pole at p=q. Its pole coefficient is

\[
 \left.(p-q)R_{reversed}\right|_{q=p}
 =-\frac{(p+1)(p^4u_1^2u_2u_3^3+p u_1^3-pu_1u_3^2+u_2u_3)}{p u_1^2u_2u_3},
\]

which is generically nonzero. A finite product of linear weights cannot be obtained by the finite-character argument from that reversed expression. Aligning both flux triples as the author does is necessary for this repair.

### 2.3 Additional correction: B.7's weight order

The printed B.7 associates a2 with μ and a3 with ν. Comparison with Theorem 4.5 requires

\[
 (a_1,a_2,a_3)=(\lambda/2,\nu/2,\mu/2)
\]

when (e1,e2)=(1,-K). The label n is the inserted weight's flux and m the outgoing weight's flux. Merely retaining the printed B.7 and allowing an unspecified sign does not work. An exact unequal-weight test in the new verifier gives actual/wrong = 15845867/18396730, neither +1 nor -1.

The frozen note makes the correct choice in its equation (14), but describes only two inconsistent printed formulas. A revision should list this third ordering correction as well.

### 2.4 The B.8 phase is harmless in the present sector

BFT includes a factor (-1)^λ in its full affine block; the repaired note does not. With a consistent determination, the ratio under λ→λ+2j is 1 for every integer j. Dropping this common flux-invariant phase does not affect the sewing equation. This observation is restricted to the integer-flux sector actually used here.

## 3. Arbitrary-integer character proof

Write D1=(1-p)(1-q/p), D2=(1-p/q)(1-q), and

\[
 A_r=\frac{p^r-1}{D_1}+\frac{q^r-1}{D_2}.
\]

A proof covering every integer, rather than a numerical range, follows from A0=A-1=0 and the recurrence

\[
 A_{r+1}-A_r=\frac{q^{r+1}-p^{r+1}}{p-q}.
\]

For r≥0 this is minus the row Σ_{i+j=r} p^i q^j with i,j≥0. For r≤-2 it is the positive row Σ_{i+j=-r} p^{-i}q^{-j} with i,j>0. Thus upward and downward induction from 0 gives precisely the author's two finite triangles. The empty r=0 and r=-1 cases are included.

Separately,

\[
 \frac qp\frac{p^r-1}{D_1}+\frac{q^r-1}{D_2}=qA_{r-1}
\]

is a rational identity: put x=p^r, y=q^r and clear denominators. No assumption on the sign of r enters.

For the signed triangle product t_r in the note, its degree is d(r)=r(r+1)/2 for all integers. Applying the finite Euler-product rule to A_r gives the first formula in (11). To obtain the second, substitute I=i+1, J=j+1 for r≥1 and use the negative triangle for r≤0. The resulting factors are exactly those of t_-r(a-e1); there is no untracked sign.

## 4. Three-point comparison and signs

For the common repaired high numerator, the two chart coefficients of each high monomial are pq and p². If its flux exponent is r, its contribution is

\[
 p^2\left[\frac qp\frac{p^r-1}{D_1}+\frac{q^r-1}{D_2}\right]
 =p^2qA_{r-1}.
\]

The low monomials give A_r. Applying the preceding finite-product identities separately to these seven monomials produces the numerator and all three denominator triangles in author equation (13). In particular, the incoming factor is t_-2l(2a1), not t_-2l(2a1+e1). This asymmetry is exactly what produces the incoming norm division.

With (a1,a2,a3)=(λ/2,ν/2,μ/2), rescale both periods and arguments by -K and interchange the two triangle periods. The net degree is zero:

\[
 d(-l-n-m)+d(l-n-m)+d(-l+n-m)+d(-l-n+m)
 -d(-2l)-d(-2n)-d(-2m)=0.
\]

Consequently no scale factor or scale-dependent phase survives. Corollary 3.18 converts the incoming denominator using

\[
 N_l(\lambda)=\frac{t_{-2l}^{1,-1/K}(-\lambda/K)}{t_{-2l}^{1,-1/K}(-(\lambda+1)/K)}.
\]

The source formula then agrees with author (16). An independent, shorter parity decomposition is useful. If σ is the finite-character sign exponent and S the Theorem 4.5 sign exponent, then

\[
 \sigma-S-l-m=-l(l+1)+m(m-1)+n(n-1)-2ln
 -2n(m-n)(2(m-n)-1).
\]

Every term is even for integer l,n,m. Therefore the sign is exactly (-1)^(l+m) for every integer triple, including mixed positive and negative fluxes. This is a proof, not an inference from the finite tests.

## 5. Sewing and formal meaning

For the two ordered vertices (μ1,μ2,λ) and (λ,μ3,μ4), the fluxes are (0,0,j) and (j,0,0). Equation (16) yields one factor (-1)^j at each vertex; their product is 1. The first incoming norm is N0(μ1)=1; the second is Nj(λ). Thus there is exactly one inverse internal norm, with the order of the two three-point coefficients matching source (4.59).

The unshifted character splitting fixes the denominator of the product ratio. Hence multiplication of the published relation (4.59) by the repaired left prefactor gives the coefficient-one identity (18). No extra elementary level-one block is needed in this four-point sector: source (4.58) uses trivial level-one external states and insertions. This observation does not automatically cover torus or half-integer sectors.

The conformal grading check is correct. With K=k+2, b²=-K/(K+1), and P=-(λ+1)b/(2K), the shift in the sum of the affine and Virasoro internal weights is j². At zero flux the sum is the original affine weight. Therefore, after factoring the common leading monomial, only finitely many j can contribute to any fixed conformal grade. This supports the formal block identity without assuming convergence of the bilateral sum as a complex analytic series.

The original report's literal reciprocal b and momentum signs do not satisfy this grading when its shift is read as P_T+j b_T. For K=2, λ=0, j=1, the grade is 5/3 instead of 1. Under the displayed positive-square-root convention, P_T=-P and b_T=1/b, so P_T-j/b_T is compatible. This is a source-convention repair, not a counterexample to the physical equation.

## 6. Zeros, poles, and regularization

The finite-product equalities are identities in a field of rational functions. Their derivation is first valid away from vanishing denominator factors; cleared-denominator versions are polynomial identities. A specialization at which an individual norm or Gram matrix degenerates cannot simply be substituted into the sewn decomposition.

In particular, the norm formula gives

\[
 N_1(\lambda)=\frac{K-\lambda-1}{K-\lambda-2}.
\]

Thus λ=K-1 gives a zero norm and λ=K-2 a pole. Both matter. An improved hypothesis should explicitly require nonzero finite norms and invertible Gram matrices, rather than only avoidance of poles. Genericity in the frozen note is sufficient in substance, but its shorter phrase about “poles of the norms and Gram matrices” is imprecise.

At minimum K≠0,-1 is needed for these affine/coset coordinates. In physical periods the dictionary assumes ε1 ε2(ε1-ε2)≠0. Further resonance and reducibility hyperplanes are excluded. The numerical use of rational K in the check tests rational-function identities; it does not purport to prove the generic representation decomposition at every rational level.

Zeros of numerator triangles can make a coefficient vanish. Such a zero is not automatically an error. If it coincides with a block pole or norm zero, a common meromorphic limit must be specified and shown to exist; it is not covered by the generic argument.

For infinite normalizers, the proof uses additivity of the regularized logarithm, or equivalently the explicitly stated multiplicative-character normalization. The finite ratios themselves have no infinite-product convergence issue. This does not uniquely identify absolute perturbative partition functions in a separate gauge convention, remove possible flux-invariant normalization freedom, or establish a global branch/analytic-convergence statement. No universal singular-level extension is certified.

## 7. Exact target and existing literature

The Coulomb/level dictionary in author (19) is algebraically correct:

- K=-ε2/ε1;
- λ=2a/ε1-1;
- d²=(ε1-ε2)ε2, b=ε2/d, P=a/d, Q=ε1/d;
- the affine chart raises k by one and shifts λ by 2j;
- the Virasoro chart shifts P by jb;
- the report's reciprocal square b_T²=(ε1-ε2)/ε2 is recovered.

For the Virasoro normalizer, using the sum of its chart periods, ε1, to define the u-coordinates is essential. Using its first chart period ε1-ε2 instead would be an erroneous alternative convention. The packet handles this correctly.

However, these equations do not supply the four external masses or prove equality of the physical and constructed full functions. The remaining exact certification should exhibit the three chart identifications and show that every additional scalar factor obeys the required product relation. Equality of KZ differential equations alone leaves normalization and solution/channel choices to be checked.

The source evidence is strong but should be described accurately:

1. BFT is a published affirmative treatment of the requested coset route, with (4.59) furnishing the substantive coefficient theorem and Appendix B furnishing the intended full-normalization construction. Its explicit gauge interpretation cannot be dismissed merely because Appendix B has correctable display errors.
2. Alday–Tachikawa's (3.23) has both an elementary scalar factor and an additional operator K. This prevents a blind identification in that particular convention. It does **not** prove that the regular defect of the original Nekrasov target needs the same insertion, or that the modern correspondence is missing.
3. Nekrasov–Tsymbaliuk (2022) proves the regular-defect KZ correspondence. Its explicit tree factors (44)–(45), coordinate change (51), gauge factor (62), twist (89), mass labels (90)–(91), and conformal realization (114), followed by section 5.4, are the appropriate precise bridge data. The present audit checked these source pointers but did not carry their N=2 specialization through all three blowup charts and match the BFT determinant normalization. That is the bounded missing calculation.

Consequently the packet's conservative full-target disclaimer is justified. It would be inaccurate to turn that disclaimer into a claim that the conjecture remains open in the literature. The public description should say that this is a verified conditional normalization repair supporting the published BFT proof, with exact gauge-convention certification not supplied here.

## 8. Recommended publication/status language

Accept the algebraic repair and sewing result with its stated dependencies. Do not claim a new theorem, an independent proof of BFT, a disproof of BFT, a new open problem, or a complete all-convention physical blowup theorem.

Before a future full-certification request:

1. Explicitly disclose the B.7 μ/ν correction alongside B.4 and B.6.
2. State nonzero norms and invertible Gram matrices, and retain the generic meromorphic/formal scope.
3. Supply an actual N=2 mass/defect/U(1)/perturbative dictionary in every chart, with the regularization and branch comparison, rather than only the Coulomb/level dictionary.
4. Credit BFT as directly relevant published prior work and keep the author’s conditional result separate from that literature claim.

## References

- J. Teschner, “Tau-functions, coset constructions and free fermion conformal blocks,” OWR 16/2022, pp. 836–839, especially p. 837. [Official report](https://doi.org/10.4171/owr/2022/16).
- M. Bershtein, B. Feigin, A. Trufanov, “Highest-Weight Vectors and Three-Point Functions in GKO Coset Decomposition,” CMP 406, 142 (2025). [Publisher](https://doi.org/10.1007/s00220-025-05318-1); [arXiv v3](https://arxiv.org/abs/2404.14350v3).
- N. Nekrasov, “Blowups in BPS/CFT correspondence, and Painlevé VI.” [arXiv](https://arxiv.org/abs/2007.03646), especially (1) and (228) in the inspected v2.
- L. Alday, Y. Tachikawa, “Affine SL(2) conformal blocks from 4d gauge theories.” [arXiv](https://arxiv.org/abs/1005.4469), especially (3.23)–(3.25).
- N. Nekrasov, A. Tsymbaliuk, “Surface defects in gauge theory and KZ equation,” LMP 112, 28 (2022). [Publisher](https://doi.org/10.1007/s11005-022-01511-8); [explicit bridge formulas in arXiv v3](https://arxiv.org/html/2103.12611v3).

No scholarly PDFs or unrelated source records are redistributed with this audit. No remote state was changed.
