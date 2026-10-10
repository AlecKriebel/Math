# Independent audit of the cubic cone barrier

Public proof-only edition. Recorded audit date: 10 October 2026. This AI-assisted audit is unrefereed; acceptance does not mean external human peer review or journal acceptance.

## Verdict

**Accept the complete mathematical solution for problem 30003439 / OWR-15219-008.** No mathematical correction is required. The frozen proof establishes that

\[
K=\{(x,y,z)\in\mathbb R^3:x,y,z\ge0,\ xy^2\ge z^3\},\qquad
F=-25\log\bigl(z(xy^2-z^3)\bigr)
\]

has all the requested properties: a regular algebraic convex cone, a 100-normal barrier on its interior, negative directional third-derivative curvature, and nonexistence of **any** homogeneous hyperbolic polynomial whose hyperbolicity cone is this cone in the original space.

This is a mathematical audit, not formal proof-assistant verification, publication acceptance, or a novelty/priority determination. No claim about all regular cones is accepted or made. The cone itself is explicitly present in Hildebrand's earlier classification. The finite checks below support the universal arguments; they are not their substitute.

This edition binds the distributed [PROOF.md](PROOF.md): 13,923 bytes, SHA-256 `9577476ee2c0fd2e3d12ab1265201d8b99f6ef50a9060e245c46f872dd673302`. The accepted proof's full mathematical argument is preserved. The publication proof also includes this audit's direct mixed self-concordance bridge and explicit endpoint PSD decomposition. These were optional expository enhancements, not corrections to the accepted theorem.

The audit independently checked every byte count/hash and exact membership of the original frozen proof package, without modifying it. The author's test script was neither imported nor executed for the audit. The original package pin and complete editorial reconstruction remain part of edition-preparation verification; the distributed proof and audit are self-contained.

## Exact target and source conventions

Tunçel's 2017 contribution, printed pages 797–800 of Oberwolfach Report 14/2017, asks on printed page 799 for an algebraic convex cone admitting a normal barrier with negative curvature while not being a hyperbolicity cone. In that statement, algebraic means a solution set of homogeneous polynomial inequalities. Negative curvature is explicitly the negative-semidefiniteness of the matrix obtained by placing a cone direction in one slot of the third differential. I read the contribution and visually inspected the question on physical PDF page 29. [Original report](https://publications.mfo.de/bitstream/handle/mfo/3578/OWR_2017_14.pdf?isAllowed=y&sequence=1)

The cited Nesterov–Tunçel source defines a regular cone as closed, convex, pointed and with nonempty interior; normality is self-concordance together with finite logarithmic homogeneity. Its scalar cubic self-concordance convention is the one proved in the author manuscript. Section 6 gives the same directional third-derivative definition. Section 9.2's Hankel example gives a barrier on the dual spectrahedral cone, not on its primal nonnegative-polynomial cone. The duality shortcut excluded in the candidate is indeed unjustified in general. [2014 preprint](https://arxiv.org/abs/1412.1857)

The current arXiv listing inspected on 2026-10-10 gives version 2 of Dahl–Tunçel–Vandenberghe, submitted 2026-06-12. The inspected author-hosted PDF has that banner but an internal revision date of 2026-06-16. Its Section 2.2 uses the matrix self-concordance convention, and Definition 3.1 defines negative curvature as concavity of every fixed cone-direction gradient. Section 6 still poses the universal existence question, which this example does not resolve. The actual definitions, rather than only the abstract, were read; pages 5 and 8 were visually inspected. [Version history](https://arxiv.org/abs/2509.10263), [inspected PDF](https://www.math.uwaterloo.ca/~ltuncel/publications/2509.10263.pdf)

For a smooth function on a convex open domain, the Hessian of the scalar map \(a\mapsto DF(a)[h]\) is \(D^3F(a)[h]\). Thus negative-semidefiniteness at every base point is exactly the 2026 concavity condition. Section “Matrix self-concordance bridge” below independently checks the 2026 self-concordance convention as well, without relying on an unstated polarization equivalence.

## Geometry and finite boundary behavior

All four inequalities are homogeneous, and their feasible set is closed. The cone lies in the nonnegative orthant and consequently contains no line. The strictly feasible point \((2,1,1)\) proves nonempty interior in \(\mathbb R^3\). Every interior point has positive coordinates and \(xy^2>z^3\): a zero coordinate lies on an orthant supporting plane, while equality with positive coordinates can be violated by decreasing \(x\). Conversely these strict inequalities give an open neighborhood in the cone.

The independent derivative calculation gives

\[
D^2(x^{1/3}y^{2/3})=
-\frac29x^{-5/3}y^{-4/3}
\begin{pmatrix}y^2&-xy\\-xy&x^2\end{pmatrix}.
\]

Its displayed inner matrix is the outer product \((y,-x)(y,-x)^T\), so the weighted geometric mean is concave on the positive orthant. Taking limits gives concavity on the nonnegative orthant. The cone is the intersection of its hypograph with \(z\ge0\), hence convex. No issue involving a nonintegral power remains in the defining inequalities: the actual cone is described by the four stated polynomials.

Set \(p=xy^2-z^3\). At any finite boundary point either \(z=0\) or \(p=0\); zeros of \(x\) or \(y\) in the cone force \(z=0\). Any interior sequence approaching that point has \(zp\to0^+\). Consequently \(F\to+\infty\), including on the whole extra facet, its edges and the vertex. Outside the closed cone there is a neighborhood disjoint from its effective domain. These facts establish lower semicontinuity of the extended-real function at every point. The interior formula is smooth and finite.

## Independent derivatives and scalar self-concordance

I computed the derivatives from the polynomial \(p\), independently of the author's script. If subscripts denote ordinary partial derivatives, then

\[
f_{ij}=\frac{p_i p_j}{p^2}-\frac{p_{ij}}p+
\frac{\mathbf1_{i=j=z}}{z^2},
\]

\[
f_{ijk}=-\frac{p_{ijk}}p+
\frac{p_{ij}p_k+p_{ik}p_j+p_{jk}p_i}{p^2}
-\frac{2p_i p_j p_k}{p^3}
-\frac{2\mathbf1_{i=j=k=z}}{z^3}.
\]

All 27 tensor entries agree identically with separate direct symbolic differentiation. A further complementary calculation expands the quartic polynomial \(zp\) on rational affine lines and reads the derivatives of its logarithm from its first three normalized coefficients. This bypasses both the tensor formula and the author's slack-variable derivation.

For the analytic estimate, let \(g=z^3/y^2\), \(\delta=x-g>0\), and for a direction \(u\) use the author's \(b=u_y/y\), \(c=u_z/z\), \(w=(u_x-g(3c-2b))/\delta\). Put \(v^2=6g(c-b)^2/\delta\), \(Q=2b^2+c^2\). Independent calculation verifies exactly

\[
D^2 f[u,u]=w^2+v^2+Q=:S,
\]

\[
D^3 f[u,u,u]=-2w^3-3wv^2+(c-4b)v^2-4b^3-2c^3.
\]

In particular, the potentially error-prone third derivative of \(g\) is precisely \(6g(c-b)^2(c-4b)\). There is no missing chain-rule term.

The quadratic form \(S\) is positive definite: if it vanishes, \(b=c=0\), and then \(w=u_x/\delta=0\). Moreover

\[
9Q-(c-4b)^2=2(b+2c)^2\ge0,
\qquad
2|b|^3+|c|^3\le Q^{3/2}.
\]

The latter follows, for example, by viewing \((\sqrt2|b|,|c|)\) as a Euclidean vector and using that its cubic norm is bounded by its quadratic norm, together with \(1/\sqrt2\le1\). Bounding the four groups in the cubic identity gives \(|D^3f[u,u,u]|\le10 S^{3/2}\). Thus

\[
|D^3(25f)[u,u,u]|\le250S^{3/2}
=2\bigl(D^2(25f)[u,u]\bigr)^{3/2}.
\]

The estimate is deliberately nonoptimal but uniform over all base points and directions. It does not deteriorate when the base point approaches a boundary stratum.

### Matrix self-concordance bridge

At a fixed base point define a genuinely linear functional

\[
v_u=\sqrt{6g/\delta}\,(c_u-b_u),\qquad \ell_u=c_u-4b_u,
\qquad \|u\|_f^2=w_u^2+v_u^2+2b_u^2+c_u^2.
\]

Polarizing the exact cubic, or directly contracting the independently derived tensor, gives

\[
\begin{aligned}
D^3f[h,u,u]={}&-2w_h w_u^2
-w_hv_u^2-2w_uv_hv_u\\
&+\tfrac13(\ell_hv_u^2+2\ell_uv_hv_u)
-4b_hb_u^2-2c_hc_u^2.
\end{aligned}
\]

The four groups are bounded in absolute value by respectively \(2,3,3,2\) times \(\|h\|_f\|u\|_f^2\). For the third group use \(|\ell_a|\le3\|a\|_f\). For the last, Cauchy–Schwarz gives

\[
|4b_hb_u^2+2c_hc_u^2|
\le2\sqrt{2b_h^2+c_h^2}\sqrt{2b_u^4+c_u^4}
\le2\|h\|_f\|u\|_f^2.
\]

It follows directly that \(|D^3F[h,u,u]|\le2\|h\|_F\|u\|_F^2\), exactly the matrix convention in the 2026 source. This is an optional strengthening of the exposition, not a repair needed for the 2017 target.

## Normality and parameter

Since \(zp\) has degree four, \(F(ta)=F(a)-100\log t\). Differentiate this identity to get \(D^2F(a)a=-DF(a)\) and \(a^TD^2F(a)a=100\). Positive definiteness then implies

\[
DF(a)^T(D^2F(a))^{-1}DF(a)=100.
\]

Thus the claimed parameter is the actual homogeneity/gradient-bound parameter, not the unscaled value four. Smoothness, domain convexity, positive Hessian, boundary blow-up, closedness and self-concordance have all been checked. These prove the precise normal-barrier requirements.

## Universal negative curvature and degeneracies

### Normalizing the base point

The diagonal map \(D=\operatorname{diag}(y^2/z^3,1/y,1/z)\) is invertible with positive diagonal entries and satisfies the cone-automorphism relation \(ab^2=c^3\). It sends the base point to \((r,1,1)\), where \(r=xy^2/z^3>1\). The identity \(f(Da)=f(a)-4\log c\) gives

\[
D^3f(a)[h,u,u]=D^3f(Da)[Dh,Du,Du].
\]

In particular the relevant matrices are related by a genuine congruence, with directions transformed as well. Exact tests at 45 nonnormalized rational base points and cone directions independently check this relation. There is no assumption that the diagonal group acts transitively on the whole interior: the invariant \(r\) is retained and treated for every value greater than one.

### Exhausting every cone direction

If \(h_y>0\), set \(t=h_z/h_y\). Then

\[
h=h_y(t^3,1,t)+\bigl(h_x-h_z^3/h_y^2\bigr)e_x.
\]

Both coefficients are nonnegative. If \(h_y=0\), the cone inequalities force \(h_z=0\), leaving a nonnegative multiple of \(e_x\). This also covers \(h=0\). Thus no cone direction is omitted. Boundary points with \(h_z=0\), including the entire facet, occur through \(t=0\) and the \(e_x\) direction.

### Exact matrix and positivity certificate

Set \(s=r-1>0\), \(h(t)=(t^3,1,t)\), and \(M=-s^3D^3f(r,1,1)[h(t)]\). All six independent entries in the author's displayed NC1 matrix were reproduced exactly from the tensor above. Its first leading principal minor is \(2(t-1)^2(t+2)\), and the next two are

\[
\Delta_2=4s(t-1)^2P,\qquad \Delta_3=8s^4(t-1)^2R,
\]

with

\[
P=2(t+2)s^2-3(t-1)(3t+5)s+3(t-1)^2(t+2)^2,
\]

\[
R=(t+2)\bigl(2ts^2-3(t-1)(3t+1)s+3(t-1)^2(t^2+4t+1)\bigr).
\]

For \(0\le t<1\), all terms in these expressions are nonnegative and the constant terms are strictly positive. At \(t=0\) specifically, \(P=4s^2+15s+12\) and \(R=6(s+1)\), so there is no division by zero or neglected ray.

For \(t\ge1\), the independently verified square identities are

\[
8(t+2)P=[4(t+2)s-3(t-1)(3t+5)]^2
+3(t-1)^2(8t^3+21t^2+6t-11),
\]

\[
8tR/(t+2)=[4ts-3(t-1)(3t+1)]^2
+3(t-1)^3(8t^2+13t+3).
\]

The first remainder polynomial becomes \(8v^3+45v^2+72v+24\) at \(t=1+v\). It is strictly positive for \(v\ge0\). For \(t>1\) both remainders are strictly positive. At \(t=1\), \(P=R=6s^2>0\). Therefore \(P,R>0\) for the full domain \(s>0,t\ge0\).

For \(t\ne1\), the three leading minors are strictly positive. Equivalently, the LDL pivots are

\[
2(t-1)^2(t+2),\quad 2sP/(t+2),\quad 2s^3R/P,
\]

all positive. Sylvester's positive-definite criterion is correctly applied here. It is not incorrectly used at the singular exceptional direction.

At \(t=1\) the matrix is exactly

\[
M=2s^2\begin{pmatrix}0&0&0\\0&2s+3&-3\\0&-3&s+3\end{pmatrix}.
\]

The lower block has positive diagonal and determinant \(s(2s+9)>0\); hence \(M\) has rank two and is positive semidefinite. Its kernel is \(\mathbb R e_x\). Strict negative definiteness is neither true nor required.

For the endpoint \(e_x\), the author's limit \(h(t)/t^3\to e_x\) is valid by linearity of the third derivative and closedness of the PSD cone. Independently, I obtained the stronger explicit identity

\[
-s^3D^3f(r,1,1)[e_x]
=2(1,2,-3)^T(1,2,-3)+6s(0,1,-1)^T(0,1,-1).
\]

Both summands are positive semidefinite and this matrix has rank two, with kernel \(\mathbb R(1,1,1)\). This separately verifies the infinite-ray endpoint without a limiting argument. The notation in this display treats the parenthesized triples preceding the transpose as row vectors.

Linearity in \(h\), the exhaustive direction decomposition, congruence under the diagonal map, and positive scaling by 25 complete the universal curvature argument. The formulas cover every finite positive \(s\); no uniform bound at the excluded base boundary \(s=0\) is needed.

## Excluding all hyperbolic defining polynomials

### Irreducibility and the whole boundary patch

Over the UFD \(\mathbb R[y,z]\), the polynomial \(p=y^2x-z^3\) is primitive because the two coefficients have gcd one. In the fraction field \(\mathbb R(y,z)\), it has degree one in \(x\), and is irreducible. Gauss's lemma therefore proves real irreducibility. The same proof even works over the complex coefficient field, although that stronger assertion is unnecessary.

The curved patch \(B=\{(z^3/y^2,y,z):y,z>0\}\) is contained in the topological boundary of \(K\), not merely in its algebraic zero set. Varying \(x\) up or down near any such point gives interior and exterior points. If a polynomial \(H\) vanishes on the boundary, then

\[
y^{2d}H(z^3/y^2,y,z)=0\qquad (y,z>0),
\]

where \(d\) may be taken to be the degree of \(H\). This is a polynomial identity because a real polynomial vanishing on a nonempty open set is identically zero. Thus \(p\) divides \(H\) over \(\mathbb R(y,z)[x]\); primitivity gives divisibility in \(\mathbb R[x,y,z]\). Equivalently, clearing denominators and using that the irreducible \(p\) does not divide \(y\) yields the same result by primality. This supplies the required Zariski-density argument on the curved component even though the full boundary has the additional facet.

### Why any hyperbolic representation must vanish there

Under the source convention, \(H\) hyperbolic in direction \(e\) has \(H(e)>0\), and its cone is the closure of the set of points with positive roots of \(\lambda\mapsto H(a-\lambda e)\). At \(a=e\), every root is one, so \(e\) belongs to the cone's interior. Roots vary continuously, with degree fixed by the nonzero leading coefficient \((-1)^dH(e)\). At a point in the boundary of the closed positive-root cone, at least one root must be zero; otherwise all roots stay positive on a neighborhood. Therefore \(H\) vanishes on that boundary. A constant positive polynomial gives all of \(\mathbb R^3\), so cannot be an exception for this proper cone.

Consequently any proposed representation of \(K\) forces \(e\in\operatorname{int}K\) and \(p\mid H\). This conclusion does not assume \(H=p\), irreducibility of \(H\), minimal degree, or a particular representation.

### A nonreal-root obstruction for every interior direction

For every \(e\in\operatorname{int}K\), define \(a=(e_xe_y^2)^{1/3}\) and \(b=e_z\). Then \(a>b>0\). Along \(v+te\), with \(v=(0,0,1)\),

\[
p(v+te)=a^3t^3-(1+bt)^3
=((a-b)t-1)\bigl((a^2+ab+b^2)t^2+(a+2b)t+1\bigr).
\]

The quadratic discriminant is \(-3a^2<0\). Thus it has two nonreal roots for **every** possible hyperbolicity direction in the interior. Its leading coefficient is positive; the cubic also has nonzero leading coefficient since \(a>b\).

Write \(H=pQ\). Since \(H(e)>0\) and \(p(e)>0\), \(Q(e)\ne0\), so the restricted product is a genuine nonzero polynomial. Its \(p\) factor's nonreal roots cannot cancel in a polynomial product. Replacing \(t\) by \(-t\) handles the source's sign convention. This contradicts hyperbolicity and excludes every homogeneous polynomial representation. A linear isomorphism to a hyperbolicity cone in the same dimension would pull back a hyperbolic polynomial, and is excluded as well. No assertion about higher-dimensional spectrahedral lifts is needed.

## Attribution and bounded literature screen

Hildebrand's Theorem 3.2, family 5, explicitly lists the one-sided cone \(0\le x_2\le x_1^{1/p}x_3^{1/q}\), with \(1/p+1/q=1\). Taking \(p=3\), \(q=3/2\), and \((x_1,x_2,x_3)=(x,z,y)\) gives exactly the candidate cone. I read the classification around the theorem and the Section 4.2 setup and visually inspected its family list. The source studies complete hyperbolic affine spheres; the adjective “hyperbolic” there is not a polynomial hyperbolicity assertion. The candidate's credit and the limited role assigned to this source are accurate. [Hildebrand source](https://arxiv.org/abs/1305.4814)

A bounded live search covered eleven variants combining negative curvature, algebraic convex cones, power cones, one-sided power cones and the cubic monomial. It recovered the original question and related conic-optimization literature but did not identify an exact prior certificate for this specific pair \((K,F)\) in the inspected results. This says nothing conclusive about priority or worldwide literature absence. Search-engine date labels were not treated as publication dates. The preserved attribution to the known cone family and the explicit absence of a novelty claim are appropriate.

## Reproducibility and adversarial controls

The independently authored verifier records **347 successful checks and 11 rejected negative controls** in each of normal Python and Python with `-O`. The reports agree apart from the optimization-mode field. The code uses explicit exceptions instead of assertions, so optimization does not erase the checks.

The verification includes:

- External manifest pin, every listed byte count/hash, safe unique paths and exact package membership.
- Independent log-composite Hessian and full third tensor, then a second direct symbolic differentiation.
- Every NC1 entry, both leading-minor factors, both square certificates and every endpoint formula.
- Exact SC identities, the mixed matrix bridge, homogeneity identities and scaling constants.
- All seven principal minors for 63 rational pairs spanning \(s=10^{-6}\) through \(10^6\), \(t=0,1\), nearby rationals on both sides of one, and \(t=10^6\).
- Forty-five independently generated nonnormalized rational bases and arbitrary cone directions, all-minor PSD checks and exact congruence checks.
- Forty-five exact polynomial-log jet calculations and scalar self-concordance inequalities.
- The discriminant and factorization, and complementary boundary-restriction kernel dimensions for homogeneous polynomials of degrees zero through six.

The negative controls detect a changed author pin, a changed matrix coefficient, false strictness at \(t=1\), a reversed cone direction, false strictness of the \(e_x\) matrix, an insufficient scale justified by this loose estimate, an incorrect parameter, omission of \(-\log z\), a false real-root claim, failure of facet blow-up without \(-\log z\), and an off-diagonal transcription error.

One useful exact control demonstrates the importance of the added barrier term. For \(f_0=-\log p\), at base \((5,1,1)\) and cone direction \((8,1,2)\), the matrix \(-(5-1)^3D^3f_0[h]\) has determinant \(-24576\). It therefore is not positive semidefinite. The accepted proof's extra \(-\log z\) term is doing substantive work.

## Required changes and acceptance boundary

There are **no required mathematical corrections**. The explicit \(e_x\) sum-of-squares matrix and direct matrix self-concordance bridge are useful optional expository additions, already supplied in this audit. The original manuscript's pending-audit language was historically accurate at creation. This publication edition supersedes it with the completed acceptance and includes both optional expository enhancements in the proof.

Acceptance applies only to the original accepted mathematical argument, the audit-supplied enhancements reproduced here, and the exact one-sided cone/barrier pair. It does not extend to a signed power cone, to arbitrary power exponents, to dual barriers, to all regular cones, or to any novelty claim. The recorded computations are supplementary historical evidence. Edition preparation rechecked frozen byte identities and publication integrity but did not rerun the original mathematical programs or perform new scholarly retrieval, source-text inspection, or literature search. No analytic claim depends on an omitted executable or raw output. Programs, raw outputs, datasets, copied source documents/text/images and private coordination material are excluded from this proof-only edition.
