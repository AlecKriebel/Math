# Independent acceptance: mixed odd SOS powers and the Motzkin threshold

Target: 30005461 / OWR-12697710-007. Reviewed 10 October 2026 (UTC).

## Decision

**ACCEPT THE FULL TWO-CLAUSE MATHEMATICAL TARGET.**

- The mixed-exponent implication is the previously published Blekherman–Kozhasov–Reznick result, with its Pinelis ingredient and the two previously disclosed display corrections retained.
- For every real c<3, all sufficiently large odd powers of f_c(x,y)=x^4 y^2+x^2 y^4+1−c x^2 y^2 are sums of real polynomial squares. Consequently the thresholds in the question satisfy lim c_k=3.

No material correction to the principal proof is required. This acceptance is a mathematical review relative to the cited published Positivstellensatz and standard projective-space cohomology, rather than a proof-assistant certificate or a reproof of those foundational results. It makes no priority claim, gives no explicit exponent or convergence rate, and makes no affirmative SOS claim at c=3.

## 1. Accepted edition and exact scope

The distributed principal proof is [PROOF.md](PROOF.md), 10,963 bytes; SHA-256 `46af7394ebfee7b0de9861693f84ab684502da3be208c626411f24e2538c7d15`. Its full mathematical argument is unchanged. [ACCEPTANCE.json](ACCEPTANCE.json) binds the exact distributed proof, complete substantive audit, credited-clause proof and optional appendix.

The original questions were independently viewed on printed p. 780, PDF p. 40, of Reznick's contribution to [Oberwolfach Report 14/2023](https://doi.org/10.4171/owr/2023/14). The target is the coefficient perturbation f_c above. The report's separate positive-definite perturbation by c(x²+y²+z²)³ is not substituted for it.

The complete elementary mixed-exponent proof and both source corrections appear in [CREDITED_MIXED_EXPONENT_PROOF.md](CREDITED_MIXED_EXPONENT_PROOF.md). Its authorship remains with Blekherman–Kozhasov–Reznick, with the Pinelis ingredient credited. The optional [real-delta appendix](REAL_DELTA_APPENDIX.md) is included without alteration. Acceptance concerns the two stated mathematical questions, not a claim that all possible literature or all quantitative refinements have been settled.

The source inspection and mathematical checks described below were performed during the historical proof and independent audit. Edition preparation rechecked frozen input bytes and publication integrity without new scholarly-source retrieval, source-text inspection, literature search or mathematical-computation reruns.

## 2. Published theorem interface

The essential imported result is Scheiderer's [Corollary 4.2, author manuscript, p. 11](https://www.math.uni-konstanz.de/~scheider/preprints/ppss.pdf), from *A Positivstellensatz for projective real varieties*, Manuscripta Mathematica 138 (2012), 73–88, [DOI 10.1007/s00229-011-0484-3](https://doi.org/10.1007/s00229-011-0484-3).

The statement was checked independently in the primary text and visually. It requires a reduced projective real scheme without one-dimensional irreducible components, Zariski-dense real points, invertible sheaves L,M with M ample, and strictly positive sections f of L² and g of M². It gives fg^N as a sum of squares of sections of L⊗M^N for every sufficiently large N. There is no smoothness hypothesis. Its quantifier includes sufficiently large even N. Neither the positive-definite special case on projective space nor the different nonnegative-section theorem for smooth surfaces is being used.

The author's retrieved PDF has 275091 bytes and SHA-256 686cfde78b5472be2f6a0185873822098f61006ba78b79ecfaccdd3365882cb0. Publication identity was cross-checked against the [author's publication list](https://www.mathematik.uni-konstanz.de/scheiderer/publikationen/papers/). This is a published theorem even though the inspected PDF is its author manuscript.

## 3. Independent reconstruction of every geometric step

### 3.1 Scheme, dimension and real density

Let G=ABC−D³ and S=V(G) in P³ over R. Viewing G as a polynomial in C, its coefficients AB and −D³ are coprime in the UFD R[A,B,D]. It is primitive and degree one over that ring's fraction field. Gauss's lemma makes G irreducible; irreducibles are prime in this polynomial UFD. Thus the homogeneous coordinate ring is a domain. S is integral, reduced, projective and of dimension two. Its sole component is not a curve.

The D≠0 chart is ABC=1, with coordinate ring R[A^{±1},B^{±1}] and real parametrization [a:b:(ab)^{-1}:1]. A Laurent polynomial vanishing on every pair of nonzero real numbers is zero, by clearing a monomial denominator and using the one-variable polynomial identity principle successively. These real points are dense in the chart. Since S is integral and the chart nonempty, they are dense in S. This verifies the theorem's density requirement without asserting that the later cubic substitution is surjective.

H=O_S(1) is an invertible very ample sheaf, as the restriction in a closed projective embedding. Singularity does not obstruct invertibility of this sheaf. Indeed, S is singular at the three coordinate vertices with D=0; the argument does not hide this fact.

### 3.2 Strict positivity on all real projective points

Write q_c=A²+B²+C²−cD². On G=0, AM–GM applied to A²,B²,C² gives A²+B²+C²≥3D². The equality (A²B²C²)^{1/3}=D² follows from ABC=D³ and is valid for every real sign pattern.

At D≠0 and c<3 this yields q_c≥(3−c)D²>0. At D=0, q_c=A²+B²+C²>0 because a projective coordinate tuple is nonzero. This covers the singular vertices and the entire real boundary. On a chart where a coordinate T is nonzero, q_c/T² is the representative of q_c as a section of H². Its sign is exactly the sign just checked. Thus the positivity is global and in the precise square-line-bundle sense of the theorem. The argument applies to every real c<3, including zero and negative values.

### 3.3 The exponent and its parity

Set X=S, L=M=H and f=g=q_c. The theorem yields q_c^{N+1}=Σs_j² with s_j in H⁰(S,O_S(N+1)) for all sufficiently large N. Choose an even N and set m=N+1. Then m is a positive odd integer, q_c^m has section degree 2m, and each s_j has degree m.

Choosing odd N instead would produce only an even power and would not establish the question. The inspected theorem's quantifier explicitly permits the required choice. The sufficient exponent may depend on c; the proof never interchanges these quantifiers.

### 3.4 Polynomial lifting, including the kernel

For every t, multiplication by G gives the exact sequence

0 → O_{P³}(t−3) → O_{P³}(t) → i_*O_S(t) → 0.

The primary formula in [Stacks Project, Lemma 30.8.1](https://stacks.math.columbia.edu/tag/01XS) gives H¹(P³_R,O(t−3))=0 for every integer t. Applying the resulting global-section exact sequence first at t=m gives real homogeneous lifts H_j of all s_j. Applying it at t=2m identifies the kernel: q_c^m−ΣH_j² is a multiple of G. The degree of that multiplier, if nonzero, is 2m−3.

This is a genuine polynomial congruence. Neither rational functions nor local-only square roots are passed off as polynomials. Normality is not an extra hypothesis, and projective normality need not be imported: the hypersurface exact sequence supplies precisely the lifting and kernel assertions required.

### 3.5 Substitution and its base points

The homomorphism (A,B,C,D)↦(x²y,xy²,z³,xyz) kills G exactly and sends q_c to M_c=x⁴y²+x²y⁴+z⁶−cx²y²z². Applying it to the congruence therefore gives the identity

M_c^m=ΣH_j(x²y,xy²,z³,xyz)².

The square roots are homogeneous of degree 3m, so the squares have degree 6m. Setting z=1 gives the exact requested f_c^m with no multiplier or denominator.

The four cubic forms vanish simultaneously at [1:0:0] and [0:1:0]. They therefore do not define a global projective morphism. This is harmless here because only a polynomial ring homomorphism is applied to a polynomial identity. The resulting identity automatically holds at those points too. No extension across a rational-map indeterminacy is asserted or needed.

### 3.6 The limit and the endpoint

For a fixed c<3, one odd SOS power implies all larger odd powers: multiply each square root by the corresponding integer power of f_c. Thus eventually c≤c_k under the interval definition in the question. For c>3, f_c(1,1)=3−c<0, so no odd power can be SOS; therefore c_k≤3. The first inequality for every c<3 and the second for every k give liminf c_k≥3≥limsup c_k.

At c=3, q_c vanishes at [1:1:1:1]. The positive-section argument stops there, as it must. No SOS conclusion at the endpoint or uniform exponent on the whole half-line follows from this proof. Monotonicity of c_k is consistent with the proof but is not needed to take the limit.

## 4. Mixed-exponent clause and source corrections

The mixed-exponent conclusion is credited to Blekherman–Kozhasov–Reznick, [published Theorem 5.3](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/on-odd-powers-of-nonnegative-polynomials-that-are-not-sums-of-squares/7C4BAF1C7EBA17DE741C36DB40691412), previously arXiv:2407.21779v1, Theorem 44. The publisher's theorem and Pinelis credit were rechecked; the archived p. 21 was visually inspected. The earlier complete audit's proof was read and independently reconstructed.

Put a=2i+1, b=2j+1, n=a+b−1 and B_{n,r}(u,v)=Σ_{s=0}^r binom(n,s)u^s v^{r−s}. For even r<n, the corrected truncated-binomial positivity argument makes B_{n,r} SOS. The coefficient-exact split

(u+v)^n=v^b B_{n,a−1}(u,v)+u^a B_{n,b−1}(v,u)

has neither missing nor overlapping terms. Substitution u=p,v=q and multiplication of sums of squares establish the claim directly for arbitrary real polynomials, including unequal degrees, zero polynomials, constants and a=1 or b=1. Thus there is no unresolved homogeneous-to-inhomogeneous restriction.

Both corrections remain explicit: the archived positivity assertion requires the even index 2r; the homogenization sum's upper limit must also be 2r. For n=3,r=1 the literal erroneous expressions can be negative, whereas the corrected quadratic is 1+3t+3t². These display errors do not invalidate the correctly indexed proof or establish novelty for this audit.

## 5. Optional real-delta appendix

The appendix is not an essential dependency and is unnecessary for full acceptance. Its restricted conclusion δ^R(M_c)=6 for 0<c<3 is nevertheless consistent and independently checked.

AM–GM shows that the only real projective zeros in this range are [1:0:0] and [0:1:0]. At the first, the local equation is u²+u⁴+v⁶−cu²v². The successive strict transforms at the unique real infinitely near point have multiplicities 2,2,2 and tangent cones u², a², b²+v². The next exceptional restriction is 1+t², so there are no further real points. Each complementary chart has exceptional restriction 1 or 1+t², ruling out omitted real directions. The local contribution is therefore 1+1+1=3 under Definition 6.3 of [Stubborn Polynomials, arXiv:2602.01191v1](https://arxiv.org/abs/2602.01191v1); symmetry supplies the other 3. The definition was checked in the retained primary text.

Only this direct local calculation is endorsed here. The preprint's Del Pezzo/resolution criterion and its deeper references are not imported into the accepted threshold proof, and this appendix makes no total-delta claim at c=3.

## 6. Reproducibility, adverse controls and residual scope

The independent exact checker passes normal Python, -O and -OO: 71722 explicit checks and 11 adverse controls. It checks symbolic substitution, singular-boundary positivity, rational signed torus samples, exponent/degree arithmetic, the complete mixed split for 961 odd-exponent pairs, derivative/Pascal coefficients and independently derived blowup charts. Adverse controls detect a changed cubic relation, wrong substitution degree, erased parameter term, unjustified strictness at c=3, an above-endpoint odd power, mistaken evidence from even powers, wrong N parity, the undefined projective map, the invalid direct positive-definite shortcut, and both erroneous source truncations.

These finite checks test transcription and vulnerable interfaces. They do not prove the imported Positivstellensatz, replace the universal arguments above, or turn the acceptance into formal certification. Historical proof-package and source-audit integrity checks passed in normal and optimized Python. The included acceptance binds the exact distributed texts; the public source metadata preserves inspection coverage and supplementary finite-check counts.

There is no unresolved mathematical residual in either stated clause. Explicit exponents, convergence rates, priority questions and a fresh foundational audit of the optional preprint are outside the accepted claim. This AI-assisted manuscript and audit are unrefereed. Acceptance is not external human peer review, journal acceptance or formal proof-assistant certification. Programs, raw outputs, generated certificates, datasets, copied primary texts/images and private coordination material are excluded from the proof-only edition. The mathematical verdict does not depend on omitted software or certificates.
