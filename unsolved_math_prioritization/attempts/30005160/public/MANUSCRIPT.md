# Fixed exponent real majorants on integer frequency sets

## Abstract

The constant-one real Fourier majorant problem asks which integer frequency sets admit coefficientwise majorization at one prescribed exponent. The results assembled here give complete classifications for $0<p<2$ and $3\leq p<4$, and a finite rational-affine candidate reduction for every fixed positive noneven exponent in every fixed dimension. The latter follows from a uniform bound on the mass of every primitive affine circuit, proved using a two-scale coefficient expansion and a negative singular tail.

For $4<p<6$, all odd collinear triples $\{0,2,K\}$ with $K\geq7$ and their surviving noncollinear four-circuit analogues are excluded. The coefficients in these exclusions may depend on the prescribed exponent. Separate fixed-coefficient witnesses hold throughout the interval. The remaining low-exponent centered-cross problem is narrowed by robust radial-cone theorems, strong-center coefficient regions, and exact partial comparisons. Several dominant and symmetric coefficient boxes are also positive on the two surviving non-AP triple supports.

The full fixed-exponent classification is **UNSOLVED**. Novelty and priority are **unestablished**. This is an editorially assembled review candidate, not a claim of publication. All substantive statements come from accepted authored proofs; their exact source bindings, computational dependencies, and remaining presentation-review status are recorded in the [inventory](CONTENT_AND_DEPENDENCIES.md).

## 1  The property and published starting points

Let $e(t)=\exp(2\pi i t)$, and equip $\mathbb T^d$ with normalized Haar measure. For $\Gamma\subseteq\mathbb Z^d$ and $p>0$, write $\operatorname{MP}_p(\Gamma)$ when

$$
 \int_{\mathbb T^d}\left|\sum_{n\in\Gamma}a_ne(n\cdot x)\right|^p\,dx
 \leq
 \int_{\mathbb T^d}\left|\sum_{n\in\Gamma}A_ne(n\cdot x)\right|^p\,dx
$$

for every pair of **finitely supported real** coefficient families with $|a_n|\leq A_n$. The finite-support convention applies equally to infinite sets and makes no assertion about undefined infinite Fourier sums. The exponent is fixed before the coefficients are quantified.

This property differs from simultaneous validity for every exponent, a majorant estimate with a constant larger than one, unit-coefficient tests, and unconditional norm invariance. These distinctions matter both mathematically and when comparing prior literature.

At every positive even integer, all frequency sets have the property. Affinely independent sets have it for every $p>0$, by the published theorem of Gressman, Guo, Pierce, Roos and Yung [R1, Proposition 8.2 and Lemma 8.3], which in fact allows complex coefficients. Their dominant-coefficient expansion [R1, Proposition 4.1] is the analytic starting point for the circuit obstructions below. Circle/disk differentiation and the planar bisubharmonic framework are credited to Baernstein and Culverhouse [R2]. Exact theorem numbers, primary full-text links, and attribution boundaries are given in [References](REFERENCES.md).

For $p\geq1$, domination of all real sign vertices at prescribed nonnegative bounds implies the entire coefficient-box inequality. Indeed the power moment is convex in the real coefficient vector, and the box is the convex hull of its sign vertices. A box theorem fixes the bounds first; it need not impose its sufficient condition again on each interior vector. This convexity step is not used for $p<1$.

## 2  Circuit obstructions and the finite shape theorem

### 2.1  Primitive circuits and the first necessary tests

A primitive affine circuit is an integer relation $\lambda=(\lambda_j)$ on a minimally affinely dependent finite set of distinct frequencies $n_j$, normalized by

$$
 \sum_j\lambda_j=0,\qquad \sum_j\lambda_jn_j=0,\qquad
 \gcd(\lambda_j)=1.
$$

Its positive and negative coefficient sums agree. Their common value is its mass:

$$
 K=\sum_{\lambda_j>0}\lambda_j
   =\sum_{\lambda_j<0}(-\lambda_j)\geq2.
$$

Set $q=p/2$ and suppose $q$ is nonintegral. Place a dominant coefficient at one circuit vertex and small signed coefficients at the others. The first sign-sensitive term in the convergent expansion gives the necessary conditions

$$
 \binom qK\binom q{K-|\lambda_i|}>0
 \qquad\text{at every circuit entry }i. \tag{2.1}
$$

The real sign choice, multinomial factors, and analytic remainder are proved in [Proof 01](proofs/01_circuit_obstructions.md). These conditions alone are not sufficient: the actual counterexamples in Section 5 pass every one of them.

### 2.2  A uniform mass bound at every noneven exponent

**Theorem A.** Fix $p>0$ that is not a positive even integer, and put $m=\lfloor p/2\rfloor$. If $\operatorname{MP}_p(\Gamma)$ holds, then:

- If $m=0$, the set is affinely independent.
- If $m\geq1$ is odd, every primitive affine circuit has $K\leq2m$.
- If $m\geq2$ is even, every primitive affine circuit has $K\leq2m+1$.

In the last case, a circuit of maximal mass $K=2m+1$ must, up to permutation and overall sign, have one of the forms

$$
 (K,-(K-b),-b),\qquad (K-b,b,-(K-b),-b),
$$

where $b$ is even, $2\leq b\leq m$, and $\gcd(K,b)=1$. These are necessary forms, not positive classifications.

The complete proof is [Proof 29](proofs/29_uniform_mass_and_finite_shapes.md). The binomial signs already give the odd-$m$ bound. For even $m$, a hypothetical circuit with $K>2m$ has exactly one large odd entry on each sign side; all other entries are even and have total at most $m$ on either side. The essential additional step retains a second coefficient at a non-small value $y\in(0,1)$ and sends all remaining coefficients to zero at scale $t$.

More precisely, choose an odd base entry $K-e$, an even entry of magnitude $b$, and flip the other odd entry. Put $\ell=K+e-b$ and let $D$ be the product of the factorials of the remaining entry magnitudes. The exact leading positive-minus-signed coefficient is

$$
 4\frac{e!K!}{b!D}\binom qe\binom qK y^b
 {}_2F_1(e-q,K-q;b+1;y^2)t^\ell.
$$

The factors outside the hypergeometric series are positive. Its eventual coefficients are negative with size comparable to $N^{\ell-p-2}$. If $\ell>p+1$, their sum tends to minus infinity as $y$ approaches one. First choose a fixed $y<1$ making that leading coefficient negative; only then choose $t$ small enough for the uniformly convergent expansion and its remainder. This order produces an actual coefficient witness, rather than a formal assertion at a singular boundary. It excludes $K\geq2m+3$ and gives the maximal-mass pattern restrictions. The exact multinomial factor and both possible sign-side positions of the even entry are included in the proof.

### 2.3  Finite cardinality and finitely many rational affine shapes

For $m\geq1$, define

$$
 B=\begin{cases}2m,&m\text{ odd},\\2m+1,&m\text{ even}.
 \end{cases}
$$

**Corollary.** If a nonempty MP set has augmented affine rank $r$, then

$$
 |\Gamma|\leq B(2B+1)^r,\qquad 1\leq r\leq d+1.
$$

For each fixed $p$ and $d$, there are only finitely many possible rational-affine equivalence classes of MP sets.

Choose any affine basis and write an additional augmented point as a rational combination of its augmented basis vectors. Its primitive fundamental relation has denominator $1\leq t\leq B$ and numerators in $[-B,B]$. The coordinate vector therefore lies in the explicit finite grid

$$
 G_{B,r}=\left\{(-\lambda_1/t,\ldots,-\lambda_r/t):
 1\leq t\leq B,\ |\lambda_i|\leq B,
 \lambda_i\in\mathbb Z,\ \sum_i\lambda_i=-t\right\}.
$$

The normalized configuration is a subset of this grid containing its standard basis. Projecting the sum-one hyperplane and multiplying by $\operatorname{lcm}(1,\ldots,B)$ gives integer representatives. A rational-affine change preserves the entire labelled integer affine-relation lattice; adding a common phase identifies the same character Haar law and therefore the same coefficient-dependent norm function. All details, including the direct argument for infinite sets, are in [Proof 29, Section 6](proofs/29_uniform_mass_and_finite_shapes.md).

This is a finite candidate reduction, not a sufficient criterion or an algorithm deciding every candidate's universal coefficient inequalities. The earlier minimum-determinant finiteness argument and odd-$m$ grid are retained only as optional background in [Proof 06](proofs/06_fixed_exponent_finiteness.md) and [Proof 08](proofs/08_finite_candidate_reduction.md).

## 3  Exact classifications below four

### 3.1  Exponents between zero and two

**Theorem B.** For every fixed $0<p<2$, $\operatorname{MP}_p(\Gamma)$ holds exactly when $\Gamma$ is affinely independent.

The sufficient direction is the published result cited above. An affine dependence contains a circuit with an odd entry of magnitude strictly between zero and $K$. For $0<q<1$, the two positive integer indices in (2.1) then have opposite binomial signs, giving a finite witness to failure. See [Proof 01, Section 2](proofs/01_circuit_obstructions.md).

### 3.2  Exponents from three to four

**Theorem C.** For every fixed $3\leq p<4$, the following are equivalent:

1. $\operatorname{MP}_p(\Gamma)$ holds.
2. Every primitive affine circuit has mass two, with the condition vacuous for affinely independent sets.
3. The set is a finite affine join of the following blocks, up to rational affine equivalence on their spans:
   - a singleton;
   - a centered cross with its center, $\{c,c\pm u_1,\ldots,c\pm u_n\}$;
   - a center-free cross, $\{c\pm u_1,\ldots,c\pm u_n\}$;
   - a two-layer simplex, $\{a_i,a_i+v\}$.

Cross directions are independent; for a two-layer simplex, $v$ and the differences $a_i-a_1$ are independent. The list can overlap, as with a parallelogram. The empty set is the empty join. Every displayed join is positive for **all $p\geq3$**; necessity is not asserted at noneven exponents above four.

An affine join means that the augmented relation lattice is the direct sum of the block relation lattices. The necessity argument in [Proof 01](proofs/01_circuit_obstructions.md) actually applies throughout $2<p<4$. [Proof 02](proofs/02_mass_two_structure.md) gives the complete elementary mass-two structure: AP-containing components are centered crosses, while AP-free components have a totally unimodular representation and form paired blocks. The exceptional seven-element tetrad pattern is excluded directly. No external matroid classification is assumed.

The analytic proof is in [Proofs 01](proofs/01_circuit_obstructions.md), [03](proofs/03_centered_cross_above_three.md), and [04](proofs/04_radial_joins.md). The centered-cross scalar argument uses the nonnegative fourth distributional derivative of $|x|^p$ for $p\geq3$. The join proof first establishes a radial test class stable under adding independent radial noise. The direct-sum relation lattice gives independent rotationally invariant block values, so the signs can be replaced one block at a time. An isolated power inequality is not used as a substitute for this robustness.

For a nonempty mass-two configuration of affine dimension $r-1$,

$$
 |\Gamma|\leq2r-1.
$$

Equality is exactly a single centered cross with its center in positive affine dimension, or a singleton in dimension zero. This sharp size statement is [Proof 02, Section 7](proofs/02_mass_two_structure.md).

### 3.3  Positive blocks below three and the remaining block

Every three-point arithmetic progression is positive for all $p\geq2$, by the direct ellipse-projection proof in [Proof 05](proofs/05_arithmetic_progressions.md). Consequently the one-dimensional classification is complete for $2<p<4$: the nonempty allowed sets are at most two points or an AP triple.

Every affine join of singletons, AP triples, two-layer simplices, and center-free crosses is positive for all $p\geq2$. The required AP comparison after arbitrary independent bounded radial noise is proved in [Proof 09](proofs/09_robust_ap_and_joins.md). The remaining mass-two blocks below three are centered crosses with at least two endpoint pairs. They are not affine joins of their AP triples, because the center is shared and there are additional cross-pair relations.

## 4  The centered mixed sign problem

After real-sign gauges, its sign vertices have the form

$$
 U=c+\sum_j(a_jZ_j+b_j\overline Z_j),\qquad
 V_s=c+\sum_j(a_jZ_j+s_jb_j\overline Z_j),
$$

where $c,a_j,b_j\geq0$, $s_j\in\{-1,1\}$, and the $Z_j$ are independent uniform circle variables. A pair is balanced if $a_j=b_j$, circular if $a_jb_j=0$, and genuinely unequal if both entries are positive and unequal.

### 4.1  A precise robust comparison

Set $K(z)=|z|^2\log|z|$, continuously extended by zero at the origin. For bounded laws $U,V$ with equal second moments, [Proof 10](proofs/10_radial_green_reduction.md) proves equivalence between comparison for every continuous radial planar bisubharmonic test and

$$
 \mathbb E K(U+\rho Z)\geq\mathbb E K(V+\rho Z)
 \quad\text{for every }\rho\geq0.
$$

The exact circular kernel is

$$
 \mathbb E K(r+\rho Z)
 =(r^2+\rho^2)\log\max(r,\rho)+\min(r^2,\rho^2).
$$

The proof includes the zero-radius atom, the quadratic cancellation, and the necessary caution about separately integrating logarithmic normalizations near zero. The full cone is stable under bounded independent radial noise and contains the power tests for $p\geq2$. Thus it supplies the replacements needed in affine joins. The general mixed-sign all-radii comparison is still unproved.

### 4.2  Unconditional sign families and restricted boxes

All-positive versus all-pairs-flipped comparison holds for all $p\geq2$ with bounded radial noise ([Proof 12](proofs/12_uniform_pair_signs.md)). More strongly, rotating an entire aligned ellipse sum through a common angle gives an expectation nonincreasing from angle zero to $\pi/2$, for the whole radial bisubharmonic cone ([Proof 15](proofs/15_common_rotation.md)). This concerns one common rotation, not separate rotations of different pairs.

Every sign pattern whose genuinely unequal pairs all have the same product sign is positive. Therefore prescribed boxes with at most one genuinely unequal pair satisfy full real majorization for all $p\geq2$, with bounded radial noise. The balanced-group alignment proof is [Proof 24](proofs/24_balanced_flip_alignment.md); the simpler balanced-or-circular argument is [Proof 11](proofs/11_balanced_coefficient_boxes.md).

### 4.3  Strong center bounds for every Green radius

Write

$$
 A_j=a_j+b_j,\quad B_j=|a_j-b_j|,\quad
 \alpha_j=(A_j^2+B_j^2)/2=a_j^2+b_j^2.
$$

[Proof 40](proofs/40_strong_center_green_cone.md) proves the full radial cone, arbitrary bounded radial-noise robustness, and full power boxes for every $p\geq2$ whenever

$$
 c\geq\sum_j(a_j+b_j).
$$

The proof pairs a centrally symmetric disk-background variable $W$ with $-W$ before taking an anisotropic Hessian. If $|W|<c$, the paired Hessian of every circular Green kernel is nonnegative. Exact elliptical-disk differentiation then permits the entire signed-anisotropy interval, including its negative half. The differential identity and aligned-anisotropy input are included in [Proof 28](proofs/28_anisotropic_hessian.md).

A smaller sufficient threshold for a specified flipped group $T$ and complement $U$ is

$$
 c\geq\max\left(
 \sum_{j\in U}A_j+\sum_{j\in T}\sqrt{\alpha_j},
 \sum_{j\in U}\sqrt{\alpha_j}+\sum_{j\in T}A_j\right).
$$

For two noncircular pairs, both mixed vertices are covered by

$$
 c\geq\max(A_1+\sqrt{\alpha_2},A_2+\sqrt{\alpha_1}),
$$

and the other vertices are equality or common-rotation cases. This gives a full box even below the total-support center bound. For example, the pairs $(2,1)$ and $(3/2,1/2)$ with $c=23/5$ satisfy it, although $23/5<5=A_1+A_2$. Circular pairs may be absorbed into the radial noise before applying the bounds.

These conditions are sufficient coefficient restrictions. They do not establish the support theorem for arbitrary center and endpoints.

### 4.4  Other exact and validated coefficient regions

A dominant endpoint has an exact entropy gap and coefficient-dependent power intervals above two. The root-integration formula is [Proof 14](proofs/14_one_phase_entropy.md), the dominant-endpoint theorem is [Proof 17](proofs/17_dominant_endpoint_entropy.md), and its full-box corollary is [Proof 18](proofs/18_near_two_boxes.md). [Proof 27](proofs/27_exterior_barrier.md) gives an exact nonnegative exterior-ellipse remainder and a stability bound beyond root containment. The earlier center-dominant numerical gap constant remains available in [Proof 13](proofs/13_dominant_center_boxes.md).

Two specific genuinely unequal boxes outside the simple dominance regimes are rigorously certified for $2<p\leq2.1079$ and $2<p\leq2.0519$. Their exact bounds and all sign patterns are in [Proof 44](proofs/44_rational_boxes.md). The quadrature error proofs and executable dependencies are [Proofs 42](proofs/42_validated_entropy_quadrature.md) and [43](proofs/43_validated_green_quadrature.md). These computations trust mpmath real interval primitives, a disclosed numerical dependency, and do not assert arbitrary radial-noise robustness or domain-wide positivity from sampled points.

### 4.5  Failures of stronger methods do not settle the target

The scalar multiradius kernel has a negative random/random mixed derivative below three ([Proof 05, Section 5](proofs/05_arithmetic_progressions.md)). The balanced entropy gap can decrease with the center near zero ([Proof 16](proofs/16_center_monotonicity_obstruction.md)). Neither fact is a negative power-majorant witness.

An exact obstruction also prevents independently aligning each conditional ellipse after compressing two pairs. [Proof 41](proofs/41_compression_obstruction.md) gives rational coefficients for which the proposed upper bound exceeds the positive expectation, while the **actual** entropy sign gap is $1/20000>0$. The lost angle is essential. This auxiliary failure must not be reported as a counterexample to the Green or power comparison.

## 5  The remaining configurations between four and six

### 5.1  The complete current support reductions

For $4<p<6$, the first primitive tests permit only masses two or three, or certain odd masses at least five ([Proof 07](proofs/07_tests_between_four_and_six.md)). Theorem A sharpens this to masses **two, three, or five**. At mass five the only possible primitive patterns are

$$
 (5,-3,-2),\qquad(3,2,-3,-2),
$$

up to permutation and sign. These restrictions still do not classify whole configurations.

For collinear triples, only the following supports remain possible after rational-affine normalization and reflection:

$$
 \{0,1,2\},\qquad\{0,1,3\},\qquad\{0,2,5\}.
$$

The AP is positive. The other two are not classified unrestrictedly.

The explicit analytic theorem in [Proof 30](proofs/30_all_odd_triples.md) excludes every $\{0,2,K\}$ with odd $K\geq7$ at each prescribed $4<p<6$. It proves a negative leading coefficient by a positive beta-integral estimate, then bounds the entire holomorphic remainder to produce positive amplitudes $(1,x,y)$ with $x+y<1$. Both $x$ and $y$ may depend on $p$ and $K$. At $p=5$, its separate rational corollary uses

$$
 y=8191/8192,\qquad x=2^{-8K-20}
$$

for every odd $K\geq7$.

[Proof 31](proofs/31_all_high_mass_four_circuits.md) likewise excludes every noncollinear circuit of relation type $(K-2,2,-(K-2),-2)$ for odd $K\geq7$ and each prescribed exponent in the interval. This is proved on a genuine two-dimensional representative, with transfer by its complete affine-relation lattice; it is not inferred by projecting a collinear counterexample. The mass-five member remains unresolved.

On a line, there are at most four points. [Proof 25](proofs/25_four_point_triple_tests.md) shows that the four-point sets passing every necessary triple test have the form

$$
 Q_K=\{0,2,K,K+2\},\qquad K>0\text{ odd}.
$$

Every $Q_K$ with $K\geq5$ contains an excluded odd triple. Hence only $Q_1$ and $Q_3$ remain collinear four-point candidates. This is not a positivity theorem for either quartet.

### 5.2  Fixed witnesses with stronger exponent quantifiers

The all-odd support exclusions permit coefficients to vary with $p$. Separate fixed integer tuples give counterexamples simultaneously for every $4<p<6$:

- $(8,11,10)$ on $\{0,2,7\}$, with the middle sign reversed;
- $(70,90,63)$ on $\{0,2,9\}$, with the middle sign reversed;
- $(90,110,63)$ on $\{0,2,11\}$, with the middle sign reversed;
- $(4,4,5,2)$ on $\{(0,0),(2,0),(0,1),(5,1)\}$, with the second sign reversed.

[Proofs 19](proofs/19_uniform_027.md), [20](proofs/20_uniform_029_0211.md), and [32](proofs/32_uniform_noncollinear_k7.md) supply the convergent-series proofs and exact certificate dependencies. The endpoint zeros at $p=4,6$ are factored symbolically; exact rational-bin inequalities and complete tail bounds cover the entire remaining closed $q$ interval. No interpolation between sampled exponents is used.

There is also a common-coefficient family for every sufficiently large odd frequency. If $n=K-1$, $j_n=\lfloor n/3+1/2\rfloor$, and $c_n=2\cos(\pi j_n/n)$, then $(1,1,c_n)$ works simultaneously throughout $4<p<6$ whenever odd $K\geq10^{1000}+1$. [Proof 23](proofs/23_large_odd_counterexamples.md) gives the Fourier singularity argument; [Proof 33](proofs/33_explicit_uniform_threshold.md) supplies an explicit, deliberately coarse bound. Its moving-zero and all-harmonic estimates are uniform after removing both endpoint factors. This threshold is an auxiliary uniform-witness bound, not a residual support-classification cutoff.

### 5.3  Positive boxes on the two surviving non-AP triples

On $\{0,1,3\}$, write the prescribed bounds as $(A,B,C)$. All three dominant cones are positive for $4<p<6$:

$$
 A\geq B+C,\qquad B\geq A+C,\qquad C\geq A+B.
$$

The proofs are [22](proofs/22_cubic_dominant_constant.md), [34](proofs/34_cubic_middle_cone.md), and [26](proofs/26_cubic_high_cone.md), respectively. Only the corrected accepted middle- and high-frequency proofs are included. Their complete factorial bounds retain the required factors; the middle proof includes its exact finite arithmetic certificate and analytic infinite tail.

The symmetric-extreme boxes $(A,B,A)$ are also positive, including their strict-triangle portion. [Proof 38](proofs/38_cubic_symmetric_slice.md) uses a three-root Chebyshev trace and gives an explicit neighborhood with unequal extremes. With $M=(A+C)/2$, $S=A+B+C>0$, and the falling factorial $(q)_3=q(q-1)(q-2)$, a sufficient neighborhood condition is

$$
 |A-C|\leq\frac{(q)_3M^3B^3}{pS^5}.
$$

On $\{0,2,5\}$, the constant-dominant and frequency-five-dominant cones are positive ([Proof 35](proofs/35_k5_constant_cone.md) and [Proof 21](proofs/21_dominant_odd_bands.md)). The symmetric-extreme boxes $(A,B,A)$ are positive by a five-root trace ([Proof 36](proofs/36_k5_symmetric_slice.md)), with the explicit unequal-extreme neighborhood in [Proof 37](proofs/37_k5_symmetric_neighborhood.md):

$$
 |A-C|\leq\frac{(q)_5M^5B^5}{6pS^9},\qquad
 (q)_5=q(q-1)(q-2)(q-3)(q-4)>0.
$$

These conditions are sufficient, not necessary. The unrestricted cubic strict-triangle region and arbitrary unequal-extreme K5 boxes remain open. The strict-triangle auxiliary third-order convex-order obstruction in [Proof 45](proofs/45_triangle_order_obstruction.md) is not a negative power witness.

### 5.4  A quartet comparison that is deliberately narrower than a box theorem

For odd $K\geq3$ and $4<p<6$, [Proof 39](proofs/39_quartet_double_flip_only.md) proves

$$
 \mathbb E|(a+bz^2)(c+dz^K)|^p
 \geq\mathbb E|(a-bz^2)(c+dz^K)|^p
$$

for nonnegative $a,b,c,d$. On the coefficient surface $(A,B,C,D)=(ac,bc,ad,bd)$, this is the **double-flip comparison only**, from $(A,B,C,D)$ to $(A,-B,C,-D)$. It does not prove either single-flip comparison or a full coefficient box, even on $AD=BC$. In particular, it does not classify $Q_3$.

## 6  Remaining gaps and how to read the proof package

The full problem remains **UNSOLVED**. The precise unresolved scope is:

1. For $2<p<3$, unrestricted centered crosses with genuinely mixed signs and at least two genuinely unequal active pairs outside the proved regions, together with the robust replacements needed for their general affine joins.
2. The unrestricted all-radii Green comparison for those mixed signs. No negative actual-power or Green witness for that target is established here.
3. At noneven $p>4$, a necessary-and-sufficient classification of the finite candidate configurations. A bounded circuit mass and a finite list do not decide each candidate.
4. On $4<p<6$, the unrestricted supports $\{0,1,3\}$ and $\{0,2,5\}$, the candidate collinear quartets $Q_1,Q_3$, and the surviving noncollinear mass-five circuit family, as well as their possible larger configurations.
5. Literature priority. Verified sources establish important analytic precedents, but the bounded comparison does not establish novelty.

The proof chapters are supporting parts of this manuscript, not inaccessible references to work elsewhere. Each chapter states its mathematical scope and links to included prerequisites. Symbols are local to a chapter; for example, $q$ usually denotes $p/2$, while the compression-obstruction chapter explicitly uses a separate aspect-ratio parameter. The [certificate guide](certificates/README.md) distinguishes integer-only proof dependencies from interval-library-dependent numerical certificates. Original sources are preserved, rejected arguments are excluded, and publication or final review acceptance is not inferred from the existence of this reading edition.
