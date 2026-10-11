# Independent acceptance, proof review and source review

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance of this correction, or formal proof-assistant certification.

The original uniform O((log A)^2) question remains unresolved by this work. No novelty, priority, worldwide-openness, or main-theorem refutation claim is made.

This is not a computational reproduction package. Complete authored proofs, the four exact sharpness constructions, and the full independent logical and source review are retained. Raw scan and enumeration datasets, executable code, copied source PDFs and text, rendered source images, and private coordination material are omitted. Historical checks support the written proofs and cannot be reproduced from this edition alone.

All retrieval, inspection, computation and match statements below describe the historical candidate or independent audit of October 11, 2026 UTC. No new mathematical execution or scholarly-source inspection occurred during editorial preparation.

## Part I. Acceptance and historical verification coverage

# Independent audit of fixed numerator Pierce iteration 3348

## Verdict

**ACCEPT the candidate's elementary structural results and its scoped source-index correction. The uniform O((log A)^2) problem remains unresolved.**

This is the original independent mathematical review of the complete structural proof, separate source correction and source-status assessment. The two authored mathematical documents are reproduced as distinct parts of PROOF.md; source metadata and the full independent source review are retained in this edition. The arguments were reconstructed from their statements and primary sources. No candidate program or source-author program was executed or imported. The independently written arithmetic and integrity checks pass under Python normal, -O and -OO modes, with identical respective results. Acceptance here means the reviewed claims are supported by the proofs and checks recorded in this audit. It is not a novelty, peer-review, worldwide-openness or unrestricted publication certificate.

The claims accepted are:

1. The AP LCM lemma and the bound of r[1+floor(log_2(2A-1))] on an r-periodic decrement block, including incomplete final periods and terminal transitions.
2. The necessary divisibility M_k(S) | G for k copies of a fixed word, the prime-power formula for its first excluded modulus, and all four sharp examples.
3. Exact all-pairs CRT recognition, the least valid numerator formula, and the equivalence of the original target to a uniform exponential-in-sqrt(length) lower bound on that least numerator.
4. The logarithmic constant-decrement construction, properly attributed to Erdős and Shallit rather than claimed as new.
5. The error in the printed extinction-index equivalence of Baraskar and Vukusic's 2026 Lemma 19, its corrected t-1 index for N>=3, and the distinct N=1,2 boundaries.
6. The narrowly stated downstream cautions. In particular, the paper's fixed-j cardinality theorem is not refuted. This audit supplies explicit repairs proving those bounds under the source's actual definitions.

No material defect requiring a candidate patch was found. The public proof now states L>=1 explicitly in the complete-chain CRT theorem, as was already implicit in a strictly decreasing chain starting at a positive state. This is a domain clarification, not a counterexample to the intended theorem.

## Authenticated input

- MANIFEST.json SHA256: ab14e82855bf819bc79c2b1aa492a4bd6d12b19690d9a7c4ef4404e437b486f6
- Manifest bytes: 6635; authenticated members: 41
- Every member's byte count and SHA256 matched; the actual inventory was exact and free of symlinks.
- Independent candidate authentication passed in all three Python modes and was repeated at completion.

Integrity acceptance is separate from mathematical acceptance. A digest alone proves neither mathematical truth nor permission to publish.

## Independent computation and its limits

All checks use exact integer arithmetic and exceptions that remain active under optimization.

- Every 1<=B<A<=1200: 719,400 direct orbits, compared with a separately computed dynamic-programming length array. The 3,782,774 transitions also checked quotient monotonicity, gcd divisibility, denominator updates and scaling. Maximum in this range: 17; the raw maximizing pair is omitted.
- Every sub-block and every valid period of every orbit with 2<=A<=180: 188,170 block/period instances. These include 9,295 incomplete-final-period instances, 11,802 instances containing at least two periods and 74,541 terminal blocks. Counts can overlap.
- 96,000 APs: 1<=a<=60, 1<=s<=40, 1<=k<=40; both the stronger central-binomial LCM bound and the normalized product/LCM factorial divisibility. Of these, 58,720 are primitive.
- Every nonempty subset of {1,...,10}, placed in decreasing order and followed by zero: 1,023 complete chains, including 250 compatible chains. The generalized CRT algorithm and all-pairs criterion were checked against all 516,031 candidate residues modulo the relevant LCMs, plus brute-force least numerators above the start.
- All 780 words of lengths 1..4 over {1,...,5}, repetitions 1..8 and final tails 0..6: 43,680 templates. The CRT test realized 3,047; the word obstruction excluded 32,382. Constant words, nonconstant words, nonminimal periods, zero/nonzero tails and partial-orbit inputs were covered.
- All four stated sharp examples were checked by direct modulo transitions and CRT reconstruction. Their given numerators are in fact the least numerators exceeding their respective starts.
- All starts for 14 selected numerators: 127,535 additional complete orbits. Also 4,000 deterministically selected larger pairs with A between 10^6 and 10^12. The raw selected inputs and generating code are omitted; the public verification metadata gives the coverage limits.
- The candidate-reported 26-step witness was verified directly, and 26 is the maximum among all starts for that numerator. The raw scan witness is omitted. **The complete 49,995,000-pair candidate scan through A=10000 was not independently rerun, so this audit does not independently certify that range-wide maximum.** Its authenticated receipt remains a candidate-reported finite result. The displayed record agrees with the historical 1996 table.
- Constant-word constructions for m=3..150; L(2u)/L(u) dividing binom(2u,u) for u=1..2000; dyadic logarithmic-size inequalities through m=2048.
- All N=1..3000: the source's set recurrence, true maximum lengths, corrected extinction stage and exceptional boundaries. The printed t+1 singleton claim failed in all 3,000 cases. There were 5,622 upper-half/Lemma-18 comparisons through N=600 and 39,000 repaired-inclusion/upper-bound checks for j=0..12, N=1..3000.
- Twelve mathematical negative controls and seventeen independent inventory/security mutation controls were rejected in each Python mode. Mutation controls use temporary synthetic fixtures, never original packets.

These ranges were chosen to exercise hypotheses, endpoint conventions and the distinct arithmetic mechanisms. They are reproducibility and falsification checks, not proofs of an asymptotic bound. Parts II and III below contain the complete universal arguments.

## Source authentication and attribution

Nine independent public retrievals succeeded on October 11, 2026 UTC. All eight resources having candidate byte counterparts matched exactly, including five PDFs. The official 18-page journal PDF retains the defective statement on physical/printed p. 13. The journal page and final PDF page confirm publication on January 26, 2026. The retained arXiv v1 contains the same issue as Lemma 11 on p. 10.

The historical LCM construction and the earlier 1996 uniform log A/log log A lower statement were checked at their primary sources; no priority claim is made. The 2022 upper exponent is 1/3-2/177=19/59. The freshly retrieved Shallit talks page still describes the 3/10 claim as unpublished; the bounded official-site search did not retrieve a supporting manuscript or a correction of the journal statement. This does not establish their nonexistence.

Detailed URLs, PDF byte pins and inspected page scopes are recorded in SOURCES.json and Part III below. Primary-source inspection does not certify every analytic dependency of the historical papers.

## Remaining obstruction and allowed use

Periodic pieces are controlled, but no bound is proved for the total period sum needed to cover an arbitrary orbit. A fixed nonconstant word's absolute repetition limit does not control arbitrary changing words. Similarly, a large CRT modulus can coexist with a small positive representative. The missing statement is still A_min >= exp(c sqrt(L)) uniformly over compatible chains for some c>0.

This public edition selects authored mathematical text and permissible verification metadata. It excludes the original audit's copied primary PDFs, extracts, rendered pages, raw scan datasets, executable code and private coordination material. The source correction remains separate from the unresolved uniform bound.

## Part II. Complete independent structural proof review

# Independent proof review

## Conventions and elementary identities

Throughout, A>B>0 are integers; start at b_1=B and repeatedly replace a positive b by A mod b. Stop at the first zero and count the modulo operations. This is not the Euclidean algorithm with a changing numerator. The convention gives 22,13,9,8,3,2,1,0 for (A,B)=(35,22), hence length 7.

For any transition x to y, put q=floor(A/x), d=x-y and g=gcd(A,x). Then 0<=y<x, d>0 and A=(q+1)x-d. Consequently x divides A+d. If y>0, x>A/(q+1) implies y=A-qx<A/(q+1), so floor(A/y)>=q+1. This proves strict quotient increase, including q=1; it never invokes modulo zero.

If x=gu and A=gD with gcd(u,D)=1, then gcd(A,y)=g gcd(D,D-qu)=g gcd(D,q). Thus the next reduced denominator is D/gcd(D,q), including the terminal step, where it equals 1. The gcd may increase: A=12, 5 to 2 to 0 is a counterexample to gcd constancy. Removing the initial common divisor scales every state and preserves the length. Strict denominator drops number at most floor(log_2 D_1), but intervening constant-denominator stretches need not be short. In particular this argument supplies no bound in the prime-numerator case beyond the terminal drop.

## Arithmetic progression LCM lemma

Let u_i=a+is, 0<=i<k, with a,s>=1 and gcd(a,s)=1. For any r consecutive members choose, for each prime p dividing their product, an index j having maximal p-adic valuation. Since p does not divide s, every other member has valuation at most v_p(i-j). Therefore the p-adic valuation of product/lcm is bounded by v_p(j!(r-1-j)!), which is at most v_p((r-1)!). Hence

    product of those r members / lcm of those r members divides (r-1)!.

Apply this to the last r members of the k-term progression. Because u_i>=i+1, their product is at least k!/(k-r)!. The LCM H of the entire progression is at least their LCM, giving

    H >= k! / ((k-r)!(r-1)!) = k binom(k-1,r-1).

Selecting a central binomial coefficient gives H>=k binom(k-1,floor((k-1)/2))>=2^(k-1), since that central coefficient is at least the average of the k coefficients whose sum is 2^(k-1). If gcd(a,s)=g, divide all members by g and multiply the resulting LCM by g. The statement holds for k=1, and reversing a positive decreasing AP converts it to precisely this increasing form with the same gcd. These details justify its use on phase subsequences, even when a phase has only one state.

The argument is valid. There is no assumed pairwise coprimality of the members, nor any multiplication of divisors into a claimed common divisor.

## Periodic decrement blocks

Take a block c_0>...>c_L>=0 and a period 1<=r<=L for its decrements d_i=c_i-c_(i+1). Define S=d_0+...+d_(r-1). Every r successive decrements in the block have this sum whenever the corresponding state is present. Thus the pre-transition states in phase j are

    c_j, c_j-S, ..., c_j-(k_j-1)S,

and all are positive. Their outgoing decrements equal d_j, so each state divides A+d_j. Their LCM divides that same integer. The AP lemma, applied after reversal and normalization by g_j=gcd(c_j,S), implies

    g_j 2^(k_j-1) <= A+d_j.

Taking an integer logarithm gives k_j<=1+floor(log_2((A+d_j)/g_j)). Summing counts every one of the L steps exactly once. Since d_j<=c_j<A, the claimed uniform bound follows:

    L <= sum_j [1+floor(log_2((A+d_j)/g_j))]
      <= r [1+floor(log_2(2A-1))] < r(2+log_2 A).

If the block ends at zero, zero itself is not a pre-transition state and is not placed in any LCM. Incomplete final periods simply give some phases one fewer member; no step of the proof demands equal phase lengths. The case r=L is allowed and harmless. The concatenation corollary follows by addition, but its total-period-sum hypothesis is substantive. It is not established for arbitrary inputs.

## Fixed word repetition obstruction

For a positive word w=(d_0,...,d_(r-1)), let S be its sum and G the nonnegative gcd of d_j-d_0. If k copies occur, each phase has k pre-transition states c_j-tS. For any m<=k with gcd(m,S)=1, its first m phase states cover every residue modulo m. One is divisible by m and also divides A+d_j. Hence m divides A+d_j for every j, so m divides every d_j-d_0. Taking the LCM over such m proves M_k(S) | G.

For a nonconstant word G>0. The integer SG+1 is coprime to S and larger than G, so there is a least excluded modulus K>=2. If K had at least two distinct prime divisors, each proper prime-power factor would be smaller, coprime to S and a divisor of G by minimality. Their coprime product K would also divide G, a contradiction. Thus

    K = min over primes p not dividing S of p^(v_p(G)+1),

and k<K. This is a necessary condition only; the candidate does not claim that every word below this threshold is realizable. For constant words G=0 all positive integers divide G and there is no absolute obstruction, consistently with the logarithmic construction.

The four examples pass direct remainder checks. Their (S,G,K), number of complete copies, least numerator and complete-chain CRT modulus are:

- (1,3): (4,2,3), 2 copies; A_min=39, H=168.
- (1,5): (6,4,5), 4 copies; A_min=602135, H=1548360.
- (1,11): (12,10,7), 6 copies; A_min=142958715119, H=251049450960.
- (1,3,5): (9,2,4), 3 copies; A_min=16700525, H=38427480.

For the last word, the decisive obstruction is modulus 4; modulus 2 divides G, modulus 3 is excluded by gcd(3,S)>1, and a primes-only test would miss the earlier exclusion. The examples show sharpness of this obstruction for those words, not optimality for every word.

## Constant decrement construction and its size

Let H_m=lcm(1,...,m), A=H_m-1 and B=m, with m>=3. Then A mod j=j-1 for each 1<=j<=m. Also H_m>=m(m-1), so A>m and the input is valid. The chain has length m and constant decrement 1. This construction is already present in Erdős-Shallit's Theorem 6, physical p. 7/printed p. 48, and is not a new lower-bound result.

For each u>=1, the ratio H_(2u)/H_u is a product of distinct primes whose highest powers first enter the interval (u,2u]. Each of those powers contributes 1 to the corresponding valuation of binom(2u,u); the other valuation terms are nonnegative. Thus the ratio divides that binomial coefficient and is at most 4^u. Iterating for m=2^t gives H_m<=4^(m-1), while the AP lemma gives H_m>=2^(m-1). Consequently m-1<=log_2(A+1)<=2(m-1). This proves the intended logarithmic scale along an infinite family and supplies no super-log-squared counterexample.

## CRT recognition and least representative

Let L>=1 and c_0>...>c_L=0 be integers with c_0>0. The required transitions are exactly

    A = c_(i+1) modulo c_i, 0<=i<L.

No modulus is zero. Pairwise compatibility requires gcd(c_i,c_j) to divide c_(i+1)-c_(j+1). Conversely, for each prime in H=lcm(c_0,...,c_(L-1)), choose a modulus carrying its highest exponent. Pairwise compatibility identifies a consistent residue at that highest prime power and at every lower power appearing in other moduli. Ordinary CRT over the distinct prime-power factors of H gives one residue a modulo H. This satisfies all original congruences.

Take 0<=a<H. The least solution exceeding c_0 is a+H max(0,floor((c_0-a)/H)+1). The strict inequality is essential: for [2,0], a=0,H=2, the smallest allowed numerator is 4, not 2. For [1,0], it is 2. Every larger numerator in that residue class gives exactly the prescribed complete orbit because the residues already lie in the legal ranges.

The chain [6,5,4,0] passes adjacent gcd compatibility but fails the pair (6,4), since 5 and 0 disagree modulo 2. The example A=35, states [22,13,9,8,3,2,1,0], has H=10296 and a=A_min=35. Hence neither a large H nor a large product of state moduli forces a large least positive numerator. These counterchecks address both of the tempting invalid shortcuts.

## Exact residual reformulation

Suppose the target holds uniformly, after adjusting constants for finitely many small A: P(A,B)<=C(log A)^2. Apply this to A_min for any compatible complete chain of L steps. Then A_min>=exp(sqrt(L/C)).

Conversely, if A_min>=exp(c sqrt(L)) for every compatible chain and one universal c>0, any realizing A>=A_min satisfies L<=c^(-2)(log A)^2. Passing between asymptotic and all-input statements is harmless because A>=2, each fixed A has finitely many starts and every orbit terminates.

This equivalence is correct but is not a lower bound proof. The earlier LCM argument applies to a shared shifted numerator inside periodic pieces. It does not bound the least CRT representative for arbitrary changing decrements. Neither gcd-change counts nor the nonconstant-word obstruction fills this gap.

## Part III. Complete independent source review and local repairs

# Primary source review and extinction correction

## Exact journal version and locations

The principal source is Omkar Baraskar and Ingrid Vukusic, Bounds for Sets of Remainders, Journal of Integer Sequences 29 (2026), Article 26.1.4. Its official publication page records January 26, 2026, with a revised version received January 22. The PDF has 18 physical pages and matching printed page numbers.

- Official page: https://cs.uwaterloo.ca/journals/JIS/VOL29/Vukusic/vukusic2.html
- Official PDF: https://cs.uwaterloo.ca/journals/JIS/VOL29/Vukusic/vukusic2.pdf
- Independently retrieved October 11, 2026 UTC: 377174 bytes, SHA256 3cd27f6994d93ad35711bbeee2f2389a7d5350427aa222af9626794a70c99be3.
- The fresh PDF is byte-identical to the candidate's retained PDF.

The relevant definitions occur on p. 3 and are repeated on p. 13. They are S_0(N)={1,...,floor(N/2)} and S_(j+1)(N)={N mod b : b in S_j(N), b!=0}. The source's p. 13 defines an individual orbit from a_0=a, stops at a_t=0, and maximizes its length over 1<=a<=N. In particular, an orbit beginning at N has length 1, not zero. These definitions agree with the candidate correction's convention.

The disputed Lemma 19 is on p. 13 and its proof continues on p. 14. Visual inspection confirms its t+1 subscript. The source does not define a successor of zero. Under its actual recurrence, N=3 has P(3)=2, S_0={1}, S_1={0}, S_2=empty and S_3=empty. Thus the printed equivalence is false.

The August 28, 2025 arXiv v1 at https://arxiv.org/pdf/2508.20853v1 has the same statement as Lemma 11 on physical/printed p. 10. Independent retrieval gave 481304 bytes, SHA256 1b1c1fb0438662608e4f778fea3c365b12b2b2455c8de0c236a447dad0a6fe17, again matching the candidate. Its p. 10 was also visually checked. The journal correction is therefore pinned to a published version, rather than inferred only from an earlier preprint.

## Reconstructed corrected theorem

Define T_N(b) to be the number of applications of b -> N mod b until the first zero, with b initially positive and zero having no successor. Put P(N)=max_(1<=b<=N) T_N(b).

For every N>=3 and t>=1, the following are equivalent:

1. P(N)=t.
2. S_(t-1)(N)={0}.
3. S_(t-1)(N) is a singleton and all its subsequent iterates are empty.

For N=1, P(1)=1 and all S_j are empty. For N=2, P(2)=1 but S_0={1}, S_1={0}, and all S_j with j>=2 are empty. Neither boundary satisfies the N>=3 formula.

### Proof of the extinction stage

For N>=2, let Q=max_(1<=b<=floor(N/2)) T_N(b). A member of S_j is exactly the j-th state of an orbit beginning in that lower half, provided that state exists. There is a length-Q orbit, all lower-half orbits have terminated by Q, and no zero is allowed a successor. Therefore S_Q={0}, every later set is empty, and every earlier set contains a positive state from a maximizing orbit. In particular the singleton-zero stage is unique.

Every start b>N/2 with b<N has first remainder N-b in the lower half, so its length is at most Q+1. Lower-half starts have length at most Q, and b=N has length 1. Thus P(N)<=Q+1.

For N>=3 choose a lower-half maximizing b. If b<N/2, then N-b lies strictly above N/2 and below N, has remainder b, and has length Q+1. If b=N/2, N is even and b has length 1, so Q=1. Here N>=4 and b'=1 is also a maximizing lower-half state strictly below N/2. Use N-b'=N-1 instead. Hence P(N)>=Q+1.

It follows that P(N)=Q+1 and S_(P(N)-1)={0}. Uniqueness of the singleton-zero stage proves equivalence of the first two claims. A singleton with empty next image must be {0}, since a positive member always has a remainder. This proves the third. The N=1,2 statements follow directly from their explicitly listed sets and possible starts.

This establishes the candidate's full correction, not merely its N=3 counterexample. No assumption of persistent zero or a maximum of an empty set is hidden in the proof.

## Nearby source statements and limited downstream effects

### Lemma 18 and its endpoint issue

On p. 13, the source identifies S_j with states reached after j+1 steps from an upper-half start, for j>=1 and N>=1. The first upper-half image is actually U={0,...,ceil(N/2)-1}, not S_0. For odd N the extra zero disappears on the next iteration. For even N>=4, U lacks N/2 and includes zero, but N/2 would map to zero and that zero is already supplied by the state 1 in both relevant positive sets. Hence the first images of U and S_0 agree for all N>=3, and their later images agree.

For N=2, the only upper-half start is a=2. It has a_1=0 and no a_2, while S_1={0}. Lemma 18 therefore fails for N=2,j=1 under the stated stopping convention. For N=1 its two sides are empty at the higher stages, although its explanatory endpoint identification is still inaccurate. The candidate correctly avoids using that identification as a proof premise.

The proof on p. 14 also needs care at b=N/2: replacing it with N-b gives the same starting state, rather than one extra step. The Q=1/alternative-start argument above repairs this point.

### Lemma 21 and the empty set

The displayed maximum in Lemma 21 (p. 14) is undefined after extinction in the usual convention; S_0(1) is also empty. Moreover its proof's assertion that every minimum is zero does not hold for the defined S_0. The useful estimate has a simple domain-safe formulation:

    S_j(N) is contained in the nonnegative integers <= N/(j+2).

The base follows from S_0's definition. If r=N mod b with b in S_j positive, then b>=r+1 and b<=N/(j+2), so q=floor(N/b)>=j+2. Hence N=qb+r>=(j+2)(r+1)+r, implying r<=N/(j+3). This proves the containment inductively, including empty sets. Counting nonnegative integers gives s_j(N)<=N/(j+2)+1, which supplies the claimed fixed-j asymptotic upper bound without any maximum-of-empty convention. For a nonempty S_j, the source's two displayed inequalities hold; s_j-1<=max S_j needs only nonnegative integrality, not min S_j=0.

### Lemma 23 and a full repair of its base case

Visual inspection of p. 15 confirms that the stated progression at j=0 includes zero, while the actual S_0 excludes it. Its proof then writes a different S_0 containing zero. The candidate's proposed repair is valid. The following induction proves a slightly more explicit safe form for every N>=1 and j>=0, with an empty right-hand side allowed.

Set x_0=0 and x_(j+1)=N-(j+2)x_j. Then

    S_j(N) contains every integer r satisfying
    max(1,j)<=r<=(N-j-1)/(j+2),
    r = x_j modulo (j+1)!.

At j=0, the integers 1<=r<=(N-1)/2 are in S_0. Suppose the claim is known for j and let r be in the claimed progression for j+1. The congruence gives an integer k=(N-r)/(j+2) with k=x_j modulo (j+1)!. The upper bound on r gives k>=r+1; thus k>=j+2>=max(1,j). Its lower bound r>=j+1 gives k<=(N-j-1)/(j+2). Therefore k is in S_j, and N=(j+2)k+r with 0<=r<k gives r in S_(j+1). This proves the induction. No large-N threshold is actually required for this repaired inclusion; when the interval is empty, it is automatic.

For a fixed j, the number of integers in this progression is N/(j+2)!+O_j(1), uniformly in the varying residue class x_j. Combined with the domain-safe upper estimate, this recovers the fixed-j cardinality bounds of Theorem 3. Its p. 15 proof explicitly invokes Lemmas 21 and 23, not Lemma 19. The offset defect does not refute Theorem 3; the neighboring endpoint/domain issues have now been addressed constructively.

This is a local audit of the iteration section and its stated consequence. The distinct asymptotic formula for s(N) and the consecutive-difference theorems were not independently audited, and nothing here shows them false. The additive two-stage correction also does not change the qualitative polynomial-versus-logarithmic discussion in Remark 20 for sufficiently large N.

## Other primary sources and attribution checks

- Open Problem Garden, A discrete iteration related to Pierce expansions: https://www.openproblemgarden.org/op/a_discrete_iteration_related_to_pierce_expansions. The stored mathematical image alt text specifies A>B>0, fixed A, the 35/22 example and the uniform log-squared question. Its historical current-best wording is not treated as a present literature certificate.
- Erdős and Shallit, New bounds on the length of finite Pierce and Engel series, 1991: https://numdam.org/item/JTNB_1991__3_1_43_0.pdf. Physical pp. 2-8/printed pp. 43-49 were inspected; the explicit LCM construction in Theorem 6 on physical p. 7/printed p. 48 was visually verified. The packet's attribution is supported.
- Vlado Kešelj, Length of Finite Pierce Series: Theoretical Analysis and Numerical Computations, CS-96-21, September 10, 1996: https://cs.uwaterloo.ca/research/tr/1996/21/cs-96-21.pdf. Theorem 2 is on physical p. 18/printed p. 15. Theorem 3 is on physical p. 21/printed p. 18 and gives the uniform log A/log log A lower order; it was visually verified. The record table on physical p. 27/printed p. 24 includes the candidate-reported 26-step record, and the preceding page reports a scan through 3,600,000. The raw scan pair is omitted here. The candidate correctly avoids calling its smaller finite scan a new computational record. This is not an independent audit of all historical numerical results or priority claims.
- Chase and Pandey, On the length of Pierce expansions, arXiv:2211.08374v1, November 15, 2022: https://www.math.kent.edu/~zchase/pierce.pdf. All eight pages were read as source context; the definitions and Theorem 1.1 are on p. 2, Theorem 1.2 on p. 3. Their P(a,n) reverses the target's argument roles. The exponent arithmetic gives 1/3-2/177=19/59. The cited analytic estimates were not independently re-proved.
- Jeffrey Shallit's current talks page: https://cs.uwaterloo.ca/~shallit/talks.html. Fresh bytes retain the n^(3/10) LLM announcement and describe it as unpublished. His selected works page, https://cs.uwaterloo.ca/~shallit/papers.html, was also checked. The bounded primary-domain searches in the retained receipt found the announcement, journal publication and arXiv preprint, but did not supply the announced manuscript or a journal erratum. This is a retrieval limit, not proof of nonexistence, novelty or global open status.

All PDFs and HTML sources were independently retrieved through public URLs during the original audit. No author/source software was run and no author was contacted. Public byte identities and separate historical inspection scopes are in SOURCES.json; copied source files and visual renderings are not distributed.
