# Proof 23  Uniform counterexamples for sufficiently large odd frequencies

The Fourier argument below proves a uniform-in-p witness for sufficiently large odd frequencies. [Proof 33](33_explicit_uniform_threshold.md) makes its threshold explicit. Separately, [Proof 30](30_all_odd_triples.md) excludes every odd K>=7 at each prescribed p, allowing p-dependent coefficients.

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Proof dependencies included in this package: [Primitive circuit tests between four and six](07_tests_between_four_and_six.md); [A fixed counterexample on zero two seven](19_uniform_027.md); [Fixed counterexamples on zero two nine and zero two eleven](20_uniform_029_0211.md).

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## Result and exact boundary

There is an integer K_0 such that, for every odd K >= K_0, one fixed triple of positive real magnitudes gives a strict reversed majorant inequality for **every** 4 < p < 6. Explicitly, put

- n = K − 1 (so n is even);
- j_n = floor(n/3 + 1/2);
- alpha_n = pi j_n/n;
- c_n = 2 cos(alpha_n).

Then, for every sufficiently large even n and all 4 < p < 6,

    integral_T |1 + z² + c_n z^(n+1)|^p
      < integral_T |1 − z² + c_n z^(n+1)|^p.                (1)

Circle integrals use normalized Haar measure. The same threshold works throughout the open exponent interval, and the coefficients do not depend on p. They satisfy c_n -> 1. The argument in this chapter gives an existential threshold. Proof 33 makes it explicit. This uniform-witness conclusion does not assert the same tuple works for every odd K>=13. The distinct fixed-p theorem in Proof 30 excludes every odd K>=7 using p-dependent coefficients.

The key point is a phase-aligned, two-dimensional Fourier singularity estimate. It is uniform over *all* harmonics entering the circle restriction. It is not an inference from a fixed-harmonic limit or from a numerical sample.

## 1. Two-dimensional Fourier convention and a local lemma

For a 2pi-periodic function H(theta,u), set

    Hhat(k,m) = (2pi)^(-2) integral integral
                H(theta,u) exp(−i(k theta + m u)) dtheta du.

For the Euclidean Fourier transform use

    F[f](xi) = integral_R² f(y) exp(−i xi·y) dy.

For complex p with Re p > −2, the homogeneous function |y|^p is a tempered distribution. Away from xi=0 its transform is

    F[|y|^p](xi) = C(p) |xi|^(−p−2),
    C(p) = 2^(p+2) pi Gamma(1+p/2) / Gamma(−p/2).          (2)

One elementary derivation first takes −2 < Re p < 0, represents |y|^p by a Gamma-weighted integral of exp(−t|y|²), transforms the Gaussian, and substitutes t -> |xi|²/(4t). This gives (2) with the stated transform convention. Both sides, restricted away from xi=0, continue holomorphically throughout Re p > −2. At nonnegative even p the left-hand transform is supported at zero and C(p)=0, consistently with this identity away from zero.

Here is the local estimate needed below. Suppose a smooth real map F from the flat two-torus, in the coordinates and normalized Lebesgue measure specified above, to R² has finitely many simple zeros x_a. Write J_a = DF(x_a), assumed invertible. In a smooth family in which these zeros remain separated, the inverse Jacobians remain bounded, and a fixed finite number of derivatives remain bounded, the Fourier coefficients of |F|^p have the expansion

    Hhat(xi) = (2pi)^(-2) C(p)
       sum_a exp(−i xi·x_a) / |det J_a|
             |J_a^(−T) xi|^(−p−2) + E(p,xi),             (3)

with

    |E(p,xi)| <= B |xi|^(−Re p−3),   |xi| >= 1,           (4)

uniformly when p ranges over any fixed compact subset of Re p > −2 for which the argument below is applied (we use only 7/2 <= Re p <= 13/2 and |Im p| <= 1/2). The error is holomorphic in p on the interior of such a region.

For completeness, the error estimate is elementary. In a chart y centered at one zero,

    F(x_a+y) = J_a y + O(|y|²),

and invertibility gives |F(x_a+y)| comparable to |y|. With a cutoff supported in that chart,

    R_p(y) = |F(x_a+y)|^p − |J_a y|^p

satisfies, for every required multi-index beta,

    |partial^beta R_p(y)| <= B_beta |y|^(Re p+1−|beta|).   (5)

This follows by factoring |J_a y|² out of |F|² and differentiating
|J_a y|^p [(1+O(|y|))^(p/2) − 1]. All constants are uniform on the indicated compact parameter sets.

Take a smooth dyadic annular partition with annulus radius r. The L1 bound of the cut-off remainder on that annulus is O(r^(Re p+3)); after M integrations by parts it is
O(|xi|^(−M) r^(Re p+3−M)). Sum the first bound over r <= |xi|^(−1), and the second over r >= |xi|^(−1), choosing an integer M > 19/2. Both sums are O(|xi|^(−Re p−3)), uniformly on the indicated p rectangle. This proves the remainder part of (4). There are no boundary terms because each annular piece is compactly supported and smooth.

For the cut-off linear model, (2) and a linear change of variables give the leading term in (3). Replacing the cutoff model by the whole homogeneous distribution introduces a rapidly decreasing error away from zero: arbitrarily high derivatives of (1−cutoff)|J_a y|^p are integrable when the derivative order exceeds Re p+2, so their Fourier transforms are bounded and give arbitrary inverse powers of |xi|. The complement of the zero charts is smooth and has the same rapid decay. This proves (3)–(4), including uniformity. Holomorphy follows by differentiation in p under the locally integrable integrals, or by the same locally uniform dyadic bounds.

This proof also gives O(|xi|^(−p−2)) decay for the complete Fourier coefficient at each real p > 0 in our range. Hence the two-dimensional Fourier series is absolutely and uniformly convergent there.

## 2. Application to the moving-zero family

Let c range over a fixed compact interval for which alpha = arccos(c/2) stays in [pi/4, 5pi/12]. This includes every alpha_n for even n >= 6. Put

    s = 2 sin alpha,
    H_(p,c)(theta,u) = |2 cos theta + c exp(iu)|^p.

The real map whose modulus occurs here is

    F_c(theta,u) = (2 cos theta + c cos u, c sin u).

Its only four zeros on the torus are

    (alpha,pi), (−alpha,pi), (pi+alpha,0), (pi−alpha,0).

They remain uniformly separated. Each Jacobian is diagonal up to signs, with absolute diagonal entries s and c. Thus all determinants have absolute value sc, and every transformed frequency has norm

    R_c(k,m) = sqrt((k/s)² + (m/c)²).

The local lemma gives

    Hhat_(p,c)(k,m)
      = C(p)/(2pi)² * [2((-1)^m + (-1)^k) cos(k alpha)]
          /(sc) * R_c(k,m)^(−p−2) + E_(p,c)(k,m),        (6)

where the error satisfies (4), uniformly in the entire stated c interval and in p in the stated complex rectangle. This checks moving-zero locations, all four phases, and the Jacobian factors explicitly.

## 3. Uniformly removing the endpoint zeros

For real p=4 or p=6, H_(p,c) is a trigonometric polynomial. Indeed

    H_(2q,c) = (4 cos² theta + c² + 4c cos theta cos u)^q

for q=2,3. Its theta degree is at most 4 or 6 respectively. Consequently, for every |k| > 6,

    Hhat_(4,c)(k,m) = Hhat_(6,c)(k,m) = 0.

The leading term in (6) also vanishes at both exponents because C(4)=C(6)=0. Therefore, for |k| > 6,

    E_(4,c)(k,m) = E_(6,c)(k,m) = 0.                      (7)

This exact zero is essential: an error bound not vanishing at the endpoints would not prove a full-interval statement.

Let R = sqrt(k²+m²) >= 1. Bounds (4), holomorphy and Cauchy's estimate on circles of radius 1/8 yield the following refinement, uniformly for real 4 <= p <= 6 and |k| > 6:

    |E_(p,c)(k,m)| <= B_1 (p−4)(6−p) R^(−p−5/2).        (8)

Here are explicit details of the harmless half-power loss. If 4 <= p <= 17/4, write E(p) = integral_4^p E'(t) dt. Cauchy's formula and (4) give

    |E'(t)| <= B_2 R^(−t−3+1/8).

For 4 <= t <= p <= 17/4, this is at most
B_2 R^(−p−3+3/8). Thus |E(p)| <= B_2 (p−4) R^(−p−21/8), which implies (8), since 6−p >= 7/4 and R >= 1. If 23/4 <= p <= 6, integrate from p to 6; now t >= p and the same Cauchy bound gives
|E(p)| <= B_2 (6−p) R^(−p−23/8), again implying (8). On the middle interval [17/4,23/4], the product (p−4)(6−p) is bounded below by 7/16, so (4) implies (8) directly. The Cauchy circles lie in the compact complex rectangle used in Sections 1–2. At the endpoints themselves (8) holds by (7).

For 4 < p < 6, C(p) is strictly negative. Moreover

    b(p) = −C(p)/[(p−4)(6−p)]

extends continuously and strictly positively to [4,6]. This follows either from the simple poles of Gamma(−p/2), or from the recurrence for Gamma. In particular b(p) has a positive minimum and finite maximum on that closed interval.

## 4. Restriction to the circle and exact sign reduction

Let n >= 6 be even. Define

    I_phi(p,c,n) = integral_T H_(p,c)(theta, n theta+phi).

Absolute uniform convergence of the Fourier series justifies termwise restriction and integration:

    I_phi = sum_(m in Z) Hhat_(p,c)(−mn,m) exp(im phi).    (9)

The kernel is even in theta and in u, so its Fourier coefficients are real and separately even in k and m. Also

    H(theta+pi,u+pi) = H(theta,u),

so Hhat(k,m)=0 whenever k+m is odd. Because n is even, the modes in (9) with odd m vanish.

For z=exp(i theta),

    |1+z²+c z^(n+1)| = |2 cos theta+c exp(in theta)|,

and shifting theta by pi/2 in the expression with −z², then multiplying by i, gives

    integral_T |1−z²+c z^(n+1)|^p = I_(pi/2)(p,c,n).

The shift actually produces the phase +pi/2 or −pi/2 according to n modulo four; these give the same integral because only even m survive (equivalently by conjugation). Thus the plus-minus difference is exactly

    D_p(c,n) = I_0 − I_(pi/2)
             = 4 sum_(m>=1, m==2 mod 4) Hhat_(p,c)(mn,m). (10)

Now choose alpha=alpha_n, c=c_n. Then n alpha=pi j_n. Every m in (10) is even, so k=mn is even and

    cos(k alpha) = cos(m pi j_n) = 1.

All four zero phases in (6) are therefore +1. Formula (6) becomes

    Hhat_(p,c_n)(mn,m)
       = C(p)/(pi² s_n c_n)
           m^(−p−2) (n²/s_n²+1/c_n²)^(−(p+2)/2)
         + E_(p,c_n)(mn,m).                             (11)

The leading term is negative. Since s_n and c_n range over fixed positive compact intervals, there is a constant A>0, independent of p in (4,6), n, and m, such that its absolute value is at least

    A (p−4)(6−p) (mn)^(−p−2).

Bound (8) gives

    |E_(p,c_n)(mn,m)|
      <= B_3 (p−4)(6−p) (mn)^(−p−5/2).

Consequently the ratio of error to leading magnitude is at most

    (B_3/A) (mn)^(−1/2).

For all sufficiently large even n, this ratio is less than 1/2 **simultaneously for every surviving m >= 2 and every 4 < p < 6**. Every summand in (10) is then strictly negative. The series is absolutely convergent, and at least its m=2 term is strictly negative. Hence D_p(c_n,n)<0, proving (1).

This is an all-harmonic estimate, stronger than what is needed merely to justify summing a limit. It handles the moving zeros and the open endpoints uniformly.

## 5. Asymptotic value and a transparent p=5 check

Summing (11) with the uniform error gives

    D_p(c_n,n)
      = [4 C(p)/(pi² s_n c_n)]
          (n²/s_n²+1/c_n²)^(−(p+2)/2) S(p)
        + O((p−4)(6−p) n^(−p−5/2)),                    (12)

uniformly for 4 <= p <= 6 after interpreting the endpoint-normalized statement continuously, where

    S(p) = sum_(m>=1,m==2 mod 4) m^(−p−2)
         = 2^(−p−2) (1−2^(−p−2)) zeta(p+2).

Since c_n -> 1 and s_n -> sqrt(3), for every fixed 4 < p < 6,

    lim_(even n->infinity) n^(p+2) D_p(c_n,n)
      = [4 * 3^((p+1)/2)/pi]
          [Gamma(1+p/2)/Gamma(−p/2)]
          (1−2^(−p−2)) zeta(p+2) < 0.                   (13)

The normalized convergence after division by (p−4)(6−p) is uniform on [4,6]. At p=5 this becomes

    lim n^7 D_5(c_n,n)
       = −(6075/(16 pi)) (127/128) zeta(7) < 0,

approximately −120.9153. This p=5 formula is a consequence of the proof, not the source of the sign certification.

## 6. Relation to the final support reduction

The argument proves a single coefficient tuple, depending on K but not p, for each sufficiently large odd K. [Proof 33](33_explicit_uniform_threshold.md) gives the explicit sufficient threshold K>=10^1000+1. The different theorem in [Proof 30](30_all_odd_triples.md) excludes every odd K>=7 for every prescribed 4<p<6 with p-dependent coefficients. The unrestricted supports {0,1,3} and {0,2,5} remain unclassified.
