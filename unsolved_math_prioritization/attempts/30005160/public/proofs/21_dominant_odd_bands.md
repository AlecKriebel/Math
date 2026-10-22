# Proof 21  Dominant constant coefficient boxes on odd frequency bands

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## Lemma

Let E be a finite set of positive odd integers, let m=min E and N=max E, and suppose N<2m. Let 4<p<6. For nonnegative numbers C and A_n satisfying C≥sum_(n∈E) A_n, every real coefficient family with |c|≤C and |a_n|≤A_n satisfies

    ||c+sum_(n∈E) a_n z^n||_p ≤ ||C+sum_(n∈E) A_n z^n||_p.

This is a theorem about this prescribed coefficient box; it is not an unrestricted majorant theorem for {0}∪E.

## Proof

Put q=p/2∈(2,3). If C=0 there is nothing to prove. First compare the sign vertices c=±C, a_n=±A_n. A global sign removes the sign of c, so take c=C. Write H(z)=sum A_n z^n. Since sum A_n≤C, the generalized binomial expansion of (C+H)^q converges absolutely uniformly, including when equality holds: sum_j |binom(q,j)|<∞. The same is true for every signed H. Products with the conjugate series can therefore be integrated termwise.

The block H^j has frequencies between jm and jN, all congruent to j modulo 2. A resonance between a monomial in H^j and one in H^l thus requires j≡l mod 2.

For odd j, binom(q,j)>0. For even j, binom(q,j)>0 at j=0,2 and binom(q,j)<0 at every even j≥4. Hence a negative product binom(q,j)binom(q,l) could occur only when one index is 0 or 2 and the other is an even integer ≥4. Index 0 cannot resonate with a positive block because every frequency is strictly positive. For index 2 versus l≥4, every degree in H² is at most 2N, while every degree in H^l is at least 4m. The strict inequality N<2m rules out those resonances as well.

Therefore every nonzero integrated block contribution has nonnegative scalar binomial product. Expanding each block into monomials, a real coefficient sign only multiplies its contribution by ±1. Replacing all signs by plus consequently weakly increases the integral of |C+H|^(2q). This proves the inequality at every sign vertex of the box.

Because p>1, the Lp norm is convex as a function of the finite real coefficient vector. Every point of the coefficient box is a convex combination of its sign vertices. Their dominance by the all-positive vertex proves the full stated coefficient-box inequality.

## Three-frequency corollary

Let K≥5 be odd. For all 4<p<6 and nonnegative A,B,C with C≥A+B,

    ||a+bz²+cz^K||_p ≤ ||A+Bz²+Cz^K||_p

whenever a,b,c are real and |a|≤A, |b|≤B, |c|≤C.

Indeed multiply the polynomial by z^(−K), conjugate the circle variable, and use the lemma with E={K−2,K}; these are positive odd integers and K<2(K−2) exactly when K>4. The constant coefficient after this transformation is the original frequency-K coefficient.

In particular this gives a full prescribed-box positive result on the unresolved support {0,2,5} whenever its frequency-5 bound dominates the other two bounds. It does not cover the triangle regime C<A+B or arbitrary coefficient boxes.
