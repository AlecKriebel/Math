# Turn 5 Exact all size certificates for fixed edge bands

**Target:** 30005718 / OWR-14298007-013. **Fifth and final substantive author turn.**

**New result:** Exact Newton-basis certificates prove the original ULC inequalities for every row size in the lower band `k=4,...,63` and the upper band `1≤d_n−k≤40`, whenever the specified index is an interior index of the original polynomial. These are all-size fixed-band theorems, with a finite exact computational certificate. They do not cover every index as n grows.

Together with TURN_4, the packet proves that every sufficiently large row is ULC, but does not know an effective threshold or certify every remaining finite row. **The original all-n question remains unresolved after 5/5 turns.**

## 1 The original inequalities as polynomials in the row parameter

Use n=2r+4+p with r≥0 an integer and p in {0,1}. The original degree is

`d=3r+4+2p`.

Extend a coefficient v_(n,k) to zero outside 0≤k≤d. At a meaningful interior index define the original ULC difference

`Delta(n,k)=k(d−k)v_(n,k)^2−(k+1)(d−k+1)v_(n,k−1)v_(n,k+1)`.

For fixed lower index j≥1, put `k=j+3` and denote this expression by `P_lower,j,p(r)`. It is a polynomial in r of degree at most `2j+1`.

Here is the degree argument, which is essential to the certificate. From TURN_1,

`z^(-3)V_(m+4)=u(z)N(z)^m b(z)`,
`N(z)=I+z A+z^2 B`.

For the coefficient at z^j, the binomial expansion in powers of N−I terminates after at most j factors, because each factor has positive z-degree. It is a finite linear combination of binomial(m,l), with l≤j, and hence a polynomial in m of degree at most j. The endpoint polynomials cannot increase that bound. Substituting m=2r+p gives the bound j in r. Both products in Delta have degree at most 2j, and the remaining original-degree factor is affine in r. This proves the claimed bound for every fixed j, without guessing it from evaluations.

For fixed upper distance h≥1, put `k=d−h` and denote the resulting polynomial by `P_upper,h,p(r)`. Its degree is at most

`4h+3−2p`.

The exact unipotent reversal argument in TURN_3 proves that the coefficient at distance h has degree at most 2h+1 for p=0 and 2h for p=1. The neighboring distances h−1,h+1 have the corresponding shifted bounds. Their products therefore have degree at most 4h+2 or 4h, and the remaining degree factor is again affine in r. These are polynomial identities for all integer r≥0, including those small r where the coefficient itself is zero. The proof relies on the nilpotent constant part and finite word-length bounds of the reversed transfer, not on eventual interpolation.

## 2 A finite certificate that proves infinitely many row sizes

For a polynomial P(r) of degree at most D, Newton interpolation gives the exact identity

`P(r)=sum_(l=0)^D a_l binomial(r,l)`,

where

`a_l=sum_(s=0)^l (−1)^(l−s) binomial(l,s) P(s)`.

For every nonnegative integer r all binomial(r,l) are nonnegative, with value zero for l>r. Therefore nonnegative a_l certify P(r)≥0 for every such r. If the first positive coefficient has index r_0, then P(r)>0 for every integer r≥r_0.

This elementary Newton finite-difference criterion is sufficient, not necessary. For example `(r−2)^2+1` is positive everywhere but has Newton coefficients `(5,−3,2)`. Failure of this sufficient test would not be a counterexample to the original ULC statement.

Applying the criterion is a rigorous finite certificate only because the degree bounds in Section 1 have already been proved. Testing P(s)≥0 at finitely many values without that interpolation/sign certificate would not establish all row sizes.

## 3 The exact certified bands

The standard-library checker `checks/verify_turn5.py` generates the needed values directly from the original three-state matrix and initial conditions. It does not use approximate roots, numerical differences, the saddle theorem, or the two-state reduction to obtain those values. It forms exact integer forward differences and verifies:

- Every Newton coefficient of P_lower,j,p is nonnegative for `1≤j≤60`, p=0,1
- Every Newton coefficient of P_upper,h,p is nonnegative for `1≤h≤40`, p=0,1
- In each of the 200 polynomials the highest Newton coefficient is positive
- The first nonzero coefficient occurs at `max(0,ceil((j−2p)/3))` in the lower case, and at `max(0,ceil((h−1−2p)/3))` in the upper case

Those first-nonzero values are exactly the first row parameters for which the corresponding central coefficient is positive and the original inequality is an interior one. The identities consequently establish strict ULC throughout each stated meaningful band, for every n. The lower endpoint k=3 is immediate from the preceding zero coefficient and can be included separately.

The certificate comprises 14,360 exact Newton coefficients, of which 12,620 are positive. Its canonical compact JSON encoding has SHA-256

`63f530185b41356c61167ba5cd16b5a3d1d70bb837cd4d8b86c9bb4b00e29e2b`.

It can be generated independently with

`python checks/verify_turn5.py --dump certificate.json`.

The hash is over the canonical encoding before its trailing newline. The program's usual stdout is the compact frozen receipt. The large coefficient list is reproducible from the small source recurrence and need not be treated as an opaque external input. Four extra evaluation points per polynomial also check the implementation's reconstructed identities; the degree proof, not those extra checks, gives universality in r.

### Small displayed certificates

As transparent examples, the lower band at j=2, namely original k=5, has the following Newton coefficient vectors, beginning at l=0:

- p=0: `(0,12208,374752,1891776,3075072,1566720)`
- p=1: `(528,113952,1123808,3355968,3910656,1566720)`

Thus these displayed expressions alone prove that particular inequality for every row size. The program applies the same exact procedure to the full stated bands. All arithmetic uses Python integers and rational numbers; no rounding is involved.

The complete checker passes 16,063 exact assertions. These include the polynomial certificates, 800 additional identity controls, source-degree controls, and the separate real-rootedness obstruction below. The certificate-based all-size conclusion is stronger than merely reporting a finite sample of ULC rows, while remaining a fixed-band conclusion.

## 4 A simple all size shortcut fails

The stripped polynomial at n=7 is

`F_3(z)=4+40z+132z^2+195z^3+129z^4+32z^5+z^6`.

It is not real-rooted. An exact rational Sturm sequence has degrees 6,5,4,3,2,1,0. The signs of its leading coefficients are `(+, +, +, +, +, +, −)`, and its signs at zero are the same. Its signs at negative infinity are `(+, −, +, −, +, −, −)`. The variation counts are therefore 5 at negative infinity and 1 at zero or positive infinity. The final constant is nonzero. Hence there are four distinct negative real roots and one nonreal conjugate pair.

The checker obtains that sequence by rational polynomial division, rather than floating-point root finding. Multiplying by z^3 does not remove the nonreal pair. Therefore an attempted all-size proof by real-rootedness and the classical Newton inequalities cannot apply directly to this family. This does not disprove ULC: the original normalization still passes all checked inequalities for n=7.

## 5 What was not established

The observed nonnegative Newton coefficients suggest a possible sufficient infinite-family statement: all P_lower,j,p have nonnegative Newton expansions for every j. Proving that would settle every original index, since j=k−3. This turn proves it only through j=60; it supplies no recurrence or cone argument that propagates the coefficient signs to arbitrary j. The upper certificate is likewise restricted to h≤40. Neither cutoff may be silently removed.

The remaining original gap is still the one isolated in TURN_4: an all-size proof or an effective global threshold with verified overlap with the finite rows. The existential eventual theorem does not provide such an overlap. The general polynomial-matrix discussion now includes a sufficient compact-band variance test, a uniform small-saddle endpoint method, and a finite Newton-certificate method for polynomial fixed-index families. It does not classify all polynomial matrix recursions.

**Final disposition:** original unresolved/exhausted, 5/5 substantive author turns. No sixth author search. Scoped results and source distinctions should be independently reviewed before any public promotion. Historical priority of the scoped consequences is not certified. Subjective planning completion estimate 75 percent, not a correctness or novelty probability.
