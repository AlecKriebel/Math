# Manuscript-first independent reconstruction

UTC2026-11-16T09:12:19+00:00. Scientific completion25%; not clearance. Root read all192actualTeX lines (8672B, SHA256317ab083bdfc4e986921e517b368de8e1501c7f9a24b4faef5b047fe1d504f43), all3PDF text pages and all3fresh own110dpi rasters. The unchanged54988B PDF has SHA256a84cfe9347d3d0ce05ef0fb22e8648ee64fd77992825729d24991cf0fc1d627d. Printed date23September2026, version1.0. Current peer mathematical findings, support programs/results and foreign proof bodies remain unread.

## Exact claim

For every positive definite real homogeneous polynomial p of positive degree on R^m, m>=1, degree d is even and at least2. Its symmetric polarization A has a real invertible basis z_i with p(z_i)=1 and0<A(z_j1,...,z_jd)<1 for every mixed ordered tuple. Pure ordered coefficients equal1. Ordinary monomial coefficients carry the multinomial factor; the assertion does not bound those unweighted coefficients by1. The change lies in GL_m(R), with no orthogonality, determinant, integrality or conditioning constraint.

## Independent derivation and hand checks

1. A positive minimum c of p exists on an auxiliary Euclidean unit sphere by continuity/compactness. Scale p and A by1/c; homogeneity gives p(x)>=||x||^d everywhere, including0, and choose a unit minimizer v with p(v)=1.
2. For each tangent u perpendicular to v, the polynomial difference p(v+tu)-(1+t^2||u||^2)^(d/2) is nonnegative and zero at0. First and second derivatives yield A(v^(d-1),u)=0 and Q(u,u)>=||u||^2/(d-1), Q(a,b)=A(v^(d-2),a,b). Thus the tangent bilinear slice is strictly positive definite, even if the minimum on the sphere is not isolated.
3. Take distinct tangent offsets w_1,...,w_(m-1) orthonormal, w_m=0. The m columns x_i=v+epsilon w_i are independent for every nonzero epsilon: tangent components force the first m-1 scalar coefficients to zero, then the radial one vanishes. Their determinant may tend to0, which is permitted.
4. For a tuple of offsets a_r, multilinearity gives N=1+epsilon^2 sum_(r<s)Q(a_r,a_s)+O(epsilon^3). Each p(v+epsilon a_r)=1+binom(d,2)epsilon^2 Q(a_r,a_r)+O(epsilon^3). Root re-expanded prod_r p(x_jr)-N^d and obtained coefficient(d/2)sum_(r<s)Q(a_r-a_s,a_r-a_s). The factor is correct: each diagonal term occurs d-1 times, each cross term twice.
5. Every mixed tuple contains two distinct offsets. The displayed quadratic coefficient is strictly positive, so the polynomial difference is positive for sufficiently small positive epsilon. There are finitely many tuples; one epsilon works simultaneously. The separate continuity check N(0)=1 keeps all N positive. Pure tuples give the identically zero difference. No uniform bound in m,d or an effective conditioning guarantee is required.
6. Taking positive d-th roots yields the geometric-mean inequality; undoing c scales both sides by c. Positive column scaling z_i=x_i/p(x_i)^(1/d) preserves invertibility and yields exactly the claimed unit pure coefficients and strict mixed coefficients.

Concrete controls calculated before external exposure:

- For p=(x^2+y^2)^2 and v=e_1, Q(e_2,e_2)=1/3, meeting the derivative lower bound exactly at d4; tangent positivity still suffices despite a nonisolated sphere minimum.
- For p=x^4+12x^2y^2+y^4, v=e_1 is a sphere minimizer, Q(e_2,e_2)=2. Set x_1=e_1+epsilon e_2,x_2=e_1. Tuple1112 has N=1+6epsilon^2 and polynomial-gap leading coefficient12. Tuple1122 has N=1+2epsilon^2 and gap leading coefficient16. These independently check repeated-index multiplicities and the d/2 factor. The original basis coefficient A(e_1,e_1,e_2,e_2)=2 also demonstrates why arbitrary existing coordinates are not sufficient.
- For d2, ordinary positive definite bilinear Cauchy-Schwarz supplies the strict upper bound for distinct independent columns, and columns close to v have positive pairing. This agrees with the general construction. Its ordinary xy coefficient is2A(z_1,z_2); no unweighted monomial bound should be inferred.
- For m1, mixed tuples do not exist; positive scalar normalization proves the whole statement.
- Merely nonnegative p=x^2 on R^2 would force normalized bilinear mixed coefficients to be plus/minus1; the required strict mixed bound fails. This explains the need for positive definiteness, without claiming every nonnegative form fails.
- Strict unnormalized geometric-mean inequalities and nonzero determinant define an open set; density permits rational raw columns. Unit-diagonal rescaling can introduce irrational numbers. No rational normalized basis or integral unimodular result follows.

## Remaining checks

No internal proof defect found. Still inspect the actual Brandes Problem11 wording, symmetric ordered-coefficient convention and absolute-value product; compare the2015 quadratic/pseudo-diagonal antecedent and avoid a global novelty claim. Inspect actual independent/adversarial proof and selected unchanged support code/results without rerunning a passed native campaign. Verify original source/ZIP/custody and the exact native version/date/assets/rights. Scope is an existence theorem, not a stable numerical algorithm, convexity theorem or quantitative reduction result. Follow-up defaults to none; no public page or canonical AA authority.
