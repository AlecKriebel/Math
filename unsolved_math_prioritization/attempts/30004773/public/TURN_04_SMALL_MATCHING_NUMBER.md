# Attempt 4: recover all degrees when the matching number is at most three

## A classical class-count polynomial, with a direct proof

For S subset V let c(S) be the number of connected components of Gamma[S], with c(empty)=0, and let N[S] be its closed neighbourhood. Set

K_Gamma(Q)=sum_{S subset V} (Q-1)^|S| Q^(m-|N[S]|+c(S)).       (6)

Every exponent is nonnegative: a spanning forest of Gamma[S] has |S|-c(S) edges, and choosing one edge from each vertex of N[S] minus S to S adds |N[S]|-|S| distinct edges. Their sum is |N[S]|-c(S), at most m.

For v in F_q^V with support S, the equation beta(v,u)=0 says that u_j/v_j is constant on each component of Gamma[S], that u is zero on N[S] minus S, and imposes no restriction on V minus N[S]. Its solution space therefore has dimension n-|N[S]|+c(S). The conjugacy class of (v,w) has size q^(|N[S]|-c(S)), since conjugation adds the image of u -> beta(v,u) in the central coordinate. Summing the reciprocal class size over all group elements gives exactly (6). Hence K_Gamma(q) is the number of conjugacy classes, or equivalently irreducible characters. This is Rossmann's class-count polynomial; the derivation is included to avoid importing an unread proof.

Together with Attempt 1, we have the two moment identities

sum_i N_i(Gamma;q)=q^m,
sum_i q^(n-2i) N_i(Gamma;q)=K_Gamma(q).                      (7)

## Rank bound from matchings

Every alternating matrix of rank 2i has a nonsingular principal submatrix of size 2i. For completeness, choose a nonzero entry and put its indices first. Its invertible alternating 2 by 2 block splits off by the Schur complement. Induction finds a nonsingular principal submatrix of the Schur complement of size rank(A)-2; the corresponding indices together with the pivot indices give a nonsingular principal submatrix of A, by the block determinant formula. The same elimination proves that ranks are even.

If a principal submatrix is nonsingular, its support graph has a perfect matching. Here is an argument avoiding any characteristic-dependent exterior-power formula. Expand its determinant by permutations. Fixed points vanish because the diagonal is zero. Pair each permutation containing an odd cycle with the permutation reversing its first such cycle (choose the cycle with smallest vertex). Odd cycles have length at least three. Reversal preserves the permutation sign and changes the product of alternating entries by -1, so these terms cancel. Each remaining permutation has only even cycles, each of which admits a matching covering all its vertices. If there is no perfect matching, there are therefore no remaining nonzero terms. This proves rank B_Gamma(y)<=2nu(Gamma) over odd fields. Conversely a maximum matching, weighted nonzero with all other edges zero, attains this bound.

## Theorem

If nu(Gamma)<=3, then every ch(Gamma,i;q) and every N_i(Gamma;q) is an integer polynomial in q, on odd prime powers. In particular this holds for every graph on at most seven vertices, and also for arbitrarily large graphs of matching number at most three.

## Proof and explicit recovery

N_0=1 and N_1=P_Gamma are known from Attempts 1 and 2. If nu<=1 nothing remains. If nu=2, then N_2=q^m-1-P_Gamma, an integer polynomial.

Suppose nu=3; then n>=6. Put

T(Q)=Q^m-1-P_Gamma(Q),
H(Q)=K_Gamma(Q)-Q^n-Q^(n-2)P_Gamma(Q).

By (7), N_2+N_3=T(q) and q^(n-4)N_2+q^(n-6)N_3=H(q). Hence

N_2(q)=[q^(6-n)H(q)-T(q)]/(q^2-1),
N_3(q)=[q^2 T(q)-q^(6-n)H(q)]/(q^2-1).                      (8)

Initially the right sides are rational functions with integer numerators and monic denominators, after multiplying top and bottom by q^(n-6). They are in fact integer polynomials, as follows from the elementary lemma below. Multiplication by q^(n-2i), a nonnegative power for a possible rank 2i, proves the assertion for character counts.

Lemma. If F(Q)=A(Q)/B(Q), where A,B belong to Z[Q] and B is monic, and F(p) is an integer for infinitely many positive primes p outside the zeros of B, then F belongs to Z[Q].

Proof. Monic polynomial division gives A=BC+R with C,R in Z[Q] and deg R<deg B. For the indicated primes, R(p)/B(p)=F(p)-C(p) is an integer and tends to zero as p tends to infinity. It is consequently zero for all sufficiently large primes in this infinite set. Thus R has infinitely many roots and is identically zero. This proves the lemma and (8), because N_2 and N_3 are actual integer counts for every odd prime.

Formula (8) is effective: compute the two finite vertex-subset polynomials P and K, then perform exact monic polynomial division. The proof establishes exact divisibility; finite interpolation is not used.

## Exact point where this approach stops

When nu=4, after N_0 and N_1 there are three unknown rank counts but only two equations in (7). The perturbation

(delta N_2, delta N_3, delta N_4)=(t,-(q^2+1)t,q^2 t)

preserves both equations identically. This is a statement about the insufficient information in these equations, not an assertion that these perturbations are realised by graphs or by nonnegative count distributions. No additional moment sufficient for arbitrary matching number was obtained. Historical novelty of the small-matching-number theorem is not asserted.
