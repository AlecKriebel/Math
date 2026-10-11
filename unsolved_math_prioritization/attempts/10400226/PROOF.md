# Knots with determinant 4k + 1 and signature four

## Statement, attribution, and scope

For every integer n > 1 satisfying n ≡ 1 (mod 4), there is a tame knot K in S³ with determinant n and signature 4. This is exactly the affirmative conclusion sought in Ohtsuki's Problem 12.21 (Y. Shinohara), printed p. 540, physical PDF p. 168.

The proof below is an independently written and checked exposition of the construction in Alper Ferudun, *Knots with Signature 4 and Determinant 4k+1: An Answer to a Question of Shinohara*, Theorem 1.1 and Lemmas 3.1–3.2, dated 2 October 2026, DOI [10.5281/zenodo.23111900](https://doi.org/10.5281/zenodo.23111900), [manuscript page](https://eulersolve.org/papers/amr-103-0226/). The author identifies that work as an unrefereed, AI-assisted preprint. This exposition claims neither novelty nor human or external peer review. Its conclusion does not certify the source paper's other theorems, lattice-theoretic sketch, knot tables, or computer programs.

## Standard inputs

We use the following classical results.

1. **Seifert realization.** An integral 2g × 2g matrix V whose skew part V − Vᵀ is a unimodular alternating form is the Seifert matrix of a knot bounding an oriented genus-g surface in S³. Its determinant is |det(V + Vᵀ)|, and its signature, with the chosen convention, is sign(V + Vᵀ). If the opposite signature convention is used, mirror the knot. Determinant is unchanged by mirroring.
2. **Dirichlet's theorem.** If gcd(a, q) = 1 and q > 0, the progression a modulo q contains infinitely many primes.
3. **Quadratic reciprocity.** For positive coprime odd integers a, b, Jacobi symbols satisfy (a/b)(b/a) = (−1)^(((a−1)/2)((b−1)/2)). For an odd prime ℓ, (−1/ℓ) = (−1)^((ℓ−1)/2). With prime denominator, a symbol equal to 1 means a nonzero square residue.
4. **Sylvester's criterion.** A real symmetric matrix with all its leading principal determinants positive is positive definite.

The realization assertion is independently corroborated in Stefan Friedl's [*Realizations of Seifert matrices by hyperbolic knots*, introduction, p. 1](https://arxiv.org/pdf/0704.3390). The exact one-component criterion appears as Theorem 7.6, physical p. 80 of [knot-theory lecture slides hosted at Kyushu University](https://www2.math.kyushu-u.ac.jp/~saeki/Lee-Lectures.pdf). For the matrices used below the skew part is already J ⊕ ⋯ ⊕ J, where J = [[0,1],[-1,0]], so no general classification or stabilization is needed. Changing the second basis vector in each pair to its negative gives the opposite sign convention in those slides. Taking the number of link components to be one gives the knot realization and genus bound.

Dirichlet's theorem is stated as Theorem 18.1 on physical p. 177 of Andrew V. Sutherland's [MIT 18.785 notes, Fall 2021](https://ocw.mit.edu/courses/18-785-number-theory-i-fall-2021/mit18_785f21_full_lec.pdf). The Legendre and Jacobi identities used here are also stated in [Stanford's quadratic-reciprocity notes](https://crypto.stanford.edu/pbc/notes/numbertheory/quadrecip.html).

## A positive-definite four-dimensional family

For integers b, c and an even integer y, put

    V = [[1, 1,   0, 0],
         [0, b, y/2, 0],
         [0,y/2,  c, 1],
         [0, 0,   0, 1]].

All entries are integral and V − Vᵀ = J ⊕ J. Its symmetric part is

    S = [[2, 1,  0, 0],
         [1,2b,  y, 0],
         [0, y, 2c, 1],
         [0, 0,  1, 2]].

Expansion of the successive tridiagonal determinants gives

    D₁ = 2,
    D₂ = 4b − 1,
    D₃ = 2c(4b − 1) − 2y²,
    D₄ = (4b − 1)(4c − 1) − 4y² = 2D₃ − D₂.

If b ≥ 1 and D₄ > 0, then D₁ > 0, D₂ ≥ 3, and D₃ = (D₄ + D₂)/2 > 0. Thus S is positive definite and has signature four. In particular, any choice satisfying

    b ≥ 1 and (4b − 1)(4c − 1) − 4y² = n > 0

gives the required determinant and signature after Seifert realization.

## Every nonsquare n

Assume n > 1, n ≡ 1 (mod 4), and n is not a square. Write n = s²m with s a positive integer and m > 1 squarefree. Since n is odd, s and m are odd; hence s² ≡ 1 (mod 4) and m ≡ 1 (mod 4).

Choose a prime r dividing m. The prime r is odd, so choose a nonzero quadratic nonresidue u modulo r. The three moduli 4, r, and m/r are pairwise coprime. The Chinese remainder theorem gives a residue t modulo 4m such that

    t ≡ 3 (mod 4),  t ≡ u (mod r),  t ≡ 1 (mod m/r).

If m/r = 1, the last condition is vacuous. The residue t is coprime to 4m. At the factor r its quadratic character is −1, and at every other prime factor of m it is +1. Therefore (t/m) = −1.

Dirichlet's theorem gives infinitely many primes ℓ ≡ t (mod 4m). Only finitely many primes divide s, so choose such an ℓ with ℓ ∤ s. The reduced residue condition also gives ℓ ∤ m. Consequently ℓ ∤ n and ℓ ≡ 3 (mod 4). Now

    (n/ℓ) = (s²/ℓ)(m/ℓ) = (m/ℓ)
          = (ℓ/m) = (t/m) = −1.

The reciprocity sign is +1 because m ≡ 1 (mod 4). The symbols with denominator m are only used to compute characters; no square-root conclusion is drawn from a composite denominator. Since (−1/ℓ) = −1, multiplicativity yields (−n/ℓ) = +1. There is therefore a nonzero x modulo the prime ℓ with x² ≡ −n (mod ℓ).

Since 2 is invertible modulo ℓ, choose y₀ in {0,…,ℓ−1} satisfying 2y₀ ≡ x (mod ℓ). In fact y₀ ≠ 0. Set y = y₀ if y₀ is even, and y = y₀ + ℓ otherwise. Then y is nonnegative and even, and ℓ divides n + 4y². Define

    h = (n + 4y²)/ℓ.

This is positive. Reduction modulo 4 gives ℓh ≡ 1 and ℓ ≡ 3, so h ≡ 3 (mod 4); in particular h ≥ 3. Let

    b = (ℓ + 1)/4,  c = (h + 1)/4.

Both are positive integers. Their matrix satisfies D₄ = ℓh − 4y² = n and has the required invariants.

## Square determinants and an exhaustive case division

There is an immediate additional case. If n has any prime divisor ℓ ≡ 3 (mod 4), put h = n/ℓ. Since n ≡ 1 (mod 4), h is a positive integer congruent to 3 modulo 4, and hence h ≥ 3. Taking

    y = 0,  b = (ℓ + 1)/4,  c = (h + 1)/4

in the four-dimensional family gives determinant n and signature four. This applies in particular to every square with a prime divisor congruent to 3 modulo 4.

After the preceding two cases, the only remaining n are squares n = s² with s > 1 and all prime divisors of s congruent to 1 modulo 4. Choose a prime p dividing s. Then p ≥ 5 and p ≡ 1 (mod 4). Since p is nonsquare, the nonsquare construction gives a 4 × 4 Seifert matrix Vₚ with symmetric determinant p and signature four.

Let h = n/p. This is a positive integer congruent to 1 modulo 4; indeed h ≥ p ≥ 5. Define the integral matrix

    W = [[−1, 1],
         [ 0, (h−1)/4]].

Its skew part is J, and

    W + Wᵀ = [[−2, 1],
              [ 1, (h−1)/2]]

has determinant −h. A real symmetric 2 × 2 matrix with negative determinant has one positive and one negative eigenvalue, so its signature is zero. The matrix Vₚ ⊕ W has skew part J ⊕ J ⊕ J, symmetric determinant −ph = −n, and signature 4 + 0 = 4. Seifert realization therefore gives a knot of determinant |−n| = n and signature four.

The three cases are exhaustive. The constructed surfaces have genus two in the first two cases and genus three in the last. Thus the knot genus is at most two or at most three, respectively. This proof makes no assertion that genus two suffices in the remaining square case. It also imposes no prime, hyperbolic, alternating, or two-bridge condition on the knot.

This proves the stated theorem and answers the exact question in [Ohtsuki, Problem 12.21](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf). The same existence assertion is asked in [Stoimenow, §5.1, Question 5.1](https://www.impan.pl/shop/en/publication/transaction/download/product/83749).
