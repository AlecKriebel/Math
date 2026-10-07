# Independent audit of the Robinson certificate counterexample

Problem 30000717 / OWR-1465-011. Review date: 7 October 2026.

## Mathematical verdict

The zero-line and coordinate-axis argument is valid. It proves that the nonnegative Robinson sextic R is not a sum of real polynomial squares modulo the ordinary radical of either the tangency-minor ideal J_R or the separate off-diagonal-product ideal K_R. The proof works even modulo the entire ideal of polynomials vanishing on the real variety.

A separately checked strengthening proves the same nonmembership for R+ε for every ε≥0. Thus the example has global nonnegativity and real-variety nonnegativity, but fails both proposed certificate conditions (iii) and (iv). The positive-ε conclusion uses an additional finite-univariate-SOS degree argument; it is not inferred from failure of the zero-ε certificate alone.

The result is a counterexample to the stated equivalence. It is not a historical-priority determination, a formal proof-assistant certificate, or conventional human peer review. The detailed source and frozen-input records accompany this report.

## Source formulation check

The publisher's report was independently retrieved from https://ems.press/content/serial-article-files/46100 . Its 559,967 bytes have SHA-256 bd4f914a306afd73002d8c74f76e0c468113749240e90815a62ad151a53f783f, identical to the supplied source. Fresh renders of printed pages 798, 810, and 811 were visually inspected.

Theorem 1 on printed p.810 uses the ordinary radical in condition (iii), and the original ideal with every positive ε in condition (iv). Its gradient-ideal hypothesis includes attainment of the infimum. Conjecture 2 on p.811 proposes replacing that ideal and dropping attainment. The displayed replacement visibly contains comma-separated cross-products and an ellipsis. It does not visibly contain the minus signs of the catalogue tangency-minor formulation. Both explicitly defined ideals are covered by the reviewed proof; the original author's intended correction has not been established. Robinson's polynomial is printed on p.798, equation (2).

The public bibliographic link is https://doi.org/10.4171/owr/2007/14 . This review does not assume that a search proves the absence of earlier counterexamples.

## Reconstruction of the decisive proof

Write S=R[x,y,z] and

R=x^6+y^6+z^6−x^4y^2−x^2y^4−x^4z^2−x^2z^4−y^4z^2−y^2z^4+3x^2y^2z^2.

Set J_R=(yR_x−xR_y,zR_x−xR_z,zR_y−yR_z), and K_R=(yR_x,xR_y,zR_x,xR_z,zR_y,yR_z).

### Nonnegativity

The substitution a=x²,b=y²,c=z² gives the symmetric cubic

F=a³+b³+c³−a²b−ab²−a²c−ac²−b²c−bc²+3abc.

The exact identity F=(a−b)²(a+b−c)+c(a−c)(b−c) is correct. By symmetry the nonnegative inputs may be ordered a≥b≥c. Each factor in both products is then nonnegative, so R≥0. Its value at the origin is zero. The attained infimum causes no scope issue: dropping an attainment hypothesis enlarges the class; it does not require nonattainment.

### Eleven real lines suffice

The ten directions are (1,s,t), (1,s,0), (1,0,t), and (0,1,t), with the indicated signs in {−1,1}. There are four in the first family and two in each other family. Exact substitution gives R(tv)=0 and ∇R(tv)=0 for every real t and every listed direction v. Alternatively, gradient vanishing follows from global minimality at these points.

Hence every generator of both J_R and K_R vanishes on these ten lines. On the first coordinate axis, R(t,0,0)=t^6 and ∇R(t,0,0)=(6t^5,0,0), so all their off-diagonal generators vanish there as well. No claim that these are the whole varieties is needed.

### Cubic evaluation injectivity

For a cubic, the six directions with one zero coordinate force the form

A x(x²−y²−z²)+B y(y²−x²−z²)+C z(z²−x²−y²)+D xyz.

Its other four evaluations are −A−Bs−Ct+Dst. The four independent sign characters show A=B=C=D=0. This is a complete coefficient proof, not an inference from numerical rank.

The same result holds in homogeneous degrees d<3: multiply by x^(3−d) and use the fact that S is an integral domain. It is harmless that x vanishes at two of the chosen representatives, since the resulting cubic vanishes at all ten, and the zero-polynomial conclusion is global.

Independently generated exact evaluation matrices have ranks 1, 3, 6, and 10 in degrees 0, 1, 2, and 3. The degree-three determinant is −128 in the independent script's stated ordering. The candidate's separately stated ordering also has determinant −128, verified by rerunning its checks.

### Ordinary and real radicals

If h belongs to the ordinary radical of L, some h^N lies in L. Evaluating at any real common zero gives h(w)^N=0, so h(w)=0. This is sufficient; no Nullstellensatz or radical computation is used.

The same conclusion for the real radical follows directly from its defining identity h^(2m)+Σr_i²∈L: evaluation gives a sum of nonnegative real numbers equal to zero. More strongly, the proof assumes only that h vanishes on the eleven displayed real lines, so it holds for h in I(V_R(L)).

### Arbitrary finite SOS and constant perturbations

Assume R+ε=Σ_j q_j²+h with real polynomials q_j and a finite number of summands, where h vanishes on the relevant real variety. On each zero line, Σ_j q_j(tv)²=ε. For ε≥0, every real univariate q_j(tv) is bounded on the entire real axis and is therefore constant. Thus every positive homogeneous component q_{j,d} vanishes at all ten directions. Cubic injectivity and its lower-degree consequence force q_{j,1}=q_{j,2}=q_{j,3}=0. The constants remain unconstrained except for their squared sum.

On the first coordinate axis, Σ_j q_j(t,0,0)²=t^6+ε. If some axis restriction has degree D>3, take the largest such degree. The coefficient of t^(2D) in the finite SOS is a nonempty sum of squares of nonzero real leading coefficients and is positive, contrary to the degree-six left side. Therefore every restriction has degree at most three. Since its degree-one through degree-three coefficients have already vanished, it is constant. A sum of constants cannot be t^6+ε.

For ε=0 the alternative argument in the original candidate is valid: all q_j vanish on the zero lines; all homogeneous components through degree three disappear; each axis restriction is divisible by t^4; and its SOS is divisible by t^8, contrary to t^6. The extension for ε>0 does not use this constant-term inference.

## Adversarial checks and boundaries

- Arbitrarily high ambient degrees are allowed. Only univariate restrictions are degree-bounded, and the bound is proved from the assumed identity.
- Lower-order terms, constants, and cross-terms cannot evade the argument. Constants are explicitly retained for positive ε.
- Finitely many real squares are essential and match the source. Complex squares, signed sums, infinite series, and rational functions are different claims.
- A pointwise zero at ten representatives alone would be insufficient to separate homogeneous components. The proof correctly uses ten entire lines and the polynomial identity in their real parameter.
- The first axis is an actual subset of each real zero set for this R, verified on every generator. Its membership is not inferred from the zero lines.
- No assumption of ordinary radicality, real radicality, zero-dimensionality, or reducedness is used.
- No completeness statement for complex eigenpoints or real tangency points is used.
- The conclusion addresses both the catalogue differences and the explicitly defined literal off-diagonal products. It does not silently identify them or assert a unique interpretation of an ellipsis.
- The known gradient-ideal theorem is unaffected: Euler's identity gives 6R=xR_x+yR_y+zR_z.
- Inequality multipliers in genuine gradient-tentacle or truncated-tangency certificates can cancel high-degree terms and are not covered by this obstruction.
- Failure of the four-way equivalence already follows from condition (iii). Condition (iv) is also false here, but only because the added degree argument proves it separately.

## Other claims in the candidate

The sphere-minimization proof of equivalence between global nonnegativity and nonnegativity on the tangency-minor real variety is correct for every real polynomial. A negative value at the origin is immediately detected. Otherwise a minimum on the compact positive-radius sphere exists; its Lagrange multiplier equation makes the gradient parallel to the radius, so all minors vanish at a negative point. No global minimum or lower bound is required.

The separate product-ideal diagnostic Q(x,y)=(1−xy)²+y²−1/2 is also correct. Its generators are 2y²(xy−1) and 2x(x(xy−1)+y). Their real common zero is only (0,0), where Q=1/2, whereas Q(2,1/2)=−1/4. Moreover Q>−1/2 everywhere and Q(1/t,t)=t²−1/2, so the infimum −1/2 is not attained. This diagnoses the product-ideal reading only; it is not attributed to the tangency-minor ideal.

## Reproducibility and preservation

The independent arithmetic script was written and successfully run before the candidate verifier was inspected or rerun. It imports neither the candidate program nor its computed data. All ranks and identities use exact arithmetic. The candidate's initial 185-check verifier was also rerun and its output byte-matched its saved checks. The exact-only candidate and its verifier/output were preserved separately; the candidate's original files were not edited by the reviewer.

The finite-dimensional algebra checks support the explicit universal proof. They do not constitute a search over an SOS degree cutoff. Source PDFs and rendered pages are inspection evidence and are not proposed for republication. The review created no remote branch, commit, or pull request and made no external publication.

See the accompanying input/output hash manifest and final freeze addendum for the precise accepted versions. The separate EPSILON_SUPPLEMENT.md gives the strengthening as a standalone argument, including all real constant shifts.
