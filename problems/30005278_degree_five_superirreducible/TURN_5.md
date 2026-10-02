# Turn 5: odd-degree descent removes the integrality gap

Problem 30005278. Fifth and final substantive author turn. **The source existence question remains unresolved, 5/5.** This turn proves that, for a fixed monic irreducible integer polynomial of odd degree, quadratic superirreducibility over integer substitutions is equivalent to the corresponding property over rational substitutions. It therefore removes the additional integral-congruence gap left in Turn 2 for the monic candidate. The remaining affine curve is proved to have points in every completion, while its rational points remain undetermined.

The candidate and the prior ax²+c result remain credited to Du; the composition criterion remains credited to Capelli. The norm, valuation and Chinese remainder arguments below are supplied explicitly, without a historical novelty claim. No statement extending the equivalence to arbitrary nonmonic polynomials is made.

## 1. An odd-degree norm-square congruence lemma

**Lemma.** Let d be odd and let

    F(T,U)=U^d+c_1 T U^(d−1)+...+c_d T^d,
    c_j in Z.

Suppose M,N,S are integers, M nonzero, S²=F(M,N) nonzero. Then N is a square modulo |M|.

**Proof.** Work prime by prime at p^m exactly dividing |M|. If v_p(N)>=m, including N=0, then zero is a square root modulo p^m.

Otherwise set n=v_p(N)<m. The j-th non-leading term of F(M,N) has valuation at least

    jm+(d−j)n = dn+j(m−n) >= dn+(m−n).

The leading term N^d has valuation exactly dn, and all others have larger valuation. Hence

    v_p(S²)=dn.

Because d is odd, n is even. Write N=p^n N_0 and S=p^(dn/2) S_0, with N_0,S_0 p-adic units. Dividing the norm identity by p^(dn) gives

    S_0² == N_0^d (mod p^(m−n)).

The inverse of N_0 exists modulo that modulus. Set

    y == S_0 N_0^(−(d−1)/2) (mod p^(m−n)).

Then y²==N_0 modulo p^(m−n), so r_p=p^(n/2)y satisfies r_p²==N modulo p^m. This argument works also for p=2; it uses only unit inverses and the parity of n, not a division by two modulo p. The Chinese remainder theorem combines the r_p to an integer r with r²==N modulo |M|. The cases |M|=1 are automatic. This proves the lemma.

Oddness is essential. For d=2, F(T,U)=U²−2T², M=4 and N=6 give F(M,N)=4, but six is not a square modulo four. Indeed in Q(sqrt(2)), (2+sqrt(2))²=6+4sqrt(2). We do not import the odd-degree conclusion into an even-degree example.

## 2. Converting every rational quadratic counterexample to an integer one

Let f be any **monic irreducible polynomial in Z[X] of odd degree d>=3**, let theta be a root, and let K=Q(theta). Suppose some quadratic polynomial with rational coefficients makes f(g) reducible. By Capelli and the quadratic discriminant criterion, there are z in K and M,N in Q, M nonzero, with

    z²=M theta+N.

Multiply z by a rational integer large enough that the new M,N are integers. The norm

    Norm_K/Q(M theta+N)

is a homogeneous polynomial F(M,N) of exactly the form in Section 1 because f is monic with integer coefficients. Norm(z) is rational and its square is the integer F(M,N), hence Norm(z) is an integer. The norm is nonzero because theta is not rational. The lemma therefore supplies an integer r satisfying r²==N modulo |M|.

Define

    G(x)=M x²+2r x+(r²−N)/M in Z[x].                     (1)

Its leading coefficient is nonzero, and its discriminant over K relative to theta is

    (2r)²−4M[(r²−N)/M−theta]=4(N+M theta)=(2z)².

Thus G(x)−theta splits over K and f(G) is reducible over Q. This produces a genuine integer substitution of degree two. It is constructive: clear denominators, compute the integer norm square, factor |M|, use the explicit local residues from Section 1, and combine them by CRT. No efficiency bound is claimed.

Conversely an integer quadratic counterexample is already a rational one. Nonconstant linear substitutions preserve the irreducibility of f in either field of coefficients. We have proved:

**Theorem.** For a fixed monic irreducible f in Z[X] of odd degree, f is 2-superirreducible under integer substitutions if and only if it is 2-superirreducible under rational substitutions, where the compositions are tested in Q[x] and the substitutions have positive degree at most two.

The source allows nonmonic polynomials as well. This theorem applies to the monic candidate and to the stated monic class; it is not a proof that all source candidates can be assumed monic without loss.

## 3. What this closes, and what it does not

Turn 2 retained the congruence N square modulo M as an extra requirement after clearing a global square-root witness. Section 1 proves that this requirement follows automatically from the odd-degree norm-square identity. Thus it is no longer an unresolved step for this monic quintic. The frozen earlier turn is preserved as a historical intermediate result; this theorem closes its stated integrality gap.

For f=X^5+2X+1, write R(s,t) for the exact plane polynomial in Turn 2. That turn proves a bijection between rational points of R=0 and nonconstant linear-square witnesses in K, modulo scaling of the square root. The present theorem now gives the exact equivalence

    f is 2-superirreducible over integer substitutions
       <=> R(s,t)=0 has no rational point.                 (2)

A rational point would construct an integer quadratic counterexample by (1). A proof that there is no rational point would prove this candidate solves the source existence question. **Neither conclusion has been established here.** An equivalent explicit curve is not being presented as a solution.

The integer norm-square condition by itself is still insufficient: Turn 3 gives globally irreducible compositions having square norm. The new lemma only removes an integrality obstruction after a genuine root-field square witness exists; it does not create that witness.

## 4. The remaining curve has points over every completion

There is no missing single-place point obstruction for R. More precisely, it has a point over R and over every Q_p, lying in the nonzero-coordinate, nonzero-denominator part used in Turn 2.

To prove this, work in the five-dimensional algebra

    B_v=Q_v[X]/(f)

for v=p, or R[X]/(f) at the real place. For a sufficiently small nonzero parameter u in Q_v or R, the convergent power series

    z(u)=(1+u theta)^(1/2)
        =sum_{n>=0} binom(1/2,n) u^n theta^n

defines an element of B_v satisfying z(u)²=1+u theta. In every p-adic algebra, theta's powers have integral power-basis coefficients. For n>=1 the binomial coefficient is a signed Catalan integer divided by 2^(2n−1). Therefore |u|_p<1 suffices at odd primes, and v_2(u)>=3 suffices at two. At the real place choose u small relative to any fixed submultiplicative norm on the finite-dimensional algebra. These estimates justify convergence and multiplication of the series.

In the fixed power basis z(u)=sum A_i(u)theta^i, the leading terms are

    A_0=1+O(u^5),             A_1=u/2+O(u^5),
    A_2=−u²/8+O(u^5),         A_3=u³/16+O(u^5),
    A_4=−5u^4/128+O(u^5).

The coefficient functions are convergent analytic power series, with these nonzero leading terms over every characteristic-zero completion. For u sufficiently small and nonzero all five coordinates are nonzero. Moreover

    A_2 A_4−A_3²=u^6/1024+O(u^7),                         (3)

so it too is nonzero for a sufficiently small choice. Normalize A_4 to one and put s=A_3/A_4, t=A_2/A_4. Equation (3) ensures t−s² is nonzero, and the coefficient equations from z(u)²=1+u theta then give R(s,t)=0 exactly, by Turn 2's elimination identity.

Thus all completions have points in the relevant open part of the curve. This does not produce rational coefficient functions at a rational u, nor a rational point of R. In particular the algebra B_v need not be a field, and a square in all local algebras is not being identified with a square for some fixed global linear element. The parameter u may be chosen separately at each place. The result only rules out an argument based on absence of points in a single completion; it does not rule out more refined global or adelic obstructions.

## 5. Final honest assessment

Across five author turns the packet has established the exact dyadic obstruction and its exhaustion, global sparsity restrictions and an exact residual curve, the precise finite-prime certificate boundary, three new global discriminant-band irreducibility classes, and odd-degree descent removing the monic candidate's integrality gap. Standard prior inputs and Du's original family are credited throughout.

The decisive global rational-point question in (2) is still open in this packet. The finite projective box in Turn 2 is not a complete rational-point computation. The all-completions statement does not imply a rational point. No new degree-five 2-superirreducible polynomial or integer quadratic counterexample to this candidate has been certified.

Recommend **unsolved, 5/5**, after a full independent source/proof review. The five-turn author budget is exhausted; no sixth author search is planned. Subjective completion estimate toward the original existence question: 22%.

The exact checker tests the norm/CRT descent on bounded integer norms, including noncoprime cases and p=2, verifies a known odd-degree square-root construction, checks the even-degree limitation, and confirms the formal square-root leading terms and denominator identity. These are reproducibility controls for the written proofs, not a rational-point solution.
