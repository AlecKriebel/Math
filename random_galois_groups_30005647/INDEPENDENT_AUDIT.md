# Independent audit: the alternating-group obstruction

Audit date: 2026-10-21. Fixed-degree centered monic integer coefficient box. This report verifies a reduction, not a solution of the next-group conjecture.

## Verdict

**PASS**, with the scope and conventions below. For every fixed n >= 10, the probability of nonzero square discriminant and the probability of irreducible square discriminant each differ from the probability of the full natural alternating group A_n by O_n(H^-2). All three therefore have equivalent o(H^-1) assertions. These estimates do not establish any of those assertions, nor do they establish relative asymptotic equivalence between those three probabilities.

## Source verification

Bary-Soroker, Ben-Porath and Matei, *Probabilistic Galois Theory – The Square Discriminant Case*, arXiv:2207.12493v2, 1 April 2024:

https://arxiv.org/pdf/2207.12493v2

The introduction on printed p. 2 explicitly records the decomposition into the standard point stabilizer and A_n with an O(H^-2) error for n >= 10, and explicitly requires a modified error for smaller degrees. Its preceding discussion identifies the point stabilizer with a rational root and a full symmetric quotient, and gives its positive c_n/H asymptotic for n > 2. The discussion on printed p. 4 explicitly confirms that its model is monic. The relevant source was inspected independently through the primary PDF and local text extraction.

Bhargava, *Galois groups of random integer polynomials and van der Waerden's Conjecture*, expanded arXiv:2111.06507v3:

https://arxiv.org/abs/2111.06507v3

Its definition of N_n(G,H) explicitly uses monic degree-n polynomials with |a_i| <= H and permutation-group isomorphism. Corollary 3(a) confirms O(H^(n-2)) for primitive groups other than S_n and A_n when n >= 10. The square-discriminant paper supplies the directly stated full decomposition; one should not misidentify that decomposition with Bhargava's weaker overall exceptional order bound alone.

## Exact event argument

Let Omega_H contain all (2H+1)^n monic polynomials, including reducible and nonseparable polynomials. Define S, T, and A only on separable polynomials, respectively by natural root permutation groups S_n, a conjugate of the standard point stabilizer S_(n-1), and A_n. Set E=Omega_H minus S. Let Q mean discriminant a nonzero integer square, and I=Q intersect the irreducible polynomials.

For separable f, write its Vandermonde product as delta=product_(i<j)(alpha_i-alpha_j). Then delta^2=disc(f), and every Galois automorphism sends delta to its permutation sign times delta. Thus disc(f) is a nonzero rational square exactly when G_f is contained in A_n. An integer that is a rational square is an integer square. The equivalence holds also for reducible separable f; it does not say that G_f equals A_n.

For n >= 3, the standard point stabilizer contains odd permutations. Consequently A is contained in I, which is contained in Q, which is contained in E minus T. Here A is contained in I because the natural action of A_n is transitive. Events T and A are disjoint. Therefore

0 <= P(Q)-P(A) <= P(E)-P(T)-P(A),

and the same inequality holds with I in place of Q. The published decomposition bounds the nonnegative right side by O_n(H^-2). The treatment of nonseparable polynomials can alter its conventions only within that same error, by the count proved below.

Since P(T) is asymptotic to a positive c_n/H,

P(T)/P(E) -> 1

is equivalent to P(A)=o(H^-1), and hence equivalent to P(Q)=o(H^-1) or P(I)=o(H^-1). For the converse direction, positivity avoids cancellation: P(E)-P(T)=P(A)+P(E minus (T union A)).

These are unconditional probabilities in the original box. Conditioning on irreducibility deletes T and is a different next-group question. The event I is an intersection, not a conditional probability.

## Independent proof of the nonseparable count

For every fixed n >= 3, the number of monic integer f of degree n and coefficient height at most H that are nonseparable is O_n(H^(n-2)).

Use Mahler measure M. For a monic polynomial p of degree k, M(p)>=1; every coefficient has absolute value at most binomial(k,j) M(p), and M(p) is at most the Euclidean norm of its coefficient vector. The latter follows from Jensen's formula, the geometric/arithmetic mean inequality on the unit circle, and Parseval. Thus M(f)<=sqrt(n+1)H for H>=1. Mahler measure is multiplicative, unlike naive coefficient height.

A nonseparable monic f in Z[x] has a repeated monic irreducible factor g in Z[x]. Write f=g^2 h, with deg g=d>=1 and deg h=m=n-2d>=0. Gauss's lemma ensures h is monic integral. Overcounting all such pairs is legitimate. Multiplicativity gives M(g)^2 M(h)<=C_n H.

For a dyadic shell T<=M(g)<2T, T=1,2,4,..., there are O_n(T^d) possibilities for g, by the coefficient bounds. Necessarily T<=sqrt(C_n H). For m>=1 there are O_n((H/T^2)^m) possibilities for h; constants may absorb the fixed C_n and the range where H/T^2 is bounded below by a positive constant. Hence the shell contributes

O_n(H^m T^(d-2m)).

Summing dyadically gives O_n(H^max(m,d/2)), except when d=2m, where the bound is O_n(H^m log(2H)). If m=0, h=1 and the direct bound is O_n(H^(d/2)).

For d=1 and n>=3, m=n-2 and d-2m=5-2n<0. The shell sum is O_n(H^(n-2)) without a logarithm. For d>=2, m<=n-4 and d/2<=n/4<n-2 for n>=4. Both endpoint exponents are strictly below n-2, so any logarithm is absorbed. This proves the claim. The bound is sharp in order: f=x^2 h already gives (2H+1)^(n-2) examples.

Degree 2 is excluded: (x-a)^2 with |a|<=sqrt(H) provides order sqrt(H) nonseparable polynomials, not O(1). This is distinct from the logarithmic reducibility phenomenon for degree 2.

After dividing by (2H+1)^n, the nonseparable probability is O_n(H^-2). Thus allowing zero as a square changes Q by at most O_n(H^-2). For fine relative square-discriminant asymptotics this modification can matter substantially, so nonzero must remain explicit in the principal event.

## Limitations and acceptance conditions

- Keep n fixed and n>=10 whenever the displayed residual O(H^-2) is used.
- Use natural permutation groups up to conjugacy, not abstract isomorphism alone.
- Do not assert square discriminant implies full A_n; proper alternating subgroups remain possible.
- An additive O(H^-2) difference does not imply P(Q) is asymptotic to P(A), because no lower bound dominating H^-2 is established here.
- Do not advertise the reduction or the elementary nonseparable count as a resolution of the original asymptotic conjecture, or as a new result without a separate novelty investigation.
- No repository, queue, or external publication was modified during this audit.

## Additional composition-sign check

Let g be monic degree m, separable, with g(0) nonzero, and f(x)=g(x^2). Then f is separable of degree 2m. Since f'(x)=2x g'(x^2), multiplicativity of the resultant gives

Res(f,f')=2^(2m) Res(f,x) Res(f,g'(x^2))
          =4^m g(0) Res(g,g')^2
          =4^m g(0) disc(g)^2.

The identity Res(f,x)=f(0) uses the even degree of f. Evaluating g'(x^2) at both square roots of each root of g gives the squared resultant. Finally the discriminant/resultant sign for degree 2m is (-1)^(m(2m-1))=(-1)^m. Therefore

disc(g(x^2))=(-1)^m 4^m g(0) disc(g)^2.

In particular, its discriminant is a nonzero square exactly when (-1)^m g(0) is a nonzero square. The sign cannot be omitted for odd m: g(x)=x-a gives f=x^2-a and disc(f)=4a. This independently verifies the proposed sign correction. It does not refute the lower-bound theorem: the signed constant-term choice produces the intended family and the centered box is symmetric under that sign change.

## Final five-route review

The full FIVE_APPROACHES.md and SOURCE_PRIORITY_AUDIT.md were reviewed. Additional mathematical checks pass:

1. Over F_p for odd p and degree n>=2, the polynomial Mobius generating function is the reciprocal of 1/(1-pu), hence 1-pu. Its degree-n coefficient is zero. On squarefree polynomials the discriminant character is (-1)^n times Mobius, giving equal counts (p^n-p^(n-1))/2 of square and nonsquare nonzero discriminants. Adding the p^(n-1) repeated-root polynomials proves the claimed (p^n+p^(n-1))/2 count, even when p divides n.

2. The CRT bound is valid for the unconditional coefficient box: each residue vector has at most (L/M+1)^n lifts, and delta(M)M^n vectors meet the local necessary condition. An integer nonzero square can reduce to zero, so allowing zero locally is necessary. Taking a prime product up to c log H with fixed 0<c<1 controls the boundary factor; its local survival density decays only subpolynomially. No unsupported independence beyond CRT is used.

3. The discriminant's leading coefficient in the constant-term fiber is (-1)^(n(n-1)/2)n^n. Generic distinct critical values make the degree-(n-1) polynomial squarefree and give genus floor((n-2)/2). The x^25+t counterexample to uniform fiber sparsity is valid: its discriminant is the square 25^25 t^24. The fiber-count obstruction is accurately stated as a limitation of this slicing argument, not an impossibility theorem for other methods.

4. Direct substitution in the inspected Bhargava Theorem 2 confirms u=1/(n(n-1)) for primitive groups and ind(A_n)=2 in the relevant degree range. Solving (2n-2)(a-u)+1<n-1 gives a<1/2-(n-2)/(2n(n-1)). Substituting a=1/2+epsilon instead gives n-2/n+(2n-2)epsilon>n-1. The first alternative retains its H^(n-1) summand, so neither alternative proves little-o by that substitution alone.

5. The signed-composition counting argument is valid for m>=2; m=1 may be handled separately, because its polynomial g is always separable. For a fixed nonzero constant c, disc(Y^m+...+c), as a polynomial in the m-1 free coefficients, is nonzero by specialization to Y^m+c. A fixed-degree nonzero polynomial has O_m(H^(m-2)) zero lattice points in that box, uniformly in c. Thus the discarded singular compositions are negligible. Pair preservation rules out A_n for n>=6, since its natural action is primitive.

6. The lower bound from x^2 h matches the established upper bound for zero discriminant. Accordingly zero-inclusive square probability cannot have the conjectural upper exponent -n/2+epsilon for n>4 and epsilon<n/2-2. This warns about a convention at a finer scale; it does not contradict the source's full-A_n conjecture.

The exact-check script was independently rerun, and its output matched IDENTITY_CHECKS.json byte for byte. The six finite-field enumerations and six composition examples pass. They are correctly described as supplements, not proofs of asymptotic assertions.

Source-priority review: independently rechecked the Annals journal metadata and distinction between its order-bound result and the strong ratio question; Arala and Larson-Rolen arXiv dates, titles and stated scope; the reciprocal-paper publisher metadata and restricted-family scope. The square-discriminant primary preprint and Proposition 3.1 were inspected. The Wiley DOI page did not load in this audit, so its exact journal acceptance/publication dates remain the author's reported inspection rather than an independently replicated observation here. No proof-completeness or exhaustive-literature claim is warranted, and the documents avoid those claims.
