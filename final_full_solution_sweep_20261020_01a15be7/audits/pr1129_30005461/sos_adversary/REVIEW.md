# PR 1129: independent SOS and threshold audit

Audit date: 2026-10-21 UTC. Problem 30005461 / OWR-12697710-007.
Immutable head: `26fed29c1130e539ba018a37200f133870f0e036`.
Comparison base: `f6caddda8f8be2cdb3e91494325d8f7f365bc3fc`.

**Mathematical verdict:** no substantive defect found in the two stated clauses. The mixed-exponent clause is a credited prior result. The principal threshold proof has the claimed quantifiers and yields the complete threshold limit, subject to its explicitly cited published geometric inputs. Independent SOS arguments below verify closedness, downward closure, the exact first threshold, the endpoint obstruction, and the limiting deduction. The optional real-delta calculation is also correct. This is an audit of mathematics and scope, not a publication-readiness or novelty decision.

The parent supplied a fresh publication-ledger preflight before this work began: 180 rows, 2026-10-21 22:48:06 UTC, no exact problem/alias/Motzkin/mixed-odd match. I did not access or modify the ledger, providers, PR, Git index or refs. I inspected the immutable PR blobs and fresh primary sources. I did not inspect another current reviewer's work or communicate with that reviewer. A later, explicitly supplied priority implication is analyzed separately in section 9.

## 1. Exact target and boundary

The original is Bruce Reznick's contribution, “The Odd Powers of the Motzkin Polynomial, etc.” in [Oberwolfach Report 14/2023](https://ems.press/content/serial-article-files/47007), printed pp.778–780, especially p.780 / PDF page 40. The local catalogue identifies both the mixed-exponent conjecture and the Motzkin threshold limit as the target. The adjacent fixed-exponent convexity question is broader and is not solved or claimed solved by this PR.

Write SOS for a finite sum of squares of real polynomials. The two audited assertions are:

1. For arbitrary real polynomials p,q in finitely many variables and integers i,j≥0, if p^(2i+1) and q^(2j+1) are SOS, then (p+q)^(2i+2j+1) is SOS.
2. For f_c=x^4y^2+x^2y^4+1−cx^2y^2 and every fixed real c<3, all sufficiently large odd powers of f_c are SOS. Consequently, if S_k={c∈R:f_c^(2k+1) is SOS}=(-∞,c_k], then lim c_k=3.

This does not require a computable exponent, convergence rate, a common exponent for every c<3, strict increase of c_k, a positive SOS conclusion at c=3, or convexity of every fixed-exponent cone. The principal proof, README, STATUS and ACCEPTANCE consistently observe those limits. In particular, the manuscript explicitly disclaims novelty and formal human peer review.

## 2. Independent closed-cone argument

Fix an odd positive integer m. Every square root in an SOS representation of a polynomial of degree at most 6m has degree at most 3m: higher leading homogeneous parts in real squares cannot cancel. Let v be the vector of all monomials in x,y of degree at most 3m. Any such SOS has a representation v^T Qv with Q positive semidefinite.

The image of a closed positive-semidefinite cone under an arbitrary linear map need not be closed; that general assertion would be an invalid proof here. Instead take a fixed Gaussian measure μ with positive density on R² and put H=∫vv^T dμ. For any nonzero coefficient vector a, ∫(a^Tv)²dμ>0, so H is positive definite. For coefficientwise convergent SOS polynomials F_n=v^TQ_nv, the integrals ∫F_n dμ are bounded. Thus

    λ_min(H) tr(Q_n) ≤ tr(HQ_n) = ∫F_n dμ.

Positive-semidefinite Q_n are bounded and have a convergent subsequence. Its limit Q is positive semidefinite and represents the coefficientwise limit F. This proves closedness of the fixed-degree SOS cone with no improper closed-image inference.

The coefficient map c↦f_c^m is polynomial, hence continuous. Therefore S_k, for m=2k+1, is closed. One does not need the image of the nonlinear curve to be convex. For c≤0, f_c itself is SOS, so all its positive integer powers are SOS by closure of SOS under multiplication. For c>3, f_c(1,1)^m=(3−c)^m<0, ruling out SOS. In particular S_k is nonempty and bounded above.

## 3. Independent downward closure, without the full mixed theorem

For any odd m≥1 define the binary form

    R_m(u,v) = ((u+v)^m−u^m)/v
             = Σ_{r=1}^m binom(m,r)u^(m−r)v^(r−1).

This is a polynomial, including at v=0. For v≠0 it is positive because an odd power is strictly increasing on R. At v=0 it equals m u^(m−1)≥0; for m=1 it is 1. A nonnegative binary form of even degree is a sum of two real polynomial squares: dehomogenize, factor over C, split real even-multiplicity factors and conjugate pairs, and homogenize back. Roots or degree drops at infinity cause no difficulty in this polynomial identity.

Consequently, if P^m is SOS and Q is SOS, then

    (P+Q)^m = P^m + Q R_m(P,Q)

is SOS. Here no division by Q, no positivity away from its zeros, and no equal-degree hypothesis is used. If c∈S_k and d≥0, take P=f_c and Q=d(xy)². Since P+Q=f_(c−d), it follows that c−d∈S_k. This proves downward closure directly. Closedness and boundedness then give S_k=(-∞,c_k] with c_k=max S_k∈[0,3]. It is stronger than merely assuming the interval notation in the original question.

Multiplying an SOS representation of f_c^(2k+1) by the square f_c² proves S_k⊆S_(k+1). More generally, one odd SOS power m gives every larger odd power m′ by multiplying its square roots by f_c^((m′−m)/2). The increment must be even; an assertion about all integer powers would need a separate formulation.

## 4. Independent Newton-support tests, including c=3

For a real SOS F=Σh_j², every monomial of h_j lies in half the Newton polytope of F. For completeness, maximize any linear functional on exponents. The leading parts of the h_j with the maximal weight cannot have a zero sum of squares as real polynomials. Thus the maximal weight in F is twice the maximal root weight. Varying the functional yields the containment. Also the Newton polytope of a nonzero product is the Minkowski sum of its factors' Newton polytopes, as exposed leading products cannot vanish in the polynomial domain.

For m=1 the half Newton triangle of f_c has vertices (0,0),(2,1),(1,2). Its only lattice points are (0,0),(1,1),(2,1),(1,2). Therefore SOS roots, if any, lie in the span of 1,xy,x²y,xy². The coefficient of x²y² in their squared sum can only be a sum of the squares of their xy coefficients. It cannot be −c for c>0. Together with the explicit SOS for c≤0, this gives **c_0=0**, independently of a numerical semidefinite calculation.

There is a stronger boundary obstruction. Let

    M=M_3=x^4y²+x²y^4+z^6−3x²y²z²

and suppose M^m=Σh_j² for odd m. The roots may be taken homogeneous of degree 3m. Their Newton supports lie in the triangle with vertices (2m,m,0),(m,2m,0),(0,0,3m). Average the representation over independent changes of the signs of x and y. Splitting each h_j into its four x/y parity components gives another SOS representation consisting of those components; the cross terms disappear exactly. Only the component even in both x and y can be nonzero at (0,0,1).

In that even/even component the maximal x exponent is at most 2m−2. Indeed x exponent 2m occurs only at the triangle vertex (2m,m,0), whose y exponent m is odd; the next possible x exponent in an even component is 2m−2. The x=0 face consists only of (0,0,3m), so evaluation at x=0 after y=z=1 extracts precisely the z^(3m) coefficient. Set y=z=1. Then

    M(t,1,1)^m=(t²−1)^(2m)=Σh_j(t,1,1)².

Every restricted real root must vanish to order at least m at both t=1 and t=−1. Otherwise the smallest order in the sum would have a nonzero sum of squared leading coefficients and could not cancel. Thus every nonzero restricted root is divisible by (t²−1)^m, and has degree at least 2m. For an even/even root the preceding degree bound is 2m−2, so its restriction is zero. In particular its coefficient of z^(3m), obtained at t=0, is zero. All other parity components vanish at (0,0,1) already. This contradicts M(0,0,1)^m=1.

Hence **no odd power at c=3 is SOS**. This is an endpoint obstruction, not an extension of the PR's existence assertion. Homogenizing an affine SOS of f_3^m to degree 6m would produce a homogeneous SOS of M^m (root degree ≤3m), so the obstruction applies to S_k as well. Therefore c_k<3 for every finite k. It also proves that no single odd exponent can work for every c<3: closedness would then put c=3 in the same fixed S_k. These checks falsify natural stronger claims while leaving the actual PR claim intact.

## 5. Mixed exponents and source-display corrections

The credited prior source is Blekherman–Kozhasov–Reznick, [Forum of Mathematics, Sigma 14 (2026), e65](https://doi.org/10.1017/fms.2026.10221), published Theorem 5.3; arXiv:2407.21779v1 labels it Theorem 44. I freshly inspected both versions. The key truncated-binomial input is credited to Pinelis. The PR does not claim ownership of this result.

For odd a=2i+1 and b=2j+1, set N=a+b−1 and

    B_(N,e)(u,v)=Σ_(s=0)^e binom(N,s)u^s v^(e−s),  e even.

The univariate truncation at even e is strictly positive for N>e. The e=0 case is 1. For e>0, the initial N=e+1 case is (1+t)^(e+1)−t^(e+1)>0. Increasing N, at each global minimum the derivative identity F′_(N,e)=N F_(N−1,e−1) and Pascal's identity reduce its value to the positive F_(N−1,e). The positive even-degree polynomial factors as a sum of two real squares of degree at most e/2; homogenizing gives B_(N,e) as two binary squares. This argument covers infinity and arbitrary real u,v through polynomial identities.

The identity

    (u+v)^N = v^b B_(N,a−1)(u,v) + u^a B_(N,b−1)(v,u)

splits binomial indices into [0,a−1] and [a,N], with no missing or repeated index. Substitution u=p,v=q proves the arbitrary-polynomial clause. Zero polynomials, constants, a=1, b=1 and different degrees are covered. No independent homogenization is necessary for this direct substitution proof. The PR's optional homogenization also uses an even common degree, so its square-root degree shifts are integral.

Two genuine display errors in the sources are correctly disclosed and repaired in the PR. The arXiv-v1 positivity statement uses r where 2r is necessary; N=3,r=1,t=−1 gives −2 for the wrongly odd truncation. Both its homogenization display and the fresh publisher PDF/HTML sum only to r where 2r is necessary. At N=3,r=1 the wrongly truncated binary form v²+3uv takes value −2 at (u,v)=(-1,1); the correct form is v²+3uv+3u². The complete binomial split in the theorem proof uses the correct full ranges. These are transcription corrections, not a gap in the repaired proof.

## 6. Existence input and complete limiting deduction

I checked the actual [Scheiderer arXiv:1104.1772v1](https://arxiv.org/pdf/1104.1772v1), Corollary 4.2 on PDF p.11, and the [publisher abstract and bibliographic record](https://link.springer.com/article/10.1007/s00229-011-0484-3). The author-site PDF retrieval timed out; I do not claim its captured byte identity. The corollary applies to reduced projective real schemes with dense real points and no one-dimensional irreducible component, positive square-line-bundle sections f,g, and ample M; fg^N is SOS in L⊗M^N for every sufficiently large integer N. It has no smoothness requirement. The full theorem is imported, not re-proved in this audit.

The PR's cubic S:ABC=D³ and H=O_S(1) fit that statement. Independently, for every real c<3 the section q_c=A²+B²+C²−cD² obeys the useful uniform-in-points estimate

    q_c ≥ δ_c(A²+B²+C²+D²),  δ_c=min(1,(3−c)/4)>0,

on S(R). Indeed A²+B²+C²≥3D², and (1−δ_c)(A²+B²+C²)−(c+δ_c)D²≥0. This checks negative c as well as 0<c<3, including D=0 and the singular coordinate points. As c→3 the lower bound degenerates, so no common exponent follows.

With f=g=q_c and L=M=H, choose a sufficiently large **even** N. Then q_c^(N+1) is SOS in sections of H^(N+1), with odd m=N+1. The hypersurface restriction sequence and H¹(P³,O(t−3))=0 lift the root sections to genuine homogeneous degree-m polynomials; [Stacks Lemma 30.8.1](https://stacks.math.columbia.edu/tag/01XS) supplies this vanishing for every twist. The equation is an identity modulo ABC−D³, not just equality on real points. Substitution (A,B,C,D)=(x²y,xy²,z³,xyz) annihilates that ideal and turns q_c exactly into M_c=x^4y²+x²y^4+z^6−cx²y²z². Thus it produces an unmultiplied SOS of M_c^m and then of f_c^m. Polynomial substitution remains legitimate at its projective basepoints. It introduces no denominator or multiplier.

The integral cubic has dimension two; the D=1 chart is ABC=1, with real points dense in the Laurent-coordinate torus. This verifies the relevant density/component hypotheses rather than incorrectly applying the positive-definite-forms special case directly to M_c, which has real zeros. I leave a second projective-family audit to the parent, but found no incompatibility between this imported result and the SOS deductions.

For each fixed real c<3 the existence route gives one odd m, so section 3 gives every sufficiently large odd exponent. Therefore for every ε>0, c=3−ε eventually belongs to S_k and c_k≥3−ε eventually. Hence liminf c_k≥3. Section 2 gives c_k≤3 for all k, so limsup c_k≤3 and the limit is 3. Alternatively monotonicity gives existence of the limit first. There is no exchange of the c and k quantifiers, no conclusion at c=3, and no rate assertion.

## 7. Optional real-delta appendix

Freshly inspected [Stubborn Polynomials, arXiv:2602.01191v1](https://arxiv.org/pdf/2602.01191v1), Definition 6.3, p.20. Its real-delta recursion counts m(m−1)/2 at a real point of multiplicity m and recurses over real first-order infinitely near points. The PR uses this definition only in an optional appendix; the principal proof has no essential dependency on that preprint's resolution criteria.

For every fixed 0<c<3, AM–GM implies M_c≥(3−c)x²y²z². Its only real projective zeros are P=[1:0:0],Q=[0:1:0]. At P the local equation is u²+u^4+v^6−cu²v². The successive vertical strict transforms are

    a²+a^4v²+v^4−ca²v²,
    b²+b^4v^4+v²−cb²v²,
    1+t²−ct²v²+t^4v^6.

The first two exceptional restrictions are a² and b², each with exactly one real zero. The third is 1+t² and has no real zero. The complementary charts have exceptional restrictions 1,1,1+s² respectively. Thus there are exactly three multiplicity-2 centers, with no omitted real direction, at each of P and Q. The tangent cones are u²,a²,b²+v², independent of c. The total is 2(1+1+1)=6. This is an all-real-c calculation; it uses no continuity extrapolation from a numerical parameter and does not silently add complex tangent directions to a real invariant. The formulas and complementary-chart identities were independently checked exactly with c left symbolic.

## 8. Checkable artifacts and limits

`CHECKS.json` records independent finite exact checks of coefficient identities, binomial index ranges, affine/homogeneous substitutions, blowup identities with symbolic c, parity/degree bounds, and adverse controls. `verify_artifact.py` reconstructs them using only the standard library. These checks detect transcription and sealing errors; they do not prove universal positivity, the projective theorem, or priority. Those conclusions depend on the written arguments and explicitly imported mathematical theorems.

All ten PR blobs, fresh source PDF/HTML bytes, extracted text, and inspected page renders are privately bound by `private/INPUT_MANIFEST.json`; public source identities and locators are in `SOURCE_BINDINGS.json`. No captured PR/source script was executed. The offline verifier has explicit guards that remain active under normal Python, -O and -OO. It requires an externally supplied manifest SHA-256, rejects symlinks and unlisted files, and verifies exact private/public inventories and hashes before running fresh independent checks. `CONTROL_TESTS.json` describes positive and corruption tests; the immutable final manifest hash is delivered separately to the parent.

No substantive mathematical correction is required to the stated principal clauses or optional appendix. The written proof remains nonconstructive: no square-root list or effective exponent is delivered. I did not reproduce Scheiderer's foundations, Del Pezzo classification, or a literature-wide originality audit.

## 9. Later supplied lead: precise prior-theorem implication

After the independent SOS/threshold mechanism above was established, at approximately 22:54 UTC the parent supplied this additional lead: apply *Stubborn Polynomials* Theorem 6.4 to the optional delta calculation. This section deliberately records that dependency on a later lead; it was not an independent discovery of that lead.

I inspected the actual Theorem 6.4 and the definition of stubbornness, and tried to invalidate each hypothesis. The theorem says that a nonnegative ternary sextic F that is not SOS and has δ^R(F)≤8 is not stubborn. “Not stubborn” provides at least one odd SOS power. For the exact M_c family and **every real 0<c<3**, nonnegativity follows from AM–GM; non-SOS follows independently from the half-Newton coefficient obstruction in section 4 (or from the affine version by dehomogenization); and section 7 gives δ^R(M_c)=6. There is no hypothesis restricting c to rational or generic values and no additional all-complex-singularities condition in this sufficient direction. Thus the theorem's hypotheses hold throughout the required interval.

The following implication is consequently complete **if that prior theorem is imported as stated**:

    Theorem 6.4 + the six-center local computation
    ⇒ for each real 0<c<3, some odd M_c^m is SOS
    ⇒ every sufficiently large odd M_c^m is SOS
    ⇒ the same statement for f_c by z=1
    ⇒ lim c_k=3 by the closed-ray argument.

For c≤0 the polynomial is already SOS, so the theorem's exclusion of SOS inputs leaves no parameter gap. Even without the independent non-SOS argument, an already-SOS alternative would satisfy the desired conclusion immediately. The word “odd” is built into stubbornness, so this is not an even-power tautology. Multiplication by a square supplies all larger odd exponents. The endpoint c=3 is outside the local/global argument and remains obstructed as shown above. Older exceptional intersections are covered by the complementary charts; no extra real infinitely near points change the count.

I found no gap in this exact prior-theorem implication. It relies on the prior preprint theorem, whereas the PR's principal proof uses a published theorem by a different direct construction. This establishes logical coverage conditional on that prior theorem; deciding the publication's originality or treatment of an alternative proof belongs to the parent priority audit. I did not independently reconstruct the preprint's general weak-Del-Pezzo theorem or its cited classification foundations.
