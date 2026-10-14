# Proof 32  A fixed noncollinear four point counterexample throughout the interval

Included supporting and related chapters: [Every surviving odd four circuit of mass at least seven fails](31_all_high_mass_four_circuits.md).

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

## Result

Let

$$
\Gamma=\{(0,0),(2,0),(0,1),(5,1)\}\subset\mathbb Z^2,
\qquad P_+(z,w)=4+4z^2+w(5+2z^5),
\qquad P_-(z,w)=4-4z^2+w(5+2z^5).
$$

For every **4<p<6**, with normalized Haar measure on the two-torus,

$$
D(p):=\int_{\mathbb T^2}|P_+|^p-\int_{\mathbb T^2}|P_-|^p<0.
$$

Consequently this configuration fails the real strict majorant property at every exponent in that open interval. These are the same positive magnitudes (4,4,5,2) for every exponent; this is a full-support counterexample with an allowed real sign change.

At p=5 the separate direct exact-rational certificate gives

$$
D(5)<-\frac14.
$$

More quantitatively, putting q=p/2, the uniform certificate establishes

$$
D(2q)<-\frac{225^q q(q-1)(q-2)(3-q)}{40\,000\,000}
\qquad(2<q<3).
$$

The finite certificate is [certify_four_circuit.py](../certificates/certify_four_circuit.py), with exact output [certify_four_circuit.json](../certificates/certify_four_circuit.json). All acceptance comparisons use integers or Python Fraction arithmetic. Floating-point numbers are display only.

## 1. Geometry and the tests this example survives

In the displayed point order, the primitive affine relation is

$$
\lambda=(5,-5,-2,2).
$$

Its entries sum to zero, its weighted frequency sum is zero, its gcd is one, and its mass is 7. Its pattern is (K-2,2,-(K-2),-2), up to permutation, with K=7.

Every three-point subset is affinely independent: the absolute determinants of the four triangles are 2,2,5,5. Thus the four points form a minimal affine circuit of affine dimension two. In particular the counterexample does not come from any failing triple subset, and does not use a degenerate projection of a collinear example.

For q in (2,3), the necessary dominant-vertex circuit tests from Proof 01 are products of binomial coefficients with index pairs (7,2) or (7,5). All factors are strictly positive. Therefore these tests pass at every vertex throughout the same exponent interval, although the majorant property fails.

The credited local analytic input for those necessary tests is Gressman–Guo–Pierce–Roos–Yung, *On the strict majorant property in arbitrary dimensions*, Q. J. Math. 74 (2023), 139–161, Proposition 4.1; arXiv v2 Proposition 10. Public sources: https://doi.org/10.1093/qmath/haac021 and https://arxiv.org/abs/2106.12538v2. The counterexample certificate below is a separate direct computation of the entire norm-power difference, not an inference from a higher relation term.

The result transfers to **every primitive affine four-circuit with relation pattern (5,2,−5,−2)**. Label such a circuit so that its primitive relation is (5,−5,−2,2), and insert an independent common unit phase into its four characters. Their joint Haar pushforward is the compact subgroup of the four-torus whose annihilator is exactly the affine relation lattice Z·(5,−5,−2,2). The representative above has the same annihilator, so the pushforward measures agree (their Fourier coefficients are the same). The inserted common phase does not change the absolute value of the polynomial. Thus the entire coefficient-dependent norm function, and in particular the displayed witness, agrees for all circuits in this relation class. This is the affine-lattice transfer used in Proof 01, not projection to a lower-dimensional frequency set.

For general odd m, the sign gauge in the representative polynomial a+bz²+w(c+dz^m) has exactly two possible classes when all magnitudes are nonzero. A global sign, w→−w, and z→−z can normalize the signs of a,c,d. These operations leave the sign product of a and b invariant, and the residual b sign distinguishes the two classes. Hence the present choice b=−4 is the relevant nongauge sign class.

## 2. Exact even moments in one-dimensional arrays

Write

$$
S_\pm=|P_\pm|^2,\qquad
R_k^\pm=\int_{\mathbb T^2}S_\pm^k.
$$

Condition on z and integrate w first. For any complex f,g,

$$
\int_{\mathbb T}|f+wg|^{2k}\,dw
=\sum_{j=0}^k\binom{k}{j}^2 |f|^{2j}|g|^{2(k-j)}.
$$

Here the two first-pair squared radii are 32±16(z²+z⁻²), and the second-pair squared radius is 29+10(z⁵+z⁻⁵).

Define the nonnegative integer array

$$
T_{h,r}=[u^r](29+10u+10u^{-1})^h,
\quad T_{h,-r}=T_{h,r},\quad T_{h,r}=0\ (|r|>h).
$$

It is obtained using the exact recurrence

$$
T_{0,0}=1,\qquad
T_{h,r}=29T_{h-1,r}+10T_{h-1,r-1}+10T_{h-1,r+1}.
$$

Also

$$
[z^{2r}]|4\pm4z^2|^{2j}
=16^j(\pm1)^r\binom{2j}{j+r}.
$$

The constant-coefficient resonance is 2r+5s=0, hence r=5ℓ and s=−2ℓ. Therefore

$$
R_k^\pm=\sum_{j=0}^k\binom{k}{j}^2 16^j
\left[\binom{2j}{j}T_{k-j,0}
+2\sum_{\ell=1}^{\min(\lfloor j/5\rfloor,\lfloor(k-j)/2\rfloor)}
(\pm1)^\ell\binom{2j}{j+5\ell}T_{k-j,2\ell}\right].
$$

This is the implemented integer formula. It implies R_k^+=R_k^- for k<7. The first moment difference is checked explicitly:

$$
R_7^+-R_7^-
=4\binom75^2 4^{10}5^2 2^2
=184\,968\,806\,400.
$$

The squared binomial coefficient matters: both sides of the circuit have the partition 5+2.

## 3. Complementary moments and the convergent series

Triangle inequality gives 0≤S_±≤15²=225. Set

$$
U_\pm=1-S_\pm/225\in[0,1],\quad
V_j^\pm=\int(225-S_\pm)^j
=\sum_{k=0}^j(-1)^k\binom jk225^{j-k}R_k^\pm.
$$

Every V_j^± is an integer. The implementation also checks

$$
0\le V_j^\pm\le225^j,\qquad V_j^\pm\le225V_{j-1}^\pm.
$$

Put δ_j=(V_j^+−V_j^-)/225^j. In particular δ_j=0 for j<7. For fixed q∈(2,3), the binomial series is absolutely and uniformly convergent on [0,1], so

$$
D(2q)=225^q\sum_{j\ge0}(-1)^j\binom qj\delta_j.
$$

For j≥4 factor

$$
(-1)^j\binom qj=-F(q)w_j(q),\qquad
F(q)=q(q-1)(q-2)(3-q)>0,
$$

where

$$
w_4(q)=\frac1{24},\qquad
w_{j+1}(q)=\frac{j-q}{j+1}w_j(q).
$$

Since δ_0,…,δ_3 vanish,

$$
D(2q)=-225^qF(q)B(q),\qquad B(q)=\sum_{j\ge4}w_j(q)\delta_j.
$$

The weights extend positively to q∈[2,3]; each is nonincreasing in q. The exact tail identity is

$$
\sum_{j>N}w_j(q)=\frac{N+1}{q}w_{N+1}(q),\qquad N\ge4.
$$

Indeed, with t_j=jw_j/q, the recurrence gives t_j−t_{j+1}=w_j, and t_j→0. For example, at q=2, w_j=1/[j(j−1)(j−2)]; at q=3, w_j=1/[j(j−1)(j−2)(j−3)]. These endpoint formulas also show convergence of the extended series. The tail identity and nonincreasing U powers yield

$$
\left|\sum_{j>N}w_j(q)\delta_j\right|
\le\frac{N+1}{q}w_{N+1}(q)
\frac{V_{N+1}^++V_{N+1}^-}{225^{N+1}}.
$$

## 4. Uniform interval certificate

Take N=128 and partition [2,3] into 256 closed intervals [a,b], where a=2+i/256 and b=a+1/256. On one such interval,

$$
B(q)\ge
\sum_{j=4}^{128}
\begin{cases}
w_j(b)\delta_j,&\delta_j\ge0,\\
w_j(a)\delta_j,&\delta_j<0
\end{cases}
-
\frac{129}{a}w_{129}(a)
\frac{V_{129}^++V_{129}^-}{225^{129}}.
$$

The endpoints and all weights in this lower bound are rational. The program evaluates every finite summand rounded downward to the 10⁻⁷⁰ grid, and the nonnegative tail rounded upward to that grid. Thus the resulting integer divided by 10⁷⁰ is a rigorous lower bound, with rounding in the unfavorable direction.

Every one of the 256 lower numerators is included in the JSON output. Their minimum is exactly

    299637640743992924436494782528032779689900625653861815274742541

on the common denominator 10⁷⁰. This is approximately 2.996376407439929×10⁻⁸, and the exact integer comparison verifies that it exceeds 1/40,000,000. The smallest lower bound occurs on the final interval [767/256,3]. This proves B(q)>1/40,000,000 on [2,3], and the stated strictly negative difference for 2<q<3.

There is no strict failure asserted at p=4 or p=6: F(q)=0 at those endpoints, and in fact the corresponding low even moments agree.

## 5. Separate p=5 check

Without the interval factorization, truncate the direct q=5/2 binomial series at N=128. Its exact rational partial sum is approximately −0.4078851009432079. The rigorous tail estimate is

$$
15^5\left|\binom{3/2}{128}\right|
\frac{V_{129}^++V_{129}^-}{225^{129}},
$$

approximately 0.07468607111428409. Hence the exact rational upper bound is approximately −0.33319902982892385, and an exact comparison proves it is less than −1/4. The true numerical integral is approximately −0.42086823, but that numerical value is not needed for acceptance.

## 6. Scope and remaining obstruction

This resolves the entire mass-7 relation class of the surviving noncollinear four-circuit family negatively, uniformly over the entire exponent gap. All its proper subsets are affinely independent, and hence have the known majorant property at every positive exponent. The example therefore shows that checking proper subsets and every primitive dominant-vertex leading test is insufficient even in affine dimension two.

The companion analytic note [Every surviving odd four circuit of mass at least seven fails](31_all_high_mass_four_circuits.md) proves failure for every odd K≥7 and every prescribed 4<p<6, with coefficients allowed to depend on p and K. The fixed coefficient tuple in the present note is a stronger uniform-witness statement for K=7. No all-amplitude classification is proved for K=5. The broad fixed-exponent classification remains open in this work.


## Reproduction

Run from any directory, with Python 3 and its standard library:

From the package root, using an ordinary nonoptimized Python interpreter:

    python certificates/certify_four_circuit.py

The default N=128, 256-bin invocation writes the exact JSON output. The p=5 upper bound is approximately −0.333199, and the uniform lower bound approximately 2.9963764×10⁻⁸; these displays are not acceptance predicates. The independent source audit reconstructed the moments by bivariate polynomial powers and Parseval. Reproduction requirements are in the [certificate guide](../certificates/README.md).
