# Proof 29  Bounded circuit mass and finite affine shapes at every fixed exponent

Included dependencies: [Circuit obstructions and positive uncentered blocks](01_circuit_obstructions.md).

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

## 1. Statement and scope

Let MP_p(Gamma) mean the constant-one Fourier majorant inequality for every finitely supported real coefficient family on Gamma subset Z^d:

    integral |sum a_n exp(2 pi i n.x)|^p dx
        <= integral |sum A_n exp(2 pi i n.x)|^p dx
    whenever |a_n| <= A_n.

All torus measures are normalized. Fix p>0 that is not a positive even integer, put q=p/2, and put m=floor(q). Thus q is not an integer.

A primitive affine circuit is the unique primitive integer relation lambda on a minimally affinely dependent set of distinct frequencies. Its positive and negative masses are equal; write their common value as K. Every entry is nonzero, and a circuit has at least three entries.

**Theorem.** If MP_p(Gamma) holds, then:

1. If m=0, Gamma is affinely independent.
2. If m>=1 is odd, every primitive affine circuit in Gamma has mass K<=2m.
3. If m>=2 is even, every primitive affine circuit in Gamma has mass K<=2m+1.

In the third case, any circuit of the maximal permitted mass K=2m+1 must, up to permutation and overall sign, have one of the forms

    (K, -(K-b), -b),
    (K-b, b, -(K-b), -b),

where b is even, 2<=b<=m, and gcd(K,b)=1. These are necessary candidate forms only.

For m>=1 define B=2m when m is odd and B=2m+1 when m is even. If the augmented affine rank of nonempty Gamma is r, then

    |Gamma| <= B(2B+1)^r,              1<=r<=d+1.

For every fixed p and d there are only finitely many possible rational-affine equivalence classes of MP_p frequency sets. An explicit finite list of rational-coordinate candidate sets is given in Section 6. Membership in that list is not asserted to be sufficient for MP_p, and an effective exact test for MP_p on every candidate is not supplied.

## 2. Analytic input and the elementary parity reduction

The existing circuit test is the dominant-coefficient expansion in [Proof 01, Section 1](01_circuit_obstructions.md), using the method of Gressman--Guo--Pierce--Roos--Yung, *On the strict majorant property in arbitrary dimensions*, Q. J. Math. 74 (2023), 139--161, Proposition 4.1 (arXiv v2 Proposition 10):

- https://doi.org/10.1093/qmath/haac021
- https://arxiv.org/abs/2106.12538v2

For every circuit entry lambda_i it gives the necessary condition

    binom(q,K) binom(q,K-|lambda_i|) > 0.                 (C)

The binomial coefficients are nonzero because q is not an integer. The new two-scale calculation needed here is proved directly below; no sufficiency of (C) is used.

Write B_q(k)=binom(q,k) for integer k>=0. Its sign is positive for k<=m+1 and, thereafter, is (-1)^(k-m-1).

If K>m+1, primitiveness supplies an odd entry a=|lambda_i|. If B_q(K) were negative, K would have parity opposite to m+1. The complementary index K-a would have parity m+1 and would therefore have positive binomial coefficient, whether in the initial range or the alternating tail, contradicting (C). Hence

    K == m+1 (mod 2),    B_q(K)>0.

For each odd entry a, the complementary index K-a has the opposite parity, so (C) forces K-a<=m. In particular,

    every odd entry has magnitude at least K-m.          (2.1)

If m is odd and K>m+1, then K is even. A sign side containing an odd entry has at least two such entries, so 2(K-m)<=K and K<=2m. The cases K<=m+1 also satisfy K<=2m.

If m is even and K>2m, then K is odd and each sign side has exactly one odd entry: each side has an odd number of odd entries, and (2.1) makes each such entry greater than K/2. All its other entries are even, with their total on that side at most m. Write the positive and negative odd magnitudes as K-e and K-f, respectively, where

    e,f are even;   0<=e,f<=m.

At least one of e,f is positive, because a circuit has at least three entries.

For m=0, every circuit has K>=2>m+1. The same argument makes K odd and every odd entry of magnitude K. Each side would then consist of one entry, contrary to circuit support size at least three. Thus there are no circuits. The affine-independence sufficiency, although not needed for the bound, is the cited paper's arXiv Proposition 13 and Lemma 14 (journal Proposition 8.2 and Lemma 8.3).

## 3. Exact two-scale coefficient, including the multinomial factor

Assume m>=2 is even and the circuit has K>2m. Choose one odd entry as base, orienting lambda so that

    lambda_0=K-e>0.

Choose any even entry lambda_j, on either sign side, and put b=|lambda_j|. Let h be the other odd entry; thus h differs from 0 and j. Translate the base frequency to zero and write nu_i=n_i-n_0. For fixed 0<y<1 put

    P_+(t,x)=1+y exp(2 pi i nu_j.x)
                 +t sum_{i not in {0,j}} exp(2 pi i nu_i.x),
    P_-(t,x)=P_+(t,x)-2t exp(2 pi i nu_h.x),

and define Delta_y(t)=integral |P_+(t,x)|^(2q) dx minus integral |P_-(t,x)|^(2q) dx. The second polynomial changes precisely one real coefficient's sign and has exactly the same coefficient magnitudes.

Let s denote the circuit support size and define

    ell=2K-|lambda_0|-b=K+e-b,
    D=product_{i not in {0,j}} |lambda_i|!.

For |t|<(1-y)/(s-2), the binomial products around the constant term converge absolutely and uniformly in x. They define a real-analytic function of real t near zero (equivalently, replace both appearances of the real variable t in the two binomial factors by the same complex variable to obtain a holomorphic extension).

The exact leading sign-sensitive coefficient is

    Delta_y(t)
      = 4 [e! K!/(b! D)] binom(q,e) binom(q,K) y^b
          * F_y * t^ell + O_y(t^(ell+1)),                (3.1)

where

    F_y = sum_{N>=0} [(e-q)_N (K-q)_N/((b+1)_N N!)] y^(2N)
        = 2F1(e-q,K-q;b+1;y^2).                         (3.2)

Here (a)_N is the rising factorial, with (a)_0=1. The implied remainder is for fixed y; no uniformity as y tends to 1 is asserted or needed. In fact parity also permits O_y(t^(ell+2)), but the weaker remainder displayed is sufficient.

### Proof of (3.1)

Delete the base coordinate from lambda and call the resulting vector c. The translated frequency matrix has a one-dimensional rational kernel generated by c. The vector c is primitive: a common divisor of its entries also divides lambda_0=-sum c_i. Thus every integrated binomial monomial with nonnegative multiindices alpha,beta satisfies

    alpha-beta=k c,        k in Z.

The changed coefficient has sign factor (-1)^(alpha_h+beta_h)=(-1)^(k lambda_h)=(-1)^k. Terms with even k therefore cancel from Delta_y. For odd k the degree in the small amplitudes t is at least

    sum_{i not in {0,j}} |k lambda_i|=|k| ell.

Consequently the first possible degree is ell, where only k=1 and k=-1 occur. For k=1, all small-coordinate counts must be minimal:

    alpha_i=max(lambda_i,0), beta_i=max(-lambda_i,0)
    for i not in {0,j}.

The y-coordinate permits a common additional count N>=0. If lambda_j=b>0 then alpha_j=b+N, beta_j=N; if lambda_j=-b then alpha_j=N, beta_j=b+N. In both cases the full nonbase positive and negative masses are e and K, so

    |alpha|=e+N,    |beta|=K+N.

The coefficient for this monomial is exactly

    binom(q,e+N) binom(q,K+N)
        * (e+N)! (K+N)! / [(b+N)! N! D] * y^(b+2N).

The k=-1 coefficient is identical, and all-positive minus sign-flipped contributes a factor 2 to each of the two terms. This gives the factor 4 in (3.1). Using

    binom(q,L+N)(L+N)! = binom(q,L)L! (-1)^N (L-q)_N

for L=e,K yields (3.2); the two factors (-1)^N cancel. Absolute convergence allows the indicated collection of coefficients and integration. Analyticity gives the remainder after the first coefficient. This proof applies to an even y-coordinate on either sign side.

## 4. The negative singular tail and the mass bound

The factors outside F_y in (3.1) are strictly positive. Indeed e<=m and e is even, while K is odd and B_q(K)>0 by Section 2.

Since e and m are even and 0<=e<=m, the number a=e-q is a negative noninteger with precisely m-e+1 negative factors in (a)_N once N>=m-e+1. That number is odd. Also K-q>0. Consequently all sufficiently late coefficients

    u_N=(e-q)_N(K-q)_N/((b+1)_N N!)

are strictly negative. Moreover,

    u_N ~ C N^(ell-p-2),
    C=Gamma(b+1)/[Gamma(e-q)Gamma(K-q)] < 0.             (4.1)

This follows by writing the rising factorials as Gamma ratios and using Gamma(N+a)/Gamma(N+c) ~ N^(a-c). There is also a direct elementary verification: after the signs stabilize,

    |u_(N+1)|/|u_N|
       = ((N+e-q)(N+K-q))/((N+b+1)(N+1))
       = 1+(ell-p-2)/N+O(N^-2).

Taking logarithms and summing the O(N^-2) errors shows that |u_N| divided by N^(ell-p-2) tends to a finite strictly positive constant. This proves the growth claim without requiring any hypergeometric continuation formula.

If ell>p+1, the exponent in (4.1) is greater than -1. The eventual negative coefficient tail therefore has infinite total negative sum at y=1. More explicitly, its negative is a power series with nonnegative coefficients whose sum tends to +infinity by monotone convergence as y increases to 1. The finite initial part stays bounded. Thus

    F_y -> -infinity as y increases to 1.                (4.2)

Choose and then fix y<1 sufficiently close to 1 that F_y<0. Only after fixing y choose t>0 sufficiently small, with (s-2)t<1-y. Formula (3.1) gives Delta_y(t)<0. This is an actual finite real-coefficient counterexample to MP_p on the circuit, with a controlled analytic remainder; it is not a merely formal sign calculation at y=1.

Now suppose K>=2m+3. At least one sign side has a nonzero even total. Orient the base odd entry on that side, so e>0, and choose any even entry from the same side. Then b<=e, and hence

    ell=K+e-b >= K >= 2m+3 > p+1,

because p<2m+2. The counterexample above rules out this circuit. Since K>2m has odd parity, the only remaining high mass is K=2m+1. This proves the stated uniform mass bound for even m.

## 5. Necessary shapes at the maximal even-m mass

Assume m>=2 is even and K=2m+1. If either sign side has at least two even entries, choose its odd entry as base and one of those even entries for y. Then e-b is a positive even integer, so

    ell=K+e-b >= K+2=2m+3 > p+1.

Section 4 excludes the circuit. Therefore each side has at most one even entry.

If only one side has an even entry b, the circuit has the three-point pattern (K; K-b,b). If both sides have even entries with distinct magnitudes e and f, orient the base side so that e>f and choose the opposite-side even entry b=f for y. The two-sided validity of (3.1) gives ell=K+e-f>=K+2>p+1, again excluding the circuit. Thus both even magnitudes must equal the same b, yielding (K-b,b; K-b,b).

The restrictions b even and 2<=b<=m follow from Section 2. Primitiveness gives gcd(K,b)=1 in both patterns. Nothing here establishes that every such surviving candidate has MP_p.

## 6. Finite cardinality and finite rational-affine candidate lists

Fix m>=1 and the bound B from Section 1. Choose any affine basis n_1,...,n_r from a nonempty MP_p set Gamma, with augmented vectors v_i=(1,n_i). A minimum-volume basis is permissible but is no longer needed once every circuit has bounded mass.

For any n in Gamma outside the basis, write v=(1,n) in this basis. The support of this coordinate representation together with v is its fundamental affine circuit. Orient the primitive integer relation as

    t v + sum_{i=1}^r lambda_i v_i=0,    t>0,

allowing zero lambda_i at unused basis positions. The uniform circuit-mass bound gives

    1<=t<=B,    -B<=lambda_i<=B.

Since every augmented vector has first coordinate 1, t+sum_i lambda_i=0. Thus the coordinate vector of v belongs to the explicit finite grid

    G_(B,r)={(-lambda_1/t,...,-lambda_r/t):
               1<=t<=B; lambda_i in Z, |lambda_i|<=B;
               sum_i lambda_i=-t}.

This grid includes the basis coordinate vectors e_1,...,e_r (take t=1). Distinct frequencies have distinct coordinate vectors. Therefore

    |Gamma| <= |G_(B,r)| <= B(2B+1)^r.

The same argument works directly for infinite Gamma: its rational affine span has finite dimension, so it has a finite affine basis, and every further point defines the stated finite fundamental circuit. Injection into the same finite grid excludes infinitude. No infinite Fourier-series interpretation is required.

Normalize the chosen affine basis to 0,e_1,...,e_(r-1) by using coordinates (x_2,...,x_r) on the hyperplane sum_i x_i=1. Every normalized Gamma is a subset of the corresponding projection of G_(B,r) containing these r fixed basis points. Thus there are at most

    2^(|G_(B,r)|-r) <= 2^(B(2B+1)^r-r)

normalized candidate subsets in affine rank r. This deliberately generous count can include different presentations of one shape and candidates failing MP_p. If an integer rather than rational finite list is desired, multiply the entire grid by L=lcm(1,...,B). Its projected coordinates then lie in the fixed integer box [-BL,BL]^(r-1).

The empty configuration can be added separately. When m=0, affine independence allows only one rational-affine shape in each affine rank r<=d+1, also giving finitely many shapes.

### Why rational-affine equivalence preserves the full MP_p question

For any finite labelled integer configuration (n_i), augment its characters by an independent common circle variable: z_i=exp(2 pi i(t+n_i.x)). The common factor does not change |sum a_i z_i|. The pushforward of normalized Haar measure under these characters is determined by the Fourier integrals

    integral product_i z_i^(k_i) = 1
       if sum_i k_i=0 and sum_i k_i n_i=0,
    and =0 otherwise,

for all integer vectors k. Two configurations related by an injective rational-affine transformation have exactly the same integer affine relation lattice, hence the same pushforward probability measure. Equality follows from uniqueness of Fourier coefficients for probability measures on a finite-dimensional torus, or density of trigonometric polynomials. Consequently they have identical coefficient-dependent pth-power integrals for all real (indeed complex) coefficient choices. This proves the claimed invariance and justifies reducing MP_p to a finite list of rational-affine candidate shapes.
