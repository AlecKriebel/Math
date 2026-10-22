# Proof 33  An explicit threshold for the uniform large odd witness

Included dependencies: [Uniform counterexamples for sufficiently large odd frequencies](23_large_odd_counterexamples.md); [Every odd collinear triple with frequency at least seven fails](30_all_odd_triples.md).

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

## Result and limitations

Put

    N = 10^1000,       K_0 = N + 1.

For every odd integer K >= K_0, let

    n = K - 1,
    j_n = floor(n/3 + 1/2),
    c_n = 2 cos(pi j_n/n).

Then, simultaneously for every real 4 < p < 6,

    integral_T |1 + z^2 + c_n z^(n+1)|^p
      < integral_T |1 - z^2 + c_n z^(n+1)|^p.           (1)

The integrals use normalized Haar measure. The coefficient triple is independent of p. In particular, the equal-coefficient conclusion holds for every K congruent to 1 modulo 6 with K >= K_0.

The threshold is intentionally extremely coarse. It makes the uniform-in-p witness effective with completely specified constants. It is not the boundary of the support classification: [Proof 30](30_all_odd_triples.md) already excludes every odd K>=7 at each prescribed p, using coefficients that may depend on p. No unrestricted positive classification of {0,1,3} or {0,2,5} follows.

## 1. Inputs and Fourier convention

The underlying Fourier singularity expansion, its normalization, and its distributional justification are included in [Proof 23](23_large_odd_counterexamples.md).

The present proof keeps its Fourier normalization:

    Hhat(k,m) = (2pi)^(-2) integral_T^2
                  H(theta,u) exp(-i(k theta + m u)) dtheta du.

The unnormalized Euclidean Fourier transform of |y|^p, away from frequency zero, is

    C(p) |xi|^(-p-2),
    C(p) = 2^(p+2) pi Gamma(1+p/2) / Gamma(-p/2).         (3)

The Gaussian-integral derivation and holomorphic distributional continuation in Proof 23 apply without change. All new estimates below are explicit and use only elementary differentiation, integration by parts, and Cauchy's estimate.

For the quantitative work, allow the slightly larger real parameter interval

    1/2 <= c <= 3/2,
    alpha = arccos(c/2),   s = sqrt(4-c^2).

Thus 1 <= s <= 2. Define

    F_c(theta,u) = (2 cos(theta) + c cos(u), c sin(u)),
    H_(p,c) = |F_c|^p,
    7/2 <= Re p <= 13/2,    |Im p| <= 1/2.              (4)

Complex powers use the real logarithm at positive real squared norms; at the zeros they are defined by continuous extension, since Re p > 0.

## 2. An explicit cutoff

Let

    A = 25!/(12!)^2,
    P(t) = A integral_t^1 v^12 (1-v)^12 dv,  0 <= t <= 1.

Extend P by 1 on t <= 0 and by 0 on t >= 1. This is a C^12 function. Its derivatives of orders 1 through 12 vanish at both joining points. For r > 0 put

    chi_r(y) = P((|y|^2/r^2 - 1)/3).

It equals 1 for |y| <= r and 0 for |y| >= 2r. For either coordinate derivative and 0 <= h <= 12,

    |partial_j^h chi_r(y)| <= 10^70 r^(-h).             (5)

Here is an elementary verification with ample slack. The sum of the absolute coefficients of the polynomial P on [0,1] is less than 2^42: A < 2^29, and the unnormalized integrand has coefficient sum 2^12. Since its degree is 25,

    sup_[0,1] |P^(h)| <= 2^42 25^h < 10^32,
       0 <= h <= 12.

On the transition annulus the inner quadratic t has |partial_j t| <= 2/r and |partial_j^2 t| <= 1/r^2, with higher derivatives zero. The one-variable chain rule gives

    partial_j^h P(t) = h! sum_(ell=0)^floor(h/2)
        P^(h-ell)(t) (partial_j t)^(h-2ell)
        (partial_j^2 t/2)^ell / ((h-2ell)! ell!).

Bounding the number of terms by 13 gives a bound less than 10^46 r^(-h), and hence (5). Outside the annulus the same assertion follows from constancy and the C^12 matching. Only these first 12 derivatives will be used.

Fix from now on

    r_0 = 10^(-3).

## 3. Uniform zero charts and local derivative bounds

The four zeros of F_c are

    (alpha,pi), (-alpha,pi), (pi+alpha,0), (pi-alpha,0).

They have pairwise torus distance greater than 1: zeros with different u coordinates are separated by pi, while the separation of zeros with the same u coordinate is at least 2 arccos(3/4) > pi/3 > 1. Thus their radius-2r_0 coordinate disks are disjoint. The Jacobian J at any zero is diagonal up to signs, with absolute entries s and c. In particular

    (1/2)|y| <= |Jy| <= 2|y|.

For p in (4), real y with 0 < |y| <= 2r_0, and either coordinate j, define

    Q_0(y) = |Jy|^2,
    R_p(y) = |F_c(x_a+y)|^p - |Jy|^p.

The following explicit bounds hold for 0 <= h <= 12:

    |partial_j^h R_p(y)| <= 10^70 |y|^(Re p+1-h),       (6)
    |partial_j^h |Jy|^p| <= 10^70 |y|^(Re p-h).         (7)

The second bound holds for every real y != 0, without the radius restriction.

To verify these estimates, write r = |y| and vary one coordinate of y through the complex disk |z_j-y_j| <= r/10^4, leaving the other coordinate real. The holomorphic quadratic Q_0(z) means (Jz)_1^2+(Jz)_2^2, not the squared modulus of a complex vector. The inequalities

    |Q_0(z)-Q_0(y)| < .001 r^2,
    .24 r^2 <= |Q_0(z)| <= 5 r^2,
    |arg Q_0(z)| < .01

follow from ||J|| <= 2, |Jy| >= r/2, and |z-y| <= r/10^4.

At a zero x_a, Taylor's formula for sine and cosine gives

    |F_c(x_a+z) - Jz| <= 3 |z|^2

whenever |z| <= .002001. For example, the cosine remainders in the first coordinate are bounded by 2|z_1|^2+(3/2)|z_2|^2, and the sine remainder in the second coordinate is at most (1/2)|z_2|^3; their Euclidean combination is less than 3|z|^2. Consequently, with Q(z) = F_1(x_a+z)^2+F_2(x_a+z)^2,

    |Q(z)-Q_0(z)| <= 13 |z|^3,
    |Q(z)/Q_0(z)-1| <= 60 r <= .12.                    (8)

The principal branches of both powers are therefore holomorphic throughout this disk and agree with the real powers on its real segment. Writing a = Re p, (4) gives

    |Q_0(z)^(p/2)| <= 200 r^a,
    |(1+v)^(p/2)-1| <= 500 r
       when v = Q(z)/Q_0(z)-1.

For the second estimate, integrate (p/2)(1+tv)^(p/2-1) from t=0 to 1; |p/2| < 4, |v| <= 60r, and the remaining factor is less than 2. Thus the holomorphic local remainder is bounded by 10^5 r^(a+1). Cauchy's estimate gives

    |partial_j^h R_p(y)|
       <= 10^5 h! 10^(4h) r^(a+1-h) < 10^70 r^(a+1-h).

Applying the same estimate to Q_0^(p/2) proves (7), including all radii by homogeneity. This proves (6)-(7) with explicit constants uniformly in the whole complex p rectangle and in c.

## 4. Quantitative Fourier error

For xi = (k,m), R = |xi| >= 1, we claim

    Hhat_(p,c)(k,m)
      = C(p)/(2pi)^2 sum_a exp(-i xi dot x_a)
          |det J_a|^(-1) |J_a^(-T) xi|^(-p-2)
        + E_(p,c)(k,m),

    |E_(p,c)(k,m)| <= 10^400 R^(-Re p-3).               (9)

This is the point at which a previously unspecified constant is made explicit. The following three estimates account for every part of the error.

### 4.1. Local nonlinear remainder

Put r_l = r_0 2^(-l) and

    b_l = chi_(r_l) - chi_(r_l/2),  l = 0,1,2,... .

Then chi_(r_0) R_p = sum_l b_l R_p in L^1. The lth term is supported where r_l/2 <= |y| <= 2r_l. From (5),

    |partial_j^h b_l| <= 10^75 r_l^(-h),  h <= 12.

Combining this with (6), the ordinary product rule, and

    2^|a+1-h| < 10^3   (7/2 <= a <= 13/2, h <= 12),

gives the deliberately loose bound

    |partial_j^h (b_l R_p)| <= 10^160 r_l^(a+1-h).

The support has area at most 16r_l^2. Choose the coordinate j for which |xi_j| >= R/sqrt(2). The L^1 estimate and twelve integrations by parts therefore give

    |F[b_l R_p](xi)|
       <= 10^164 min(r_l^(a+3), R^(-12) r_l^(a-9)).

Writing b = a+3 in [13/2,19/2], split the dyadic sum at r_l = 1/R. The two geometric sums are bounded by

    sum_(r_l<=1/R) r_l^b <= 2 R^(-b),
    sum_(r_l>1/R) R^(-12) r_l^(b-12) <= 2 R^(-b).

These also hold when either subcollection is empty. Hence the error from each local remainder is less than 10^165 R^(-a-3). There are four charts. The C^12 matching of the cutoff eliminates boundary terms in all twelve integrations by parts.

### 4.2. Replacing the cut-off linear model by the homogeneous distribution

The difference is the Fourier transform of

    T_p(y) = (1-chi_(r_0)(y)) |Jy|^p.

Its twelfth coordinate derivative is integrable. Outside radius 2r_0, use (7). On the transition annulus use (5), (7), and the product rule. More explicitly, the outside contribution to its L^1 norm is at most

    2pi 10^70 r_0^(a-10)/(10-a) < 10^92.

For each product-rule term on the annulus, replace powers of |y|/r_0 by at most 2^9 < 10^3; then the sum of terms is bounded pointwise by

    10^147 r_0^(a-12).

Multiplication by the area, at most 16r_0^2, gives less than 10^169, since r_0^(a-10) <= 10^19.5. In particular

    ||partial_j^12 T_p||_1 <= 10^180.

As a tempered distribution, off the hyperplane xi_j = 0 its Fourier transform is the Fourier transform of this integrable derivative divided by (i xi_j)^12. The chosen coordinate therefore gives

    |F[T_p](xi)| <= 10^182 R^(-12)
                   <= 10^182 R^(-a-3).

This argument uses no unproved integrability of T_p itself. It justifies comparison with (3), including complex p and every frequency direction. There are four such tails.

### 4.3. The complement of the zero charts

Set

    G = (1-sum_a chi_(r_0)(x-x_a)) H_(p,c)(x).

Outside the four radius-r_0 disks,

    |F_c(x)| >= r_0/100 = 10^(-5).                      (10)

Here is a quantitative proof. If |F_c| < epsilon = r_0/100, the distance delta_u from u to the nearer member of {0,pi} satisfies delta_u <= pi epsilon < 4epsilon, because c >= 1/2 and |sin u| >= 2delta_u/pi. Replacing cos u by that endpoint's cosine changes the real component by at most (3/4)delta_u^2. Hence |2 cos(theta) +/- c| < 2epsilon. On reducing theta by reflection to [0,pi], its corresponding root beta lies in [pi/6,5pi/6]. The identity

    |2 cos(theta)-2 cos(beta)|
      = 4 sin((theta+beta)/2) |sin((theta-beta)/2)|
      >= |theta-beta|/pi > |theta-beta|/4

uses sin(pi/12) > 1/4. Thus delta_theta < 8epsilon and the distance to one of the four zeros is less than 12epsilon < r_0. This proves (10) by contraposition.

For a point obeying (10), the real quantity

    Q(theta,u) = 4 cos^2(theta)+c^2+4c cos(theta) cos(u)

lies in [10^(-10),12.25]. If one coordinate is moved into a complex disk of radius rho = 10^(-14), its derivative along that disk has magnitude less than 100. Therefore |Q(z)-Q(x)| <= 10^(-12) <= Q(x)/100. The principal power Q(z)^(p/2) is holomorphic there and is bounded by 10^6: |Q(z)| < 13, |arg Q(z)| < .02, and p is in (4). Cauchy's estimate consequently gives, for every 0 <= h <= 12,

    |partial_j^h H_(p,c)(x)|
       <= 10^6 h! rho^(-h) < 10^183.

The cutoff factor and all its first 12 coordinate derivatives are bounded by 10^107, by (5) and r_0 = 10^(-3). The product rule yields

    |partial_j^12 G| < 10^294.

Within the inner zero disks G is identically zero, and its derivatives extend across their boundaries by C^12 matching. Its L^1 derivative norm is less than 10^296, because the torus area is less than 64. Twelve periodic integrations by parts now give

    |integral_T^2 G exp(-i xi dot x)| < 10^298 R^(-12)
                                      <= 10^298 R^(-a-3).

### 4.4. Combining the bounds

The normalization (2pi)^(-2) is less than 1. The sums of the four local errors, the four linear tails, and the global complement are bounded by

    (4*10^165 + 4*10^182 + 10^298) R^(-a-3)
        < 10^400 R^(-a-3).

This proves (9). Every constant has been obtained from the displayed cutoff, radius, parameter ranges, and derivative estimates; no unspecified constant is absorbed into 10^400. Holomorphy in p follows from the locally integrable original coefficients and (3), or from the uniform dyadic estimates above.

## 5. Explicit endpoint factorization

The four Jacobians all have determinant magnitude sc and the same transformed frequency length

    R_c(k,m) = sqrt((k/s)^2+(m/c)^2).

The four phases sum to 2[(-1)^m+(-1)^k]cos(k alpha). Thus (9) is the explicit-constant version of the accepted expansion

    Hhat_(p,c)(k,m)
      = C(p)/(2pi)^2 * 2[(-1)^m+(-1)^k]cos(k alpha)
          /(sc) * R_c(k,m)^(-p-2) + E_(p,c)(k,m).       (11)

When p is 4 or 6, H is a trigonometric polynomial of theta degree at most 6. Its coefficient vanishes when |k| > 6. Since C(4)=C(6)=0, E has exact zeros at both these exponents for such frequencies.

Apply Cauchy's estimate on p-disks of radius 1/8. They lie inside the rectangle (4). With B = 10^400, (9) gives, for 4 <= t <= 6,

    |E'(t)| <= 8B R^(-t-3+1/8).

For 4 <= p <= 17/4, integrate from 4 to p, obtaining

    |E(p)| <= 8B(p-4) R^(-p-21/8).

Since 6-p >= 7/4, this is bounded by 8B(p-4)(6-p) R^(-p-5/2). For 23/4 <= p <= 6, integrating from p to 6 gives the same conclusion, with the stronger power -p-23/8. On the intervening interval, (p-4)(6-p) >= 7/16, so (9) again implies that conclusion. Consequently

    |E_(p,c)(k,m)| <= 10^402 (p-4)(6-p) R^(-p-5/2)
       for 4 <= p <= 6 and |k| > 6.                    (12)

This handles both endpoints uniformly; no lower bound on their distance from p is imposed.

For an explicit lower bound on the leading coefficient, put t = p/2-2 in [0,1]. Gamma recurrence gives

    b(p) = -C(p)/((p-4)(6-p))
      = 2^p pi (1+t)^2(2+t)^2 Gamma(1+t)/Gamma(2-t),    (13)

with the continuous endpoint interpretation. The integral definition yields

    Gamma(1+t) >= integral_1^2 exp(-x) dx > 1/8,
    Gamma(2-t) <= 1 + integral_1^infinity x exp(-x) dx
                = 1+2/e < 2.

Thus b(p) >= 1 throughout the closed interval. In particular C(p) is negative on 4 < p < 6. These estimates avoid an unspecified positive minimum of a Gamma ratio.

## 6. All harmonics and the explicit threshold

Let n >= 6 be even and alpha_n = pi j_n/n. Rounding gives

    pi/4 <= alpha_n <= 5pi/12,

so c_n lies in [1/2,3/2], within the quantitative family used above. For

    I_phi = integral_T H_(p,c_n)(theta,n theta+phi),

the accepted exact restriction identity is

    D_p(c_n,n) = I_0-I_(pi/2)
      = 4 sum_(m>=1, m congruent to 2 mod 4)
                    Hhat_(p,c_n)(mn,m).                (14)

For completeness, (9) gives absolutely summable two-dimensional Fourier coefficients for each real 4 <= p <= 6, so termwise restriction is valid. H is separately even in theta and u, and H(theta+pi,u+pi)=H(theta,u). Hence odd m vanish after restriction for even n; the phase difference selects m congruent to 2 modulo 4. Factoring out z from 1+z^2+c_n z^(n+1) gives I_0. Shifting theta by pi/2 in the middle-minus polynomial gives I_(pi/2) or I_(-pi/2), which are equal by the same symmetry.

Every m in (14) is even, so

    cos(mn alpha_n) = cos(m pi j_n) = 1.

The leading term of the corresponding coefficient in (11) is therefore negative, with magnitude

    L = b(p)(p-4)(6-p)/(pi^2 s_n c_n)
          * m^(-p-2) * (n^2/s_n^2+1/c_n^2)^(-(p+2)/2).

Use b(p) >= 1, pi^2 s_n c_n <= 48, and

    1/s_n^2 + 1/(c_n^2 n^2) <= 1+4/36 < 2.

Since (p+2)/2 <= 4, this proves

    L >= 10^(-4) (p-4)(6-p) (mn)^(-p-2).              (15)

In (12), R = sqrt((mn)^2+m^2) >= mn. Dividing its bound by (15) gives the uniform ratio

    |E|/L <= 10^406 (mn)^(-1/2).                       (16)

For n >= N = 10^1000 and every surviving m >= 2, the right-hand side is at most 10^(-94)/sqrt(2), which is strictly less than 1/2. Thus every single summand in (14) is strictly negative, simultaneously for every real 4 < p < 6. The series is absolutely convergent and its m=2 term is nonzero. Its sum is strictly negative, proving (1) with the stated explicit K_0.

The same argument in fact works for any even n satisfying 10^406/sqrt(2n) < 1/2, but the round value N = 10^1000 avoids any claim of useful numerical sharpness. There is no fixed-harmonic extrapolation, sampled-exponent inference, numerical quadrature, or unbounded-constant step in this conclusion.

## 7. Scope of the quantitative improvement

This supplies an explicit, p-independent threshold for the entire accepted moving-coefficient family, rather than just for fixed p=5 or for a subsequence. It also makes the equal-coefficient subsequence K congruent to 1 modulo 6 effective, because n divisible by 6 gives j_n=n/3 and c_n=1 exactly. This argument gives a uniform witness above the stated threshold. The separate fixed-p support exclusion in [Proof 30](30_all_odd_triples.md) covers every odd K>=7, while the unrestricted cubic and K5 support questions remain open.

The proof is mathematical rather than a computational sign certificate. A separate arithmetic check of the deliberately coarse constant inequalities may be supplied as an aid to review; it is not a substitute for Sections 2-6. Prior accepted artifacts and their hashes are preserved.
