# Positive three term radical blocks

## Result and scope

This AI-assisted, unrefereed edition records an independent internal AI audit. Acceptance is an internal mathematical assessment, not external human peer review or formal proof-assistant certification. The complete authored elementary proof and Pell/BHV completeness derivation are retained. BHV is an explicitly imported established theorem; its proof and original computations are not reproduced or independently audited here. The exact 41-smooth enumeration is a computation-dependent result supported by historical independent verification. This edition omits the 141-start inventory, raw certificates, programs and raw datasets, so it is not a self-contained computational reproduction package. Hashes authenticate bytes, not mathematical truth. Source retrieval and inspection described here occurred in the preceding candidate and audit on 11 October 2026; this editorial preparation performed no new scholarly-source retrieval, inspection or mathematical computation.

The full EP 850 / upstream 2339 question is not resolved here. No counterexample was found and no unconditional proof for arbitrary prime supports is claimed.

This packet gives two separate unconditional partial results.

1. **Elementary theorem.** The positive integers n for which n(n+1)(n+2) has at most three distinct prime divisors are exactly

   1, 2, 3, 4, 6, 7, 8, 16.

   Consequently, a pair of distinct positive three-term blocks with positionwise equal radicals must have at least four primes in its common union of supports.
2. **Imported-theorem computational theorem.** If all prime divisors of n(n+1)(n+2) are at most 41, there are exactly 141 possible positive starts n. Their largest member is 212380. In every case

   rad(n(n+1)(n+2)) >= 3n.

   Consequently, no pair in the target can have its common union of supports contained in the primes at most 41, regardless of the sizes of its starting integers. The completeness bridge uses the established Bilu–Hanrot–Voutier primitive-divisor theorem, classical continued fractions, and the exact certificate and independently written checking program verified during the preceding work, but omitted from this prose-only edition. It does not assume abc.

These are independently derived and checked results for this attempt, not novelty claims. The finite-prime-set method is classical Størmer/Pell theory; the published primitive-divisor result is explicitly imported. The subsequent independent audit in AUDIT.md accepted both partial results without a mathematical correction. The original frozen candidate predates that audit; this edition updates only that historical acceptance wording and the stated distribution boundary.

## The target and source boundaries

For a positive integer m, rad(m) is the product of its distinct prime divisors; rad(1)=1. The exact target is whether positive integers a<b can satisfy

rad(a+i)=rad(b+i) for i=0,1,2.                                      (1)

Equality is positionwise. Equality of the radicals of the two whole products alone is a different condition. Length two is different, as is any extension to zero or negative integers.

The authenticated source is Shorey and Tijdeman, *Arithmetic properties of blocks of consecutive integers*, arXiv:1612.05438v1, https://arxiv.org/abs/1612.05438. The Erdős–Woods discussion is in **Section 7, PDF page 8**. Section 9, PDF page 13, states Theorem 9.1 for exactly the positive three-term target. It assumes Baker's explicit abc conjecture and uses the consequence c < rad(abc)^(7/4). Ordinary abc only gives finiteness of possible exceptions. The relevant statement and the entire short proof on page 13 were inspected in text and in the page image. No unconditional result is obtained by dropping their stated hypothesis.

The finite-prime-set argument below imports Bilu, Hanrot and Voutier, *Existence of primitive divisors of Lucas and Lehmer numbers*, J. reine angew. Math. 539 (2001), 75–122, DOI https://doi.org/10.1515/crll.2001.080. The author-uploaded manuscript's Section 1 definitions and Theorem 1.4 were inspected; it is a 36-page manuscript, not the 48-page journal pagination. The imported theorem is not reproved here, and its original large computation was not rerun. The exact theorem used and every exceptional index needed in this application are spelled out below. See SOURCES.json for retrieval limits and inspection details.

## A necessary radical bound and an exact reformulation

Write d=b-a and R=rad(b(b+1)(b+2)). If (1) holds, any prime p dividing b+i also divides a+i, hence divides d. Since R is squarefree,

R | d, and therefore R <= d < b.                                  (2)

This observation is already in the proof of Shorey–Tijdeman Theorem 9.1; it is not presented as a new lemma. In particular, 6|R and 6|d.

Here is a useful exact formulation. For fixed positive d, call an integer S(d)-smooth if all its prime divisors divide d. Then (1), with b=a+d, is equivalent to all six integers a,a+1,a+2,a+d,a+d+1,a+d+2 being S(d)-smooth.

The forward implication follows from the preceding prime-divisibility argument. Conversely, let a prime p divide one of a+i or a+d+i. By smoothness p|d, so the congruence of the two integers modulo p makes p divide the other as well. This works at each position separately and proves the reverse implication. Primes dividing d but none of the six integers are harmless.

A further elementary necessary condition keeps track of exponent growth. For each i, let G_i be the primes whose exponent in b+i exceeds their exponent in a+i. Each G_i is nonempty: all prime supports agree, and otherwise b+i<=a+i. If p belongs to G_i, subtraction gives

v_p(a+i)=v_p(d), and p^(v_p(d)+1) | b+i.                           (3)

The three sets G_0,G_1,G_2 are disjoint. If p belonged to two, p^(v_p(d)+1) would divide a nonzero difference of two positions, whose absolute value is at most 2. But p|d, so this prime power is at least 4. Thus there must be three distinct primes at which increases occur. The next theorem strengthens the weaker resulting support-cardinality obstruction.

## Elementary classification with at most three primes

First solve the elementary auxiliary equation

|2^u-3^v|=1, with u,v positive integers.                            (4)

Its possibilities for (2^u,3^v) are (2,3), (4,3), (8,9).

For 2^u-3^v=1, if u>=3 then reduction modulo 8 would give 3^v=7 modulo 8; the only residues of powers of 3 are 1 and 3. Thus u<=2, and direct substitution gives only (4,3). For 3^v-2^u=1 with u>=3, reduction modulo 8 forces v to be even. Put v=2w. The two positive even integers 3^w-1 and 3^w+1 have product 2^u, so both are powers of 2 and differ by 2. The only such pair is (2,4): dividing their difference by the smaller power of 2 proves this immediately. Hence (2^u,3^v)=(8,9). The remaining cases u=1,2 yield only (2,3). This proves (4) without using Catalan's theorem.

Now suppose n(n+1)(n+2) has at most three distinct prime divisors. It contains both 2 and 3. Write its possible third prime as p; an absent third prime is allowed in the discussion. The cases n=1,2 work and are set aside.

If n>=3 is odd, its endpoints n and n+2 are coprime odd integers greater than 1. They must use the two available odd primes separately, so they are powers of 3 and p in some order. The middle term cannot contain either odd prime and is therefore a power of 2. Consequently a power of 3 is adjacent to a power of 2. By (4), the middle term is 4 or 8, giving n=3 or 7.

Suppose instead n>=4 is even. The middle term is odd and is coprime to both endpoints. If it contained both odd primes, the endpoints would both be powers of 2. The only powers of 2 differing by 2 are 2 and 4, contrary to n>=4. Thus the middle is a power of a single odd prime r. There is at most one odd prime q available to the endpoints; it cannot divide both endpoints because their gcd is 2. At least one endpoint is therefore a pure power 2^u. The other endpoint cannot also be a power of 2. Thus it has the form 2^c q^v, with v>0. Since the block contains a multiple of 3, either r=3 or q=3.

If r=3, the middle is a power of 3 adjacent to a power of 2. Equation (4) gives only the block starting at 8 after the excluded block starting at 2.

If q=3, the pure power of 2 is at least 4, and the endpoint differing from it by 2 has 2-adic valuation exactly 1. Thus c=1 and

|2^(u-1)-3^v|=1.

Equation (4) gives the endpoint pairs (4,6), (6,8), (16,18), hence the starts 4,6,16. These cases exhaust every allocation of at most three primes.

Direct factorization shows that all eight starts obtained really work. In their increasing order the union radicals are

n: 1, 2, 3, 4, 6, 7, 8, 16
R: 6, 6, 30, 30, 42, 42, 30, 102.

Every R exceeds n. If (1) had at most three common primes, its larger start b would be in this list, contradicting (2). Therefore a counterexample needs at least four common primes. This proof is elementary and independent of all Pell computations below.

## Complete finite prime set reduction

This section proves that a finite Pell computation suffices for **all positive sizes** when a finite allowed prime set S is fixed. It does not bound S in the unrestricted problem.

Assume 2 belongs to S, and put P=max(S), Q=product of the primes in S, and K=max(30,P+1). Let t,t+1 be positive S-smooth integers. Write

t(t+1)=D w^2

with D squarefree. Since t^2<t(t+1)<(t+1)^2, D is not 1. All prime divisors of D and w belong to S. With X=2t+1 and Y=2w we obtain

X^2-DY^2=1, X odd, Y positive and S-smooth.                        (5)

Thus D is one of the nontrivial squarefree divisors of Q. No case D=1 is lost.

### Fundamental solutions and normalization

For each such D let x1+y1 sqrt(D)>1 be the smallest positive solution unit of x^2-Dy^2=1 with integer x,y and y>0. This is the fundamental solution in Z[sqrt(D)], not a possibly half-integral fundamental unit of the full ring of integers of the quadratic field.

Every positive solution X+Y sqrt(D) of (5) is a positive integral power of this unit. For completeness, choose k so that

(x1+y1 sqrt(D))^k <= X+Y sqrt(D) < (x1+y1 sqrt(D))^(k+1).

The quotient is again in Z[sqrt(D)] because the inverse fundamental unit is x1-y1 sqrt(D). It has norm 1 and lies in [1,x1+y1 sqrt(D)). If greater than 1, its conjugate is its positive reciprocal less than 1; its sqrt(D) coefficient is therefore a positive integer. This would be a smaller positive solution, a contradiction. The quotient is 1, proving the assertion.

In the historically verified certificate each fundamental pair is certified using the exact regular continued fraction of sqrt(D). A positive Pell solution has gcd(x,y)=1 and satisfies

0 < x/y-sqrt(D) = 1/[y^2(x/y+sqrt(D))] < 1/(2y^2).

The standard continued-fraction approximation lemma therefore makes x/y a convergent. The lemma follows from the best-approximation property of adjacent convergents: if q_j<=q<q_(j+1) and a distinct p/q had error less than 1/(2q^2), then |p q_j-q p_j| <= (q+q_j)|q alpha-p| < 1, contradicting its nonzero integral value. The best-approximation property used here is the usual one for |q alpha-p|. Consequently the first convergent with norm +1 gives the smallest positive solution. The certificate checker reconstructs every continued-fraction coefficient and every convergent before that point, and verifies that none earlier has norm +1. It is not enough merely to check x1^2-Dy1^2=1, since a later solution would omit a subsequence.

### The exact imported primitive divisor theorem

The Bilu–Hanrot–Voutier theorem used here says: for a Lucas pair (alpha,beta), every Lucas number U_k=(alpha^k-beta^k)/(alpha-beta) with k>30 has a primitive prime divisor. A Lucas pair consists of algebraic integers for which alpha+beta and alpha beta are nonzero coprime rational integers and alpha/beta is not a root of unity. A primitive prime divisor q divides U_k but does not divide (alpha-beta)^2 U_1...U_(k-1).

Apply this with alpha=x1+y1 sqrt(D) and beta=x1-y1 sqrt(D). They are roots of T^2-2x1 T+1, hence algebraic integers. Their sum is 2x1, their product is 1, and alpha/beta=alpha^2>1 is not a root of unity. All hypotheses hold. Writing

alpha^k=x_k+y_k sqrt(D)

gives U_k=y_k/y1. In particular y1 divides y_k. If y1 has a prime outside S, no positive-index solution can contribute an S-smooth Y and this D may be discarded.

### Bounding every possible index

Suppose k>30 and y_k is S-smooth. A primitive q exists and divides U_k, hence y_k; therefore q belongs to S. Primitivity also gives q not dividing 4Dy1^2, so q is odd and does not divide D y1.

Reduce modulo q. If D is a square modulo q, work in F_q; otherwise work in F_(q^2), writing s^2=D. The elements u=x1+y1 s and v=x1-y1 s are distinct and nonzero, and uv=1. Since q does not divide alpha-beta, q|U_j is equivalent to (u/v)^j=1. Primitivity says the multiplicative order of u/v is exactly k.

In the split case the order divides q-1. In the nonsplit case Frobenius sends s to -s, so u^q=v and (u/v)^q=v/u; the order divides q+1. In either case

k <= q+1 <= P+1.

It follows that every allowable index lies in 1<=k<=K=max(30,P+1). This deliberately conservative bound is sufficient. We do not use a stronger bound from the real-positive Pell setting, nor any classification of defective small-index Lucas pairs. **Every index 1 through 30 is explicitly retained**, including 1,2,3,4,6,12 and all other exceptional possibilities. Nothing at small index is discarded through the primitive-divisor theorem.

### The resulting exhaustive algorithm

Enumerate every nontrivial divisor D of Q. Certify its fundamental solution as above. If y1 is not S-smooth, discard that D by divisibility. Otherwise compute every power from index 1 through K. Retain each odd x_k for which t=(x_k-1)/2 and t+1 are both S-smooth. This produces exactly all positive consecutive S-smooth pairs: (5) proves that none can be omitted, and the final two smoothness tests prove that no spurious pair is admitted.

A start t is a three-term S-smooth block precisely when both t and t+1 are starts in that complete pair list. Thus intersecting the pair-start list with its translate produces exactly the complete triple list. This completes the bridge from the finite arithmetic certificate to all positive sizes for a fixed S.

## Exact computation for the primes at most 41

Here

S={2,3,5,7,11,13,17,19,23,29,31,37,41}, K=42.

The certificate contains all 2^13-1=8191 nontrivial squarefree divisors D, their fundamental pairs, and all continued-fraction coefficients through the first norm-one convergent. In total 1832120 coefficients are checked. Exactly 881 fundamental y1 values are S-smooth. Every index from 1 through 42 is checked for these equations.

The result is 869 consecutive-pair starts; the largest is 63927525375. Exactly 141 starts begin a three-term block, and the largest is 212380. For each of the 141, the certificate provides all prime exponents in each of the three integers, the three radicals, and their least common multiple R. Direct integer comparisons verify R>=3n in every case. Equality occurs only for n=2. No repeated positionwise radical signature occurs either, providing a redundant direct check of the desired restricted conclusion.

These counts and inequalities were verified by the candidate's independently written checker, which imports no generator code. It reconstructs continued fractions using 2-by-2 matrix products, computes Pell powers by polynomial-pair binary exponentiation rather than the generator's sequential recurrence, strips nonallowed factors using repeated gcd with Q for its smoothness decision, and independently rebuilds the complete pair and block inventories. Its factor-exponent checks reconstruct the same exact factorizations.

The certificate SHA256 is

955f27b8922973813f75f252526b869de55aaed5ad189a2d368db2d16522197a.

The checker passed under normal Python, `-O`, and `-OO`. It uses explicit exception guards rather than assertions. Three negative controls were rejected: omission of a D equation, corruption of the first fundamental x value, and omission of a listed block. Aggregate verification metadata is supplied in VERIFICATION.json; the raw run receipts and numerical certificate are omitted from this public edition.

A separately authored elementary sieve checked the eight-start classification for n<=1000000. That bounded check is a regression check, not the proof of the elementary theorem. Known two-term examples (2,8), (6,48), and (75,1215) were positive controls for two-position equality and negative controls for three-position equality. No downloaded author code, source theorem proof-computation, external dataset of solutions, floating-point arithmetic, or remote mutation was used.

The complete 141-start list is omitted from this public edition, along with the 869-pair inventory, raw arithmetic certificates and programs. These numerical conclusions depend on the preceding exact computation and independent audit, not on the aggregate counts or hashes alone. The complete finite reduction and algorithm above explain why a correctly executed enumeration covers every magnitude, but these eight prose/metadata files alone do not replay or replace the finite arithmetic verification. To independently establish the enumeration, a reader must implement and execute the stated exact algorithm or separately obtain the authenticated numerical artifacts. The elementary eight-start theorem is fully proved in the text and has no such computational dependency.

The exploratory computations at prime bounds 31 and 37 were retained in the original candidate and are omitted from this edition. A run at prime bound 43 was interrupted before a certificate was produced; it supports no mathematical assertion. The result at 41 does not depend on that interrupted run.

## Consequences and the exact remaining gap

Combining the elementary theorem, the complete 41-smooth classification, and (2), a putative counterexample a<b must satisfy all of the following:

- its common union of prime supports contains at least four primes;
- one of these primes is at least 43;
- its squarefree common union radical R is a divisor of d=b-a;
- R<=d<b;
- each position has an exponent increase at a different prime as in (3).

Since 2 and 3 belong to the union, the first two restrictions imply R>=2*3*5*43=1290. Also a>=41, because a<=40 would make all three integers have no prime above 41. Thus d>=1290 and b>=1331. These are necessary conditions, not a construction and not a sharp search record.

There is an additional useful warning about what would finish the problem. By (2), any counterexample would make

1+b(b+2)=(b+1)^2

a coprime abc triple with c=(b+1)^2>R^2. This is precisely why a universal bound c<R^(7/4), as used in the source, rules it out. Ordinary abc with epsilon=1/2 gives only (b+1)^2<=C R^(3/2)<C b^(3/2), bounding b in terms of an unspecified constant. It does not prove that no small exception exists.

The missing unconditional step is a uniform argument for the unbounded set of possible prime supports, or an actual pair meeting all three positionwise equalities. The finite-prime-set reduction decides each fixed finite support, but there are infinitely many such supports. Neither the elementary classification nor a finite number of complete support computations closes that union. The tempting inequality rad(n(n+1)(n+2))>=n for every positive n has not been proved here and must not be silently inserted.

## Attribution and acceptance boundary

The target and conditional argument are Shorey–Tijdeman's. The elementary classification and detailed finite-field/computational application are authored here without a novelty claim. The Pell strategy is classical and is also described in Filip Najman's *Large strings of consecutive smooth integers*, Section 2, https://web.math.pmf.unizg.hr/~fnajman/cs.pdf; that paper was consulted for overlap and attribution, not used as a source of solution data or executable code. Its method's known heritage prevents treating this computation as a new general theory.

This is an internally accepted partial-result edition. The original EP 850 question remains unresolved by this work. Source inspection does not confer proof acceptance, computational verification does not replace the completeness argument, and the subsequent independent audit accepts only the two delimited partial results. The elementary result is proved in full here; the 41-smooth numerical result additionally depends on the omitted exact computation. No novelty, worldwide current-status, external peer-review or full-resolution claim is made.
