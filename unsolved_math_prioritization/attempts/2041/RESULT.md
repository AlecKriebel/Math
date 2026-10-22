# EP-312 / problem 2041: partial reciprocal-multiset approximation results

## Publication and review scope

This is an unrefereed AI-assisted prose-only edition. “Accepted” means an independent internal AI audit of the explicitly stated partial result; no external human peer review, journal acceptance, or formal proof-assistant certification is claimed. The complete substantive candidate proof and independent mathematical audit are retained. No mathematical correction was required. Historical finite tests are described for context; their programs, detailed receipts, and certificate contents are not distributed, and this edition is not an executable reproduction package. Publication preparation did not rerun those mathematical tests or newly inspect scholarly sources.

## Disposition

**PARTIAL. The universal exponential approximation conjecture is not resolved.** This attempt proves a same-constant equivalence removing the sufficiently-large-cardinality qualification, gives an exact logarithmic-mass formulation of the missing estimate (up to absolute constants), proves the desired kind of estimate when occurrence multiplicities are bounded, and gives a rigorous upper restriction on any possible universal exponential constant. The remaining step is stated explicitly below. No finite computation is used as evidence of a universal theorem.

The target is the existence of one constant c>0 such that, for every K>1, every sufficiently large finite occurrence-multiset A of positive integers with

    R(A) = sum_{a in A} 1/a > K

has an occurrence-submultiset S with

    1 - exp(-c K) < R(S) <= 1.

The cardinality threshold may depend on K. Equal denominators are separate selectable occurrences. Exact sum 1 is a successful outcome.

Write

    epsilon(A) = 1 - max { R(S) : S is an occurrence-submultiset of A,
                                      R(S) <= 1 }.

All maxima exist because A is finite; the empty submultiset is allowed.

## Sources and attribution

The original source is P. Erdős and R. L. Graham, *Old and new problems and results in combinatorial number theory* (1980), printed p. 40, PDF page 36, https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf . Its displayed question was visually inspected. It records the older polynomial error bound.

A directly relevant later source is Samuel Korsky, *A Stretched-Exponential Bound for an Erdős–Graham Unit-Fraction Problem*, arXiv:2607.04157v1, https://arxiv.org/abs/2607.04157 . The manuscript claims the bound epsilon(A)<=exp(-c sqrt(K log K)) for arbitrary multisets and sufficiently large K. That claim is weaker than the present target. It is recorded as a manuscript claim, not as an independently accepted theorem in this attempt. The PDF and HTML have different displayed dates and are not silently treated as identical versions. The deterministic optimal-complement and divisibility-compression reductions below also appear in that work; no novelty is claimed for them. None of this report's proved conclusions depends on its analytic claims.

The elementary statements below have complete proofs here. They are authored deductions for this attempt, not claims of literature priority.

## 1. Padding lemma

**Lemma 1.** If A and T are finite multisets and R(T)<=eta, then

    epsilon(A union T) >= epsilon(A) - eta.

Here union means disjoint occurrence union, even if denominators coincide.

**Proof.** If U is a submultiset of A union T with R(U)<=1, write U=U_A union U_T by occurrence labels. Positivity gives R(U_A)<=1, so R(U_A)<=1-epsilon(A). Therefore R(U)<=1-epsilon(A)+eta. Taking the maximum proves the assertion. This argument also covers a negative right side. QED.

For any eta>0 and any desired cardinality t, one can take t copies of an integer D>t/eta. Then R(T)=t/D<eta. Thus arbitrarily large cardinality need not add significant reciprocal mass.

## 2. The cardinality threshold is removable, with the same constant

**Theorem 2.** For a fixed c>0, the target statement with its K-dependent cardinality thresholds is equivalent to the following assertion:

    epsilon(A) <= exp(-c R(A))

for every finite multiset A with R(A)>1.

**Proof, target implies uniform assertion.** Fix such an A and any K with 1<K<R(A). If epsilon(A)>exp(-cK), choose eta strictly between 0 and epsilon(A)-exp(-cK). Append arbitrarily many occurrences with total reciprocal mass below eta. Their union A' still has mass greater than K and can exceed the target's cardinality threshold. Lemma 1 gives epsilon(A')>exp(-cK), contradicting the target. Consequently epsilon(A)<=exp(-cK) for every 1<K<R(A). Let K increase to R(A); continuity gives the displayed uniform assertion.

**Proof, converse.** If R(A)>K>1, the uniform assertion gives

    epsilon(A) <= exp(-c R(A)) < exp(-cK).

This is the required strict inequality, for every cardinality. QED.

The non-strict inequality at R(A), the strict inequality at K, and the strict mass hypothesis are all used as written. A boundary equality for one finite A is not a counterexample to the target.

## 3. Optimal complement and exact compression

**Lemma 3.** Suppose epsilon(A)=delta>0 and R(A)>1. Choose an optimal S, so R(S)=1-delta, and put B=A minus S by occurrences. Then:

1. Every denominator n in B satisfies n<1/delta.
2. R(B)=R(A)-1+delta>R(A)-1.
3. Every submultiset of B avoids the interval (1-delta,1].
4. delta<=1/2.

**Proof.** If an unused n had 1/n<=delta, adding that occurrence to S would improve its mass without exceeding 1, a contradiction. This proves 1. Statement 2 is the disjoint-union identity. Statement 3 follows because a submultiset of B is also one of A. For 4, a denominator 1 would already give delta=0, so every occurrence weight is at most 1/2. Since the total mass exceeds 1, follow any occurrence ordering until the partial sum first reaches 1/2. The previous sum was less than 1/2, hence this partial sum is at least 1/2 and less than 1. Thus the optimal mass is at least 1/2. QED.

Starting from B, whenever a prime p divides n and at least p formal occurrences of n are present, replace p of them by one formal occurrence of n/p. Label every formal item by its disjoint bundle of original B occurrences.

**Lemma 4.** This process terminates. The resulting multiset C has the same mass as B; every submultiset of C lifts to an occurrence-submultiset of B with identical mass; all its denominators are less than 1/delta; it has no denominator 1; and its multiplicities satisfy

    m_C(n) < least_prime_factor(n)  for n>1.

**Proof.** Each replacement preserves reciprocal mass because p/n=1/(n/p), and replaces disjoint bundles by their union. This maintains the lifting property and disjointness. Every replacement strictly lowers the finite number of formal items, proving termination. Every new denominator divides an old one, so the upper denominator bound is preserved. A denominator 1 would lift to an exact unit sum, impossible when delta>0. At termination no prime divisor p of n has p copies available, which gives the stated inequality. QED.

Call this final multiplicity property **stable**. No uniqueness of the terminal multiset is assumed or needed.

## 4. The exact logarithmic-mass obstacle

For N>2, consider a stable finite multiset C of integers 2<=n<N satisfying

    no submultiset of C has reciprocal mass in (1-1/N,1].          (G_N)

The right endpoint is included; merely forbidding exact sum 1 is much weaker.

Consider the following assertion:

    There is an absolute C0>0 such that every such C satisfies
    R(C) <= C0 log N.                                           (L)

**Theorem 5.** Existence of a target constant c>0 is equivalent to existence of a constant C0 in (L), allowing an absolute change of constants.

**Proof, target implies (L).** By Theorem 2, epsilon(C)<=exp(-c R(C)) whenever R(C)>1. Condition (G_N) says epsilon(C)>=1/N. Hence R(C)<=log N/c. If R(C)<=1, then R(C)<=log N/log 2 because N>2. Thus (L) holds with C0=max{1/c,1/log 2}.

**Proof, (L) implies target.** For an arbitrary A with R(A)>1 and delta=epsilon(A)>0, form the compressed optimal complement C from Lemmas 3–4. With N=1/delta, one has N>=2; in fact N>2 whenever B is nonempty, since its integer denominators satisfy 2<=n<N. Here B is nonempty because R(A)>1. The lifting property gives (G_N). Thus

    R(A) = 1-delta+R(C) < 1+C0 log(1/delta).

Put x=log(1/delta). Lemma 3 gives x>=log 2, and so

    R(A) < 1+C0 x <= (C0+1/log 2) x.

Therefore

    delta < exp[-R(A)/(C0+1/log 2)].

The exact-unit case delta=0 is immediate. Theorem 2, or directly R(A)>K, now gives the target with c=1/(C0+1/log 2). QED.

This is the substantive reduction reached by the attempt. **Assertion (L) remains unproved here.** It retains arbitrary stable multiplicities and the one-sided interval around 1; it does not replace the target by distinct denominators or by exact unit-fraction representation.

## 5. A fully proved bounded-multiplicity case

**Theorem 6.** Fix an integer M>=1. Every finite multiset A with at most M occurrences of each denominator and R(A)>K>1 has a submultiset S satisfying the target estimate with

    c_M = 1/(M+1/log 2).

No sufficiently-large-cardinality condition is needed.

**Proof.** If epsilon(A)=0 there is nothing to prove. Otherwise use the optimal complement B, without any compression. Put delta=epsilon(A), N=1/delta and J=ceil(N)-1. Its multiplicities remain at most M. Since its denominators lie between 2 and J,

    R(B) <= M sum_{n=2}^J 1/n <= M log J < M log N.

The middle inequality follows termwise from 1/n<=integral_{n-1}^n dx/x. For J=1 the sum is empty; in the present case B is nonempty and J>=2. Consequently R(A)<1+M log(1/delta). Apply x>=log 2 exactly as in Theorem 5 to obtain

    epsilon(A) < exp(-c_M R(A)) < exp(-c_M K).

An optimal S witnesses the result. QED.

This includes the distinct-denominator case M=1. It does not solve the multiset conjecture: c_M tends to zero as M tends to infinity. Compressing does not fix that loss because a prime denominator p may retain p-1 occurrences. This dependence is the essential unresolved issue in this route.

## 6. A rigorous upper restriction on the universal constant

Let A0 consist of one 2, two 3s, and four 5s. Then

    R(A0)=1/2+2/3+4/5=59/30,
    epsilon(A0)=1/15.

Here is a proof not depending on enumeration. Every submultiset mass has the form

    (15a+10b+6d)/30,
    0<=a<=1, 0<=b<=2, 0<=d<=4,

with integer coefficients. The numerator 28 occurs with (a,b,d)=(0,1,3). Numerator 29 is impossible: modulo 2 it forces a=1; then 5b+3d=7, and b=0,1,2 gives respectively d=7/3,2/3,-1. Numerator 30 is also impossible: parity gives a=0, and 5b+3d=15 forces b=0 by reduction modulo 3, followed by d=5, outside the range. Hence 28 is the largest numerator at most 30, proving the deficit.

**Corollary 7.** Every constant c satisfying the original target must obey

    c <= (30/59) log 15 = 1.3769746785265475... .

**Proof.** Apply Theorem 2 to A0: 1/15<=exp(-59c/30). Taking logarithms gives the bound. Equivalently, for any larger c choose log(15)/c<K<59/30 with K>1, and append arbitrarily many tiny reciprocal occurrences whose total is less than 1/15-exp(-cK). Lemma 1 then gives arbitrarily large counterexamples to that particular c. QED.

For a fully explicit illustration, append t copies of 300t to A0. For every integer t>=1 the resulting multiset has mass 197/100 and deficit 19/300: the old best submultiset together with all appended occurrences attains this, and Lemma 1 gives the matching lower bound. It violates c=3/2 at K=19/10, because exp(57/20)>300/19. The latter comparison follows, for example, from the positive Taylor polynomial through degree 12, using exact rational arithmetic. This is an unbounded-cardinality counterexample to that particular constant.

This rules out only constants larger than the displayed number. It is **not** a counterexample to the existence of some positive c. No optimality of this upper restriction is claimed.

## 7. Why the attempted merging/iteration does not close (L)

Three potential continuations were examined.

1. **Harmonic counting after compression.** It only gives

       R(C) <= sum_{2<=n<N} (least_prime_factor(n)-1)/n.

   Its prime terms are (p-1)/p. There is no uniform bound on the remaining multiplicities, and this envelope alone does not give the required C0 log N estimate. Interval avoidance (G_N), rather than stability alone, must do substantial additional work.

2. **Repeatedly fill the remaining gap.** At an optimal S every unused single reciprocal is larger than delta. Every nonempty positive block of unused occurrences is therefore larger than delta too. Thus no positive filling step can improve S. A proof needs controlled exchanges that remove selected occurrences as well as add unused ones, or a different global argument. A sequence of independently found near-unit blocks does not combine into a legal submultiset near 1.

3. **Use a very small residue modulo 1 and reduce it into (0,1].** Reduction modulo 1 is not a legal operation on an occurrence-submultiset. In A0 the unique allowed coefficients giving numerator congruent to 29 modulo 30 are (a,b,d)=(1,2,4), whose actual mass is 59/30, near 2 rather than below 1. Uniqueness follows by reducing the numerator successively modulo 2, 3, and 5. There is no submultiset of mass 29/30. Likewise the signed difference (1/2+1/3)-4/5=1/30 does not make 1/30 an available positive block. This exact example blocks the proposed residue-to-unit and signed-to-unsigned shortcuts.

None of these observations disproves (L). They identify precisely why the current elementary approach stops. A successful continuation must bound the mass of the *gap-avoiding* stable configurations logarithmically, without discarding the positivity, capacity, or target-level constraints.

## 8. Historically recorded finite verification and scope

The historically recorded exact search explored all stable multiplicity choices on denominators 2 through 12, pruning branches as soon as exact mass 1 occurs. It used an integer subset-sum bitset with common denominator lcm(2,...,12)=27720. It found 135828 terminal configurations with no exact unit subsum, including configurations of mass at most 1, and 674 distinct positive deficits among those with mass above 1. Its ranked ratios are exploratory floating-point output, not proof certificates for the order of arbitrary transcendental expressions. The useful A0 conclusion has the separate hand proof above.

A separate historically recorded verification used a different direct coefficient-product enumeration to check the recorded leading configurations, all occurrence subsets of A0, a separate Fraction-based exhaustive comparison on stable denominators 2 through 8, occurrence-bundle lifting for sample compressions, and exact padding examples. These were local reproduction checks of finite calculations and implementations. The omitted programs and detailed outputs are not part of this prose-only edition. The proofs of Theorems 2, 5, and 6 are the arguments in this document, not conclusions extrapolated from those tests.

There is no claim that this finite denominator range covers all A or K, no claimed optimal universal c, and no claim of complete literature coverage.
