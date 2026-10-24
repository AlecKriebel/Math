# Exact arithmetic profiles; no numerical QI invariance claim

The table computes the sole nonzero L2 Betti number c_T=b_d^(2)(Q_T), with d=rank(T)−1. The different positive numbers do **not** prove quasi-isometry inequivalence. The qualitative support, compact-support/coarse cohomology rings, and top two central-product heat exponents all agree within a rank-matched pair.

| T | d | Coxeter h | Exponents e_i | c_T=∏_{i≥2}(e_i−1) |
|---|---:|---:|---|---:|
| F4 | 3 | 12 | 1,5,7,11 | 240 |
| H4 | 3 | 30 | 1,11,19,29 | 5,040 |
| D6 | 5 | 10 | 1,3,5,5,7,9 | 1,536 |
| E6 | 5 | 12 | 1,4,5,7,8,11 | 5,040 |
| D7 | 6 | 12 | 1,3,5,6,7,9,11 | 19,200 |
| E7 | 6 | 18 | 1,5,7,9,11,13,17 | 368,640 |
| D8 | 7 | 14 | 1,3,5,7,7,9,11,13 | 276,480 |
| E8 | 7 | 30 | 1,7,11,13,17,19,23,29 | 127,733,760 |

## Primary theorem and computation boundary

[Brieskorn, *Sur les groupes de tresses*, Theorem 6(ii)](https://www.numdam.org/item/SB_1971-1972__14__21_0.pdf), exposé 401, scanned page 401-09 / printed p.29, explicitly gives the reflecting-hyperplane complement's Poincare polynomial ∏(1+e_i u). The formula was checked visually in the cached scan sources/brieskorn_theorem6.png. Deconing removes the factor 1+u. Evaluating at u=−1 and applying the inspected arrangement L2 theorem gives c_T in the table.

The arithmetic is reproduced by python3 compute_profiles.py, which uses only the standard library. It constructs simple reflection matrices from the relevant Cartan matrices, multiplies them to form a Coxeter element, and computes its characteristic polynomial exactly over Q(√5) by Faddeev–LeVerrier. For each type it checks the exact order h; in crystallographic types it also checks the claimed eigenvalue list through exact cyclotomic factorizations. The output profiles.json includes the characteristic polynomials, every Poincare coefficient, signed Euler characteristics, and final products. These are finite exact calculations, not numerical estimates of an infinite-group spectrum.

## H4 exponent certificate

Put a=(1−√5)/2. The computed characteristic polynomial is

\[
f(x)=x^4+a(x^3+x^2+x)+1.
\]

The program verifies exactly that f(x)\bar f(x)=Φ_30(x), where the bar sends √5 to −√5. To select the four roots belonging to f rather than its conjugate, write y=x+x^−1. Then

\[
x^{-2}f(x)=y^2+ay+a-2.
\]

The two y-roots lie respectively in (19/10,2) and (−7/5,−13/10), by substitution and the elementary bound 2.23<√5<2.24. The primitive thirtieth roots have y-values 2cos(kπ/15), k∈{1,7,11,13}; the roots with k>15 have the same y as their inverses. The positive y-root must have k=1, since k=7 gives 0<2cos(7π/15)<1 and the other choices are negative. The negative y-root must have k=11, since 2cos(13π/15)<−√3<−7/5. Thus the exponents are 1,11,19,29, as recorded. No floating-point root identification is used in the certificate.

## Strongest inference allowed

All c_T are strictly positive. This justifies the nonzero coefficient required in the two failed filters. Neither c_T nor the finite Poincare polynomial, unbounded virtual Betti numbers, or ordinary Euler characteristic is promoted to an invariant of arbitrary group quasi-isometries.
