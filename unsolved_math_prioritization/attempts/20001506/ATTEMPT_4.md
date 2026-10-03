# Turn 4: periodic conjugacy through the second lower-central quotient

Date: 2026-10-03. Aim: find a nontrivial periodic conjugacy class of the exact phi. Such a class would make G nonhyperbolic, while the credited fully irreducible nongeometric lower map makes Gamma hyperbolic, proving the original QI separation. No such class is found here; no atoroidality certificate is claimed.

## Why the quotient torus does not supply the answer

Killing a,b,c leaves beta(d)=e, beta(e)=ed. It inverts the conjugacy class of [d,e], so that class has period two in the quotient. This does not lift automatically. In F5 the first image of [d,e] cyclically reduces to a e d a^-1 e^-1 d^-1, which has length 6, whereas [d,e] has length 4. Its first six full-map cyclic lengths are 6,10,16,28,46,76. These numbers are illustrative, not a proof that every iterate grows.

## An all-period necessary filter

Turn 1 proves that any periodic class w has zero abelianization. On gamma_2(F5)/gamma_3(F5), use the integral basis

    a∧b, a∧c, a∧d, a∧e, b∧c, b∧d, b∧e, c∧d, c∧e, d∧e.

The induced map is W=exterior^2(M); its matrix entries are 2-by-2 minors of M. Conjugation acts trivially on this quotient. If phi^n(w) is conjugate to w, its class c therefore satisfies W^n c=c.

The eigenvalues of W are pairwise products of eigenvalues of M. Write rho for the real root of x^3-x-1 and tau=(1+sqrt(5))/2. The two other cubic roots have modulus rho^(-1/2), and the other quadratic root is -tau^(-1). We have 1<rho<1.4<tau, so no pair product has modulus 1 except the product of the two quadratic roots, which is -1. M has distinct eigenvalues and is diagonalizable over C; so is its exterior square. Exact integer computation gives

    ker(W+I)=Q v,
    v=(0,1,0,1,1,0,1,-1,-1,1),
    rank(W+I)=9.

Consequently:

- For odd n, any periodic w is already in gamma_3(F5).
- For even n, its degree-two class is an integral multiple of v. Integrality of the multiple follows from the final coordinate v_10=1.

This filter is necessary for every period, not merely the tested periods. It does not exclude words whose first nonzero lower-central term has degree three or higher. Nor does it prove that multiples of v lift to periodic classes.

## Exhaustive finite test

search_periodic.py generates all freely and cyclically reduced words of cyclic length at most 8 with zero exponent sums, identifies cyclic rotations and inverse words, and applies the necessary exterior-square filter. Every surviving class is then tested under phi for unoriented periods 1 through 12, using exact free and cyclic reduction.

Counts by lengths 2,4,6,8:

- Cyclically reduced zero-homology words: 0, 80, 2160, 101040.
- Classes modulo rotation and inversion: 0, 10, 180, 6320.
- Classes surviving the all-period class-two filter: 0, 0, 0, 40.
- Periodic or inverse-periodic hits within 12 iterates: none.

Because odd-length zero-exponent words are impossible, the exterior-square filter and exhaustive enumeration actually rule out nontrivial periodic conjugacy classes of cyclic length at most 6 for every period. For length 8, the result is only the stated bounded-period negative search. An inverse-periodic hit would also have supplied a periodic conjugacy class after doubling the exponent; the search includes this possibility.

## Outcome

This route narrows the exact nonhyperbolicity search but does not decide whether phi is atoroidal. There is no certified all-length Nielsen-path bound here. Absence of a short periodic word cannot be promoted to hyperbolicity, let alone to a solution of the QI conjecture.

## Verification

verify_t4() independently assembles W from M, verifies Wv=-v, checks both ranks, and checks W's action on all ten basis commutators using Magnus coefficients. checks_turn4_linear.json records it. checks_turn4_search.json is the exact output of the separate bounded enumerator. Both scripts are dependency-free and read no private context or remote files.
