# Every positive determinant 4k+1 greater than one occurs with signature four

## Scope and attribution

This is an independently written reconstruction of the argument in Alper Ferudun, *Knots with Signature 4 and Determinant 4k+1: An Answer to a Question of Shinohara*, 2 October 2026, Theorem 1.1 and Lemmas 3.1–3.2, DOI https://doi.org/10.5281/zenodo.23111900, https://eulersolve.org/papers/amr-103-0226/ . That manuscript expressly identifies itself as an unrefereed, AI-assisted preprint. Its central page 4 was checked both as extracted text and as a rendered image. This reconstruction does not claim novelty or external peer review and does not certify the paper's ancillary computational or lattice-theoretic claims.

The question is Ohtsuki's Problem 12.21, printed p. 540 (physical PDF p. 168), https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf . Stoimenow's 2007 paper, *Determinants of knots and Diophantine equations*, §5.1, gives earlier partial results: https://www.impan.pl/shop/en/publication/transaction/download/product/83749 . The imported problem title is truncated, but its statement is accurate.

## Mathematical inputs

Use the classical Seifert-matrix realization theorem: any integral even-size matrix V with unimodular alternating part V−Vᵀ is realized by an oriented knot. Its determinant is |det(V+Vᵀ)| and its signature is the signature of V+Vᵀ. A block direct sum corresponds to connected sum. The argument below also uses Dirichlet's theorem for a reduced arithmetic progression and quadratic reciprocity. These standard theorems, rather than a finite search, supply the unbounded existence steps.

## Matrix construction

For integers b,c and even y, define

    V(b,c,y) = [[1,1,0,0],
                [0,b,y/2,0],
                [0,y/2,c,1],
                [0,0,0,1]].

The alternating part is the direct sum of two matrices [[0,1],[-1,0]], hence has determinant one. Let S=V+Vᵀ. Its consecutive leading principal determinants are

    D₁=2,
    D₂=4b−1,
    D₃=2c(4b−1)−2y²,
    D₄=(4b−1)(4c−1)−4y².

They obey 2D₃=D₄+D₂. Consequently, if b≥1 and D₄=n>0, every Dᵢ is positive. Sylvester's criterion makes S positive definite, with signature four and determinant n. It remains to manufacture the indicated factorization of n+4y².

## Nonsquare integers

Suppose n>1 and n≡1 mod 4 is not a square. Factor n=s²m with m>1 odd and squarefree. Then m≡1 mod 4. Pick a prime r dividing m and a nonzero quadratic nonresidue u modulo r. The Chinese remainder theorem supplies a residue t satisfying

    t≡3 mod 4,   t≡u mod r,   t≡1 mod (m/r).

Thus gcd(t,4m)=1 and the Jacobi symbol (t/m) is −1. Dirichlet supplies infinitely many primes ℓ≡t mod 4m; choose one not dividing s. For this prime ℓ, quadratic reciprocity and m≡1 mod 4 give

    (n/ℓ)=(m/ℓ)=(ℓ/m)=(t/m)=−1.

Because ℓ≡3 mod 4, (−1/ℓ)=−1, and therefore (−n/ℓ)=1. There is an x with x²≡−n mod ℓ. Solve 2y≡x mod ℓ; changing y by ℓ if necessary makes it even. It may be taken nonnegative. Then

    h=(n+4y²)/ℓ

is a positive integer, and h≡3 mod 4, since n+4y²≡1 and ℓ≡3 mod 4. In particular h≥3. Set b=(ℓ+1)/4 and c=(h+1)/4. These are positive integers and

    (4b−1)(4c−1)−4y²=ℓh−4y²=n.

The matrix construction proves the desired result for every nonsquare n in the required congruence class.

## Squares and the remaining cases

If n has a prime divisor ℓ≡3 mod 4, put h=n/ℓ. Then h≡3 mod 4 and h≥3. Taking y=0, b=(ℓ+1)/4, c=(h+1)/4 again works. This also handles squares possessing such a prime factor.

The only remaining case is n=s²>1, with every prime divisor of s congruent to one mod four. Choose any prime p|s. It is nonsquare and p≡1 mod 4, so the preceding argument produces a four-by-four Seifert matrix Vₚ whose symmetric part has determinant p and signature four. Put h=n/p, so h≡1 mod 4, and use the two-by-two integral block

    W(h)=[[-1,1],[0,(h−1)/4]].

The alternating part of W is unimodular. Its symmetric part has determinant −h, hence one positive and one negative eigenvalue and signature zero. Therefore Vₚ⊕W(h) realizes a knot with determinant ph=n and signature four.

This proves the exact question for every n=4k+1 with k>0. The construction has genus at most two in the first two cases and at most three in the final square case. It does not prove that genus two suffices for every square, and no such additional assertion is made.

## Direct audit checks

For n=33049, the values b=5,c=437,y=6 give 19·1747−4·36=33049; the leading determinants are 2,19,16534,33049, all positive. For n=5, b=1,c=2,y=2 gives 3·7−16=5. For n=25, adjoining W(5) to that n=5 block gives absolute determinant 25 and signature four. These examples only check the formulas. The preceding Dirichlet and block arguments prove the unbounded assertion.

The proof neither executes nor depends on the source author's code. Mathematical acceptance remains subject to independent review of this exact reconstruction and its named standard inputs.
