# Fixed-numerator Pierce iteration and a separate source correction

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance of this correction, or formal proof-assistant certification.

The original uniform O((log A)^2) question remains unresolved by this work. No novelty, priority, worldwide-openness, or main-theorem refutation claim is made.

This is not a computational reproduction package. Complete authored proofs, the four exact sharpness constructions, and the full independent logical and source review are retained. Raw scan and enumeration datasets, executable code, copied source PDFs and text, rendered source images, and private coordination material are omitted. Historical checks support the written proofs and cannot be reproduced from this edition alone.

All retrieval, inspection, computation and match statements below describe the historical candidate or independent audit of October 11, 2026 UTC. No new mathematical execution or scholarly-source inspection occurred during editorial preparation.

## Part I. Structural results for the fixed-numerator iteration

# Fixed-numerator Pierce iteration: periodic-decrement bounds and the remaining obstruction

## 1. Scope and outcome

For integers A > B > 0, put b_1 = B and b_(i+1) = A mod b_i until the first zero b_(n+1). Write P(A,B)=n. The numerator A remains fixed; no coprimality condition is imposed. In particular, P(35,22)=7.

The uniform assertion P(A,B)=O((log A)^2) is **not proved or disproved here**. The results below give rigorous logarithmic bounds for structured parts of any orbit, a stronger obstruction to repetition of a fixed nonconstant decrement word, and an exact arithmetic reformulation of the unresolved question. All proofs are elementary and self-contained. The restricted statements were accepted in the independent internal AI audit reproduced in AUDIT.md; novelty is not claimed.

The separate source-index correction in Part II below is not a resolution of this question.

## 2. Basic identities and the gcd warning

For 1 <= i <= n let q_i=floor(A/b_i), d_i=b_i-b_(i+1), and g_i=gcd(A,b_i). Then

- b_i > b_(i+1) >= 0 and d_i>0;
- A=(q_i+1)b_i-d_i, so b_i divides A+d_i;
- the q_i are strictly increasing;
- g_i divides g_(i+1), with g_(n+1)=A.

Here is a direct proof of quotient monotonicity. The remainder inequality A<(q_i+1)b_i gives
b_(i+1)=A-q_i b_i < A/(q_i+1). If b_(i+1)>0, its quotient is therefore at least q_i+1.

The common divisor of the initial pair can be removed: if g=gcd(A,B), every state is divisible by g and
P(A,B)=P(A/g,B/g). Nevertheless the gcd need not remain equal to this initial g. For example, the orbit for (A,B)=(12,5) is 5,2,0, and gcd(12,5)=1 while gcd(12,2)=2.

More precisely, let D_i=A/g_i, including D_(n+1)=1. Writing b_i=g_i u_i, where gcd(D_i,u_i)=1, gives

D_(i+1) = D_i / gcd(D_i,q_i).

This follows from gcd(D_i,D_i-q_i u_i)=gcd(D_i,q_i). There can be at most floor(log_2 D_1) strict denominator decreases, but there is no bound here on the number of steps between them. If A is prime, all nonterminal steps preserve D_i=A. Thus counting strict gcd changes cannot by itself settle even the prime case.

## 3. An elementary least-common-multiple lemma

**Lemma 1.** Let k>=1 and let a,a+s,...,a+(k-1)s be positive integers, with s>0 and gcd(a,s)=1. Their least common multiple L satisfies

L >= k * binom(k-1, floor((k-1)/2)) >= 2^(k-1).

For a progression with gcd(a,s)=g, the same lower bound is multiplied by g.

**Proof.** First consider any r consecutive members u_0,...,u_(r-1) of the coprime progression and write L_r=lcm(u_0,...,u_(r-1)). We show

(product u_j)/L_r divides (r-1)!.

Fix a prime p dividing one of these members. It cannot divide s. Choose an index j_0 with largest p-adic valuation among these members. For j!=j_0,

v_p(u_j) <= v_p(u_j-u_(j_0)) = v_p(j-j_0).

Indeed, if the valuations of the two members differ, the valuation of their difference is the smaller one; if they agree, that difference has at least that valuation. Summing over j!=j_0 gives

v_p((product u_j)/L_r)
 <= v_p(j_0! (r-1-j_0)!)
 <= v_p((r-1)!).

This proves the divisibility claim prime by prime.

Apply it to the final r members of the original k-member progression. Since a,s>=1, its member of index i is at least i+1. Consequently

L >= [k!/(k-r)!]/(r-1)! = r * binom(k,r).

Choose r so that r-1 is a central index of the binomial coefficients of order k-1. Then r binom(k,r)=k binom(k-1,r-1). The central coefficient is at least the average 2^(k-1)/k of those k coefficients. The asserted bounds follow. If gcd(a,s)=g, divide every member by g and then multiply its LCM by g. The case k=1 is immediate. QED.

## 4. Periodic-decrement blocks have logarithmic length

A block of L steps has states c_0>c_1>...>c_L>=0, each satisfying c_(i+1)=A mod c_i. Its decrement word is d_i=c_i-c_(i+1), for 0<=i<L. A positive integer r<=L is a period if d_(i+r)=d_i whenever both positions exist. This definition allows a final incomplete period.

Write S=d_0+...+d_(r-1). For each phase 0<=j<r, let k_j be the number of indices in {0,...,L-1} congruent to j modulo r, and set g_j=gcd(c_j,S).

**Theorem 2.** Every such block satisfies

2^(k_j-1) <= (A+d_j)/g_j,

and hence

L <= sum_(j=0)^(r-1) [1+floor(log_2((A+d_j)/g_j))]
  <= r [1+floor(log_2(2A-1))].

In particular L < r(2+log_2 A).

**Proof.** The states at positions j,j+r,j+2r,... are exactly
c_j,c_j-S,c_j-2S,..., and remain positive because these are states before one of the L steps. Their decrement is always d_j. By Section 2 each of these states divides A+d_j. Their LCM therefore divides A+d_j. Dividing this progression by g_j gives a coprime progression, so Lemma 1 gives

A+d_j >= g_j * 2^(k_j-1).

This proves the first inequality and its integer logarithm form. Sum over the r phases. Finally 1<=d_j<=c_j<A, so A+d_j<=2A-1. QED.

**Corollary 3.** If the entire decrement word can be partitioned into blocks with respective periods r_1,...,r_h, then

P(A,B) <= (r_1+...+r_h) [1+floor(log_2(2A-1))].

Thus the requested log-squared conclusion holds for any family of inputs that admits such partitions with sum r_j=O(log A). For a fixed number of blocks of bounded period, the stronger O(log A) bound holds.

This is a conditional structural criterion. No bound of O(log A) on that period sum is established for general orbits. Allowing each step to be its own block makes the hypothesis vacuous and proves nothing further.

## 5. A fixed nonconstant word has an absolute repetition limit

The preceding theorem still permits logarithmically many repetitions as A grows. For a fixed nonconstant decrement word there is a stronger restriction independent of A and of the starting state.

Let w=(d_0,...,d_(r-1)) be a word of positive integers, and set

S=sum d_j,
G=gcd(d_1-d_0,...,d_(r-1)-d_0),

using the nonnegative gcd and G=0 for a constant word. For k>=1 define

M_k(S)=lcm{m: 1<=m<=k and gcd(m,S)=1}.

**Theorem 4.** If k complete consecutive copies of w occur in a Pierce orbit, then M_k(S) divides G.

**Proof.** Fix m<=k coprime to S and fix a phase j. The k states in that phase are c_j-tS for 0<=t<k. The first m of them represent all residue classes modulo m, so at least one is divisible by m. That state divides A+d_j. Hence A+d_j is divisible by m. This holds for every phase, so m divides every d_j-d_0, and therefore m divides G. Taking the LCM over m proves the result. QED.

If w is nonconstant, define

K(S,G)=min{m>=2: gcd(m,S)=1 and m does not divide G}.

This exists: SG+1 is coprime to S and is larger than G. Theorem 4 gives k<K(S,G). The first excluded m must be a prime power. Indeed, if m has at least two distinct prime factors, all its proper prime-power factors are smaller, coprime to S, and divide G by minimality; their LCM is m, a contradiction. Consequently

K(S,G)=min_(p prime, p does not divide S) p^(v_p(G)+1).

This formula is an exact explicit obstruction, not a sufficient condition for realizing a word. Additional pairwise congruence constraints can prevent realization below this threshold.

**Examples and tightness of this obstruction.** Each line below is a complete orbit, ending at zero, and attains the maximal repetition count allowed by Theorem 4 for the indicated word.

- Word (1,3), S=4, G=2, K=3: A=39, states 8,7,4,3,0. Two copies occur.
- Word (1,5), S=6, G=4, K=5: A=602135, states 24,23,18,17,12,11,6,5,0. Four copies occur.
- Word (1,11), S=12, G=10, K=7: A=142958715119, states 72,71,60,59,48,47,36,35,24,23,12,11,0. Six copies occur.
- Word (1,3,5), S=9, G=2, K=4: A=16700525, states 27,26,23,18,17,14,9,8,5,0. Three copies occur. Here the decisive modulus is 4, showing why prime powers strengthen a primes-only argument.

The modulo operation verifies each displayed chain directly. For example, an alternating word (a,b) with a+b odd and a!=b cannot repeat twice when a-b is odd: modulus 2 already forbids it.

## 6. Constant decrements show that the logarithmic scale cannot be improved in general

This is the standard LCM construction credited to Erdős–Shallit, rather than a new lower-bound claim. For m>=3 set

A=lcm(1,...,m)-1, B=m.

Then A mod j=j-1 for every 1<=j<=m, so the orbit is m,m-1,...,1,0 and P(A,m)=m. These are single-period blocks.

The required inequality A>B holds: lcm(1,...,m) is at least lcm(m-1,m)=m(m-1), whose value minus 1 exceeds m for m>=3.

For completeness, the construction has logarithmic order along m=2^t. Let L(u)=lcm(1,...,u). The quotient L(2u)/L(u) divides binom(2u,u): for any prime whose exponent increases, the new prime power lies in (u,2u], contributes 1 to the central binomial valuation, and the exponent increases by at most 1. Thus L(2u)<=L(u)4^u. Iterating from L(1)=1 gives L(2^t)<=4^(2^t-1). Lemma 1 also gives L(m)>=2^(m-1). Therefore, for this family,

m-1 <= log_2(A+1) <= 2(m-1).

So arbitrarily long constant-decrement blocks really can have length proportional to log A. This is compatible with the target and is not a super-log-squared counterexample.

## 7. Exact CRT recognition and an equivalent unsolved growth problem

**Theorem 5.** Let L>=1 and let c_0>c_1>...>c_L=0 be a prescribed chain of nonnegative integers. It is a complete fixed-numerator orbit for some integer A>c_0 if and only if

gcd(c_i,c_j) divides c_(i+1)-c_(j+1)

for every 0<=i,j<L. When compatible, all valid numerators lie in a single residue class a mod H, where H=lcm(c_0,...,c_(L-1)). Choose 0<=a<H. The smallest numerator exceeding c_0 is

A_min = a + H * max(0, floor((c_0-a)/H)+1).

**Proof.** The transition condition is exactly A congruent to c_(i+1) modulo c_i, because 0<=c_(i+1)<c_i. Necessity of the pairwise condition follows by subtracting two congruences. For sufficiency, work prime by prime. For each prime dividing H, choose a modulus c_i with the highest exponent of that prime. The pairwise condition says its required residue agrees with every other required residue modulo the smaller prime power. It therefore determines one consistent congruence at the highest power. The ordinary CRT for these mutually coprime highest prime powers gives a unique residue modulo H, satisfying all the original congruences. Taking the least representative above c_0 gives the displayed formula, and all transitions then hold with A fixed. QED.

Adjacent compatibility is insufficient. For the chain 6,5,4,0, adjacent positive moduli are coprime, but the first and third congruences require A congruent to 5 modulo 6 and to 0 modulo 4, which disagree modulo 2. No numerator realizes this chain.

Large H alone does not imply large A_min. The actual orbit of A=35 beginning at 22 has H=10296. Its small simultaneous residue is 35. Multiplying all state moduli, or treating their LCM as a divisor of A, is invalid unless the residues have also been accounted for. The common shifted multiple A+d exists only inside the structured pieces used in Theorem 2.

By Theorem 5, the original target is equivalent (after harmless adjustment for finitely many small A) to the following uniform statement over all compatible complete chains:

There is c>0 such that A_min >= exp(c sqrt(L)).

Indeed, P(A,B)<=C(log A)^2 gives this with c=1/sqrt(C) at A_min. Conversely this inequality gives L<=c^(-2)(log A_min)^2<=c^(-2)(log A)^2 for any numerator realizing the chain. Finitely many exceptional small numerators have only finitely many orbits, so asymptotic and all-input forms differ only by constants.

No such lower bound on the least CRT representative is proved here. Theorems 2 and 4 control periodic decrement pieces; they do not control how many irregular pieces a long compatible chain can contain. This is the exact remaining obstruction in this approach.

## 8. What the finite checks establish

The original candidate checks used exact integer arithmetic and explicit exceptions, never assert statements. Their historical coverage is summarized here; the code and raw datasets are not distributed in this edition. They compare direct iteration with dynamic programming for all 79,800 pairs with 2<=A<=400; test the AP LCM inequality in 12,000 finite cases; compare generalized CRT with a separate bounded brute-force search for 255 complete chains; examine 3,780 periodic-word/tail cases; and verify every displayed example.

A separate exhaustive dynamic-programming scan covers all 49,995,000 pairs with 2<=A<=10000. Its candidate-reported maximum is 26. The independent audit verified the corresponding witness and all starts for its numerator, but did not rerun this complete 49,995,000-pair scan or independently certify the range-wide maximum. This is a reproducibility check, not an extension of the larger computation already reported in 1996 and not evidence sufficient for any asymptotic conclusion.

The human-readable proofs above, rather than the finite scan, justify the universal structured statements. The complete independent logical review is in AUDIT.md. No novelty assessment is claimed.

## Part II. Separate published-source extinction-index correction

# Scoped correction: extinction index for iterated remainder sets

## Version and exact issue

The inspected source is Omkar Baraskar and Ingrid Vukusic, *Bounds for Sets of Remainders*, Journal of Integer Sequences 29 (2026), Article 26.1.4, published January 26, 2026. The 18-page journal PDF was retrieved from the official journal site on October 11, 2026. Its SHA256 is 3cd27f6994d93ad35711bbeee2f2389a7d5350427aa222af9626794a70c99be3, size 377174 bytes.

Official source: https://cs.uwaterloo.ca/journals/JIS/VOL29/Vukusic/vukusic2.pdf

Its definitions on physical/printed p. 3 set S_0(N)={1,...,floor(N/2)} and S_(j+1)(N)={N mod b: b in S_j(N), b!=0}. On physical/printed p. 13, Lemma 19 equates P(N)=t with S_(t+1)(N)={0}. That index is incorrect. This is also present as Lemma 11 on p. 10 of the retained arXiv v1 (August 28, 2025), whose separate source pin is in SOURCES.json.

Counterexample: N=3 has P(3)=2, S_0={1}, S_1={0}, and S_j=empty for all j>=2. Thus S_(t+1)=S_3 is empty.

The following proof is independent and addresses the positive-integer boundary cases explicitly.

## Corrected exact statement

Use the source convention P(N)=max_(1<=b<=N) P(N,b), where P(N,b) counts modulo steps to the first zero. The choice b=N has length 1, so it does not change the maximum for N>=2 compared with 1<=b<N.

For every N>=3 and positive integer t, the following conditions are equivalent:

1. P(N)=t.
2. S_(t-1)(N)={0}.
3. |S_(t-1)(N)|=1 and S_(t-1+j)(N)=empty for every j>=1.

The boundary cases are:

- N=1: P(1)=1 and S_j(1)=empty for every j>=0. There is no singleton-zero extinction stage.
- N=2: P(2)=1, S_0(2)={1}, S_1(2)={0}, and S_j(2)=empty for every j>=2.

Neither boundary satisfies the N>=3 formula, so the corrected statement must not silently include them.

## Proof

First fix N>=2 and let Q be the largest orbit length among starting states 1<=b<=floor(N/2). This set is nonempty. Under repeated application of the map, an orbit contributes its j-th state to S_j precisely when it has not terminated before that state. Consequently:

- S_Q={0}, because some orbit has length Q and every contributing orbit ends by that time;
- S_j=empty for j>Q;
- S_j contains a positive state for j<Q, obtained by following an orbit of maximal length Q.

In particular S_Q is the unique stage equal to {0}. This argument does not define a modulo operation at zero; states equal to zero have no successor.

We now show P(N)=Q+1 for N>=3. If N/2<b<N, its first remainder is N-b<N/2, so its orbit length is at most Q+1. Starts at most N/2 have length at most Q, and the start b=N has length 1. Therefore P(N)<=Q+1.

Choose a lower-half starting state b attaining Q. If b<N/2, then the valid upper-half start N-b has first remainder b and length Q+1. If the only selected maximizer is b=N/2, then N is even and that state has length 1, so Q=1. Since N>=4 in this case, b=1 also lies strictly below N/2 and attains Q. Apply the same upper-half construction to b=1. Thus P(N)>=Q+1.

Combining P(N)=Q+1 with the unique singleton-zero stage Q proves the first two equivalences. A singleton whose next image is empty must consist of zero, because every positive state has a defined successor. This also proves the third equivalence. The explicit N=1,2 computations above prove the boundary claims. QED.

## Downstream consequences and limits of this correction

1. The exact translation from orbit length to extinction time needs the index t-1 and the N>=3 restriction. A program using t+1 would misidentify the stage by two iterations.
2. The fixed-j asymptotic statement in the source's Theorem 3 is not refuted by this defect. Its printed proof invokes Lemmas 21 and 23, rather than Lemma 19. An additive two-stage shift also does not change the polynomial-versus-logarithmic size discussion of an extinction time.
3. The source's Lemma 18 is stated down to N=1; when iterations stop at zero, N=2, j=1 already exposes a boundary problem in its higher-iterate formulation. Its explanatory description of S_0 also suppresses endpoint discrepancies. The corrected proof above avoids that identification entirely. For N>=3 the image sets agree after the first application: the lower-half set and {0,...,ceil(N/2)-1} differ only at endpoints whose images are absent or the already-present zero.
4. Empty sets have no maximum under the ordinary convention. A use of the source's Lemma 21 after extinction should either restrict to nonempty S_j or state a convention for max(empty). This is a domain issue, not a disproof of the bound where defined.
5. There is a separate endpoint mismatch at j=0 in the stated inclusion of Lemma 23 (p. 15): its right-hand side includes zero, while the defined S_0 excludes zero. Replacing the lower endpoint j by max(1,j) removes that base-case issue without changing the fixed-j asymptotic cardinality. The full independent local repairs of Lemmas 21 and 23 appear in Part III of AUDIT.md. They recover the fixed-j bounds of Theorem 3 under the actual definitions; no full audit of all arguments of the paper is claimed.

No conclusion that the paper's main theorem is false is drawn. No author was contacted during the original research or audit. The correction concerns an exact indexing statement only and does not resolve the uniform log-squared Pierce problem.
