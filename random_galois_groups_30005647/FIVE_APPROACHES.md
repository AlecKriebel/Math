# Fixed-degree next-most-probable Galois group: five approaches

Checked 2026-10-21. Queue row 1852, ID 30005647. **Outcome: NOT SOLVED.** This is an authored mathematical audit and collection of elementary consequences, not a new asymptotic theorem. No external communications or repository publication were made.

## Model and notation

Fix n and sample monic f=X^n+a_1 X^(n-1)+...+a_n with independent uniform integer a_i in [-H,H]; let H tend to infinity. The denominator is L^n, L=2H+1. Groups mean permutation groups on the n distinct roots, up to conjugacy. All nonseparable polynomials are included in the exceptional complement, not silently discarded. No irreducibility conditioning is imposed.

Write E for this exceptional complement of S_n, T for the standard point stabilizer S_(n-1), A for A_n, Q for nonzero square discriminant, I for irreducible nonzero square discriminant, and Z for zero discriminant. Event notation and event probabilities are distinguished below. The strong question is P(T)/P(E)→1. The literature gives P(T)~c_n/H, c_n>0. For n>=10 the recorded decomposition is P(E)=P(T)+P(A)+O_n(H^-2), after the harmless nonseparable convention is verified below. We do not extend that particular remainder to degrees 5–9.

## Attempt 1: isolate the residual and remove degeneracies

**Exact partial, proved.** For n>=10,

0 <= P(Q)-P(A) <= P(E)-P(T)-P(A) = O_n(H^-2),

and the same inequalities hold with I in place of Q. Indeed, A subset I subset Q subset E; the nonzero-square-discriminant criterion says G<=A_n, whereas the standard S_(n-1) contains a transposition and is not contained in A_n. Thus Q is disjoint from T. The remaining difference is contained in the published residual event. In particular P(Q minus I)=O_n(H^-2), so reducible square discriminants have negligible mass on the H^-1 scale.

It follows, rigorously, that for fixed n>=10 each of the following is equivalent:

1. P(T)/P(E)→1.
2. P(A)=o(H^-1).
3. P(I)=o(H^-1).
4. P(Q)=o(H^-1).
5. P(Disc(f) is a square, including zero)=o(H^-1).

For (1)↔(2), divide the nonnegative residual identity by P(T)~c_n/H; conversely P(E)~P(T) makes P(A)≤P(E)-P(T)=o(H^-1). Statements (2)–(4) follow from the O(H^-2) differences. Statement (5) uses the next lemma.

These statements are NOT event equalities and do NOT show P(Q)~P(A). An additive error O(H^-2) can exceed the conjectural size H^-n/2. This distinction prevents an incorrect solution of the separate square-discriminant asymptotic-equivalence problem.

### Elementary nonseparable count

For every fixed n>=3, #Z=O_n(H^(n-2)). Proof: a monic integer nonseparable f has a nonconstant monic integer g with g² dividing f. Put deg g=d, deg h=m=n-2d and f=g²h. Mahler measure is multiplicative and satisfies M(f)<=sqrt(n+1) max(1,H). Every monic degree k integer polynomial of Mahler measure at most Y has coefficients O_k(Y), hence there are O_k(Y^k) such polynomials for Y>=1.

In a dyadic range T<=M(g)<2T, with T<=O_n(sqrt H), the number of pairs (g,h) when m>0 is

O_n(T^d (H/T²)^m).

Summing gives O_n(H^max(m,d/2)), with an extra log H only when d=2m. For d=1, the dyadic exponent d-2m=5-2n<0, so the result is directly O_n(H^(n-2)). For d>=2, m=n-2d<=n-4 and d/2<=n/4<n-2 for n>=4, so even a possible logarithm is absorbed below H^(n-2). When m=0, h=1 and the count is O_n(H^(d/2)), also sufficient. There are finitely many d. Overcounting f by several g is harmless for an upper bound. The order is sharp: f=X²h supplies (2H+1)^(n-2) examples. Thus P(Z) is of order H^-2. For n>4, a conjectural H^(-n/2+epsilon) upper bound cannot hold for the square-discriminant event if zero is included and epsilon<n/2-2; the nonzero qualification is essential at that finer scale. This argument uses Mahler measure, NOT false multiplicativity of coefficient height.

**Why this attempt stops:** it identifies exactly the residual requiring new input, but every known bound used still permits P(A) comparable to H^-1. It does not improve that bound.

## Attempt 2: exact local parity sieve

For an odd prime p and n>=2, among the p^n monic degree n polynomials over F_p, the number whose discriminant is a square or zero is exactly

(p^n+p^(n-1))/2.

Proof: there are p^n-p^(n-1) squarefree polynomials. For squarefree f with r irreducible factors, Frobenius has sign (-1)^(n-r), equal to the quadratic character of the discriminant, and equal to (-1)^n times the polynomial Möbius function. The generating series for the sum of the Möbius function is 1-pu, so its coefficient vanishes in degree n>=2. The nonzero square and nonsquare discriminants therefore split the squarefree polynomials equally. The other p^(n-1) polynomials have zero discriminant.

For a squarefree product M of odd primes define delta(M)=product_(p|M) (p+1)/(2p). By CRT, exactly delta(M) M^n residue vectors survive. Each residue vector has at most (L/M+1)^n representatives in the coefficient box. Consequently

P(Q union Z) <= delta(M)(1+M/L)^n.

This is a completely explicit valid upper bound, and letting H→infinity first and then taking more fixed primes proves density zero. It is far too weak for the desired o(H^-1). Choosing the product of primes up to c log H with fixed 0<c<1 keeps M below H^(c+o(1)) and controls the CRT boundary factor but only yields delta(M)=exp(-O(log H/log log H)), a subpower rather than H^-1 saving. More sophisticated large-sieve estimates improve this, but the classical resulting H^-1/2 scale remains weaker than Bhargava's H^-1 scale.

**Failed inference identified:** finite-field independence is exact only after CRT at a controlled total modulus. One cannot multiply arbitrarily many one-half probabilities while ignoring the box boundary or treating coefficients modulo an enormous modulus as uniform. The local identities do not yield a proof of the conjecture.

## Attempt 3: discriminant fibers and determinant-method geometry

Fix a_1,...,a_(n-1) and put a_n=t. The discriminant D(t) has degree n-1, with leading coefficient (-1)^(n(n-1)/2) n^n. For generic fixed coefficients it is squarefree as a polynomial in t. Thus the smooth curve y²=D(t) has genus floor((n-2)/2). This suggests exploiting high-genus integral-point bounds, but the required average is much stronger than merely a pointwise power saving.

There are O(H^(n-1)) fibers. A uniform bound O(H^(1-delta)) points per fiber produces only O(H^(n-delta)); even O(1) points per fiber produces O(H^(n-1)), not little-o. To prove the target by this slicing one needs an average number of admissible t equal to o(1), or another structural saving across the base. Fiberwise finiteness, with constants depending on the coefficients, gives neither.

Moreover smoothness is not uniform: the slice f=X^n+t has D(t)=(-1)^(n(n-1)/2)n^n t^(n-1). For n an odd square (for example n=25), every t!=0 gives nonzero square discriminant. This is a thin degenerate slice, not a counterexample to the conjecture; it rules out an indiscriminate all-fibers sparsity assertion. The two-parameter resolvent/determinant estimate recorded in the historical literature has count exponent n-2+sqrt(2), still larger than n-1.

**Why this attempt stops:** a family-uniform integral-point estimate plus controlled exceptional fibers is needed. Generic genus or a dimension count for y²=Disc(f) does not supply it. The double cover has the same dimension n as coefficient space, so codimension rhetoric alone is particularly misleading.

## Attempt 4: number-field counting and Bhargava's general group bound

Let F_n(A_n,X)=O(X^a) count degree n fields of alternating normal-closure group by absolute field discriminant. Bhargava's expanded preprint Theorem 2 has, for primitive groups, u=1/(n(n-1)); its second alternative for A_n is

N_n(A_n,H) << H^((2n-2)(a-u)+1) (log H)^(n-1).

For this alternative alone to give a power saving over H^(n-1), one needs

a < (n-2)/(2n-2)+1/(n(n-1)) = 1/2-(n-2)/(2n(n-1)).

Even the conjectural Malle exponent a=1/2+epsilon does not meet that threshold. Its substitution gives exponent n-2/n+(2n-2)epsilon, which exceeds n-1. The other alternative contains H^(n+1-ind(A_n))=H^(n-1), since ind(A_n)=2; improving the accompanying summand does not remove that term. Thus even granting Malle's expected field-count exponent does not, by a mechanical substitution into this theorem, settle the strong next-group assertion.

This is a limitation of the quoted inequality, not a proof that field-counting methods or Malle plus additional arguments can never resolve the problem. Polynomial discriminant differs from field discriminant by an index square, and many generators give the same field; neither multiplicity can be discarded.

**Why this attempt stops:** the bound has a genuine H^(n-1) contribution for index-two groups. New information must reduce that contribution or count generators substantially more sharply, not just update an older general field-count exponent.

## Attempt 5: structured square families and potential counterexamples

For monic degree m g with g(0)!=0 and g separable, the exact composition identity is

Disc(g(X²)) = (-1)^m 4^m g(0) Disc(g)^2.

Proof: write g(Y)=product_i(Y-beta_i), so g(X²)=product_i(X²-beta_i). Each quadratic has discriminant 4 beta_i; the resultant of X²-beta_i and X²-beta_j is (beta_i-beta_j)². The product discriminant formula gives 4^m(product beta_i) product_(i<j)(beta_i-beta_j)^4, which is the displayed expression since product beta_i=(-1)^m g(0).

Thus the square condition is (-1)^m g(0) a square, not g(0) a square for every m. The source introduction's abbreviated assertion misses this sign for odd m; its Proposition 3.1 correctly uses constant term (-1)^m B_0². This is a local sign correction, not a defect in its stated lower-bound order.

For m>=2, choosing m-1 coefficients freely in a fixed box and g(0)=(-1)^m s² with 1<=s<=sqrt H yields order H^(m-1/2) distinct compositions; separable ones retain this order. To see the latter directly, for every fixed nonzero constant the discriminant is a nonzero polynomial in the other coefficients (specialize to Y^m+c), so its zero set contains O_m(H^(m-2)) coefficient vectors. Summing over s gives only O(H^(m-3/2)) bad vectors. The ambient probability is therefore of order H^(-(n+1)/2) for n=2m.

Every such Galois group preserves the pairs {alpha,-alpha}. For n>=6 it cannot be A_n, which is primitive in its standard action. The family gives many square discriminants but does not lower-bound the A_n event. Generic full group within the even wreath subgroup is established in the cited source, but is unnecessary for this elementary distinction.

The source's separate derivative-square constructions do produce A_n families, but their proven lower bounds are far below H^(n-1), hence do not contradict strong dominance. Lines of A_n polynomials likewise provide constructive abundance, not the ambient upper bound. No family at order H^(n-1) was found here.

**Why this attempt stops:** examples reveal why the naive random-integer heuristic for discriminant squares is unreliable, but neither exhibit a competing leading term nor establish the needed upper bound.

## Final assessment

Five routes yield exact reductions, elementary degeneracy control, a corrected sign identity, explicit local counts, and a precise barrier in a tempting conditional number-field argument. None proves P(A_n)=o(H^-1). The original fixed-n problem remains open within this investigation; no solved status or novel theorem priority should be claimed. The n→infinity {0,1} Odlyzko–Poonen model is not used anywhere in these proofs.

## Bibliographic links

- Bhargava expanded Theorem 2: https://arxiv.org/abs/2111.06507 ; journal record: https://annals.math.princeton.edu/2025/201-2/p01 .
- Bary-Soroker–Ben-Porath–Matei, residual formula and constructions: https://doi.org/10.1112/blms.13049 ; inspected preprint: https://arxiv.org/abs/2207.12493 .
- Arala, constructive alternating lines: https://arxiv.org/abs/2205.01502 .
- See SOURCE_PRIORITY_AUDIT.md for dates, inspection scope, and current-literature limitations.

## Verification

The independently checked core reduction, repeated-factor estimate, and composition sign are detailed in the separate independent audit. verify_identities.py exactly enumerates monic degrees 2–4 over F_3 and F_5 and checks six characteristic-zero composition examples. IDENTITY_CHECKS.json records successful matches. These finite checks supplement, but do not replace, the general proofs or imply the unresolved asymptotic.
