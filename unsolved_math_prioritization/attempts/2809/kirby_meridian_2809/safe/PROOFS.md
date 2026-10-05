# Scoped deductions for the meridian-length question

## 0. Target and status

For every hyperbolic knot K in S³, let T be the intrinsic Euclidean torus bounding its maximal horocusp. Is the geodesic length m of its meridian μ at most 4? This is K3 Problem 3.11 / imported record 2809. This investigation does not prove or refute that assertion.

All deductions below are conditional on their stated inputs. Essential-surface existence, hyperbolicity, ambient S³, and a maximal-cusp metric are not certified by the accompanying arithmetic checks. No novelty or priority is claimed.

Fix a meridian-longitude basis (μ, λ) of H₁(T; Z). Write the corresponding lattice vectors as M, L, and A = |det(M,L)| > 0. A spanning slope, oriented to have longitude coefficient +1, has vector L + aM, a ∈ Z. Thus two spanning slopes with coefficients a ≠ b have intersection number n = |a-b| and determinant of magnitude nA. This remains true for the boundary of a nonorientable spanning surface; only its boundary curve is being oriented.

Credited geometric input: for an essential spanning surface S with χ(S) < 0, the geodesic length of its boundary slope is at most 6|χ(S)|. This follows from the pleated-surface cusp estimate, used in Burton–Kalfagianni, Theorem 2.4 and the proof of Theorem 4.1. We use that published estimate, not a new proof of it.

## 1. What exceptional filling and crossing number provide

The meridional filling is S³. Agol's 6-theorem says a slope of length greater than 6 produces a hyperbolike manifold; in particular its fundamental group is infinite. Since π₁(S³) is trivial, m ≤ 6. The maximal-cusp tangency causes no difficulty: if m > 6, shrink the cusp slightly and retain that strict inequality before applying the theorem.

Adams–Colestock–Fowler–Gillam–Katerman's Theorem 3.1 gives, for a c-crossing diagram of a hyperbolic knot, m ≤ 6 − 7/c < 6. The numerical bound 6 − 7/c is at most 4 exactly when c ≤ 7/2. In particular it does not, by itself, prove m ≤ 4 for any c ≥ 4. This is a limitation of this inequality, not a claim that a knot realizes its upper bound. No uniform extra loss of 2 is obtained.

## 2. An area-aware two-slope bound

### Proposition 2.1 (pure Euclidean statement)

Suppose a ≠ b and

|L+aM| ≤ P,  |L+bM| ≤ Q,  A ≥ A₀ > 0,

with P,Q > 0. Put n = |a-b| and R = P²Q² − n²A₀². Necessarily R ≥ 0, and

m² ≤ [P² + Q² + 2√R] / n².                 (2.1)

Also m < (P+Q)/n.

Proof. Let u = L+aM and v = L+bM. Then u−v = (a−b)M, and |det(u,v)| = nA. The planar Gram identity gives

(u·v)² = |u|²|v|² − n²A².

Since |u| ≤ P and |v| ≤ Q, the right side is nonnegative and at most R. Consequently

n²m² = |u−v|² = |u|²+|v|²−2u·v
       ≤ P²+Q²+2|u·v| ≤ P²+Q²+2√R.

For strictness of the simpler bound, equality in |u−v| ≤ |u|+|v| requires u and v to be collinear in opposite directions. Their nonzero determinant rules this out. Therefore n m < |u|+|v| ≤ P+Q. ∎

The cap expression is sharp as a Euclidean optimization statement. If 0 < D = nA₀ ≤ PQ, choose vectors of lengths P,Q with determinant magnitude D and nonpositive dot product −√(P²Q²−D²). Set M=(u−v)/n and L=v, and take coefficients a=n, b=0. The resulting lattice has area A₀ and equality in (2.1). This proves sharpness among these abstract marked flat tori, not realization as a knot cusp with specified essential surfaces.

### Corollary 2.2 (conditional knot certificate)

If a hyperbolic knot has two essential spanning surfaces with negative Euler characteristics −x and −y, distinct boundary slopes of intersection n, and a proven lower bound A₀ > 0 for its maximal cusp area, then (2.1) holds with P=6x and Q=6y. In particular,

x+y ≤ 2n/3  implies  m < 4.                 (2.2)

The weak version of this two-surface criterion is credited to Burton–Kalfagianni. The strict inequality in (2.2) follows immediately from the noncollinearity argument above. No claim of an unrecognized improvement is made.

For rational data, (2.1) proves m ≤ B > 0 exactly when the following test on its upper-bound expression succeeds:

R ≥ 0,  D_B = n²B²−P²−Q² ≥ 0,  D_B² ≥ 4R. (2.3)

The last comparison may be replaced by > to certify m < B. The sign check on D_B is indispensable before squaring. R < 0 indicates inconsistent alleged cap/area data and must not be called a positive certificate. Failing (2.3) is inconclusive about the actual length.

For example, n=8, P=Q=18, A₀=36 yields R=22032 and D₄=376, with D₄²=141376 > 4R=88128. The old cap-only bound is 36/8=9/2, whereas the area-aware bound is strictly below 4. A compatible abstract torus has M=(15/4,0), L=(−15,48/5), a=8, b=0. Both slope lengths have square 7929/25 < 324; A=36. These are algebraic control data only: no knot or essential surfaces realizing them are supplied.

For an adequate diagram with c crossings and Turaev genus g, the standard all-A/all-B pair has n=2c and x+y=c+2g−2. Consequently its cap-only bound is 3+(6g−6)/c, the published adequate-knot estimate. Thus c ≥ 6g−6 suffices for the bound 4. Neither all knots being adequate nor this inequality holding for every adequate knot is proved here.

## 3. Many boundary slopes do not improve the cap-only triangle method

### Proposition 3.1 (exact finite-dimensional optimum)

Given finitely many real numbers a_i and positive caps P_i, with at least two distinct a_i, define

B_pair = min_{a_i ≠ a_j} (P_i+P_j)/|a_i−a_j|.

Among all real coefficient vectors t satisfying Σt_i=0 and Σa_i t_i=1, the minimum of ΣP_i|t_i| equals B_pair. Consequently, using identities M=Σt_i(L+a_iM) and the triangle inequality with only the individual caps cannot outperform the best pair.

Proof. Any feasible t has positive and negative entries, with common total mass T=Σt_i⁺=Σt_i⁻>0. Couple these masses by w_ij=t_i⁺t_j⁻/T, so the first index ranges over positive entries and the second over negative entries. Its row and column sums are t_i⁺ and t_j⁻. Therefore

1 = Σ_ij w_ij(a_i−a_j),
Σ_i P_i|t_i| = Σ_ij w_ij(P_i+P_j).

For unequal a_i,a_j, P_i+P_j ≥ B_pair|a_i−a_j|; for equal coefficients this inequality still holds because its right side is zero. Hence the cost is at least B_pair Σw_ij|a_i−a_j| ≥ B_pair. A minimizing pair attains the lower bound using t_i=1/(a_i−a_j), t_j=−1/(a_i−a_j), and all other entries zero. ∎

This theorem does not rule out using cusp area, correlated length information, topology of surface intersections, or genuinely stronger estimates. It rules out one specific attempt to gain a universal factor merely by combining many independent surface caps. For any knot violating the desired bound, every essential pair with negative Euler characteristic must satisfy x+y > 2n/3. Producing a good pair universally remains an unproved extra assertion; existence of any essential spanning surface alone does not supply it.

## 4. A numerical-model obstruction to a topology-free conclusion

Let T=R²/⟨(5,0),(0,6/5)⟩, marked by M=(5,0) and L=(0,6/5). Then m=5, A=6, and the shortest nonzero lattice vector has length 6/5. Indeed a nonzero vector (5p,6q/5) either has p≠0 and length at least 5, or p=0, q≠0 and length at least 6/5. The shortest longitude-coefficient-one slope is L, of length 6/5.

The numerical assignment c=8 satisfies the individual crossing-number inequalities from §1 and the associated He-surface budget:

m=5 ≤ 6−7/8=41/8,
8m+|L| = 206/5 ≤ 42 = 6(8−1),
|L| ≤ 5·8−6,
A ≤ 9·8·(1−1/8)².

It also satisfies m≤6 and systole>1. Thus these selected necessary numerical restrictions on a marked flat torus do not force the bound 4. The assignment c=8 is just a parameter in the inequalities; it is not the crossing number of a constructed knot. No hyperbolic manifold, cusp, S³ filling, or counterexample to the target is realized by this torus. In particular no theorem asserting that every such numerical assignment comes from a knot may be inferred.

## 5. What augmentation and geometric limits would need

### Proposition 5.1 (conditional transfer)

Let N be a finite-volume hyperbolic link exterior with a distinguished cusp and a marked slope μ whose length on some embedded horotorus is L₀>4. Suppose there is a sequence of fillings of all the other cusps such that:

1. each resulting one-cusped hyperbolic manifold is S³ minus a knot, and the surviving μ is its meridian;
2. each resulting cusp admits an embedded horotorus T_j for which the lengths of this marked slope converge to L₀.

Then the universal meridian bound 4 is false.

Proof. Put ε=(L₀−4)/2>0. For all sufficiently large j, the length on T_j exceeds L₀−ε>4. Expanding an embedded horocusp to its maximal size multiplies every length on its boundary by a factor at least one. Therefore the maximal-cusp meridian of those knots also has length greater than 4. ∎

This is a precise sufficient construction, not an assertion that its hypotheses hold for the known link examples. Standard long Dehn filling explains why hypothesis 2 is plausible for a suitably controlled family. It does not supply hypothesis 1, including the peripheral marking. No S³-preserving long-filling sequence for a link with L₀>4 was constructed.

In the positive direction, Purcell's generalized augmented-link theorem gives a knotting-strand meridian strictly below 4 before filling. Convergence gives bounds for sufficiently long fillings of a fixed parent, but by itself does not cover every filling, or every parent uniformly. The quantifier obstruction is elementary: f_N(n)=4−1/N+1/n has lim_{n→∞} f_N(n)=4−1/N<4 for every positive N, while f_N(N)=4 and f_N(n)>4 for n<N. These scalar examples make no assertion about any knot's actual deformation; they show why convergence alone cannot justify the proposed universal inference.

## Exact remaining gap

No argument here turns the knot-in-S³ hypothesis into either a universal good pair of essential spanning surfaces, a uniformly adequate area-aware certificate, or a stronger exceptional-filling estimate at length 4. Conversely, no actual hyperbolic knot with a rigorously certified maximal-cusp meridian greater than 4 is given. Those are the original alternatives; none has been replaced by a finite computation, an abstract torus, a multi-component link, or a limit statement.
