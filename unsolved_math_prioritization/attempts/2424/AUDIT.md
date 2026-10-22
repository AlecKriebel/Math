# Audit of the Price claim for Erdős problem 983

This is an AI-assisted, unrefereed authored mathematical audit edition. Acceptance means an independent internal AI audit of the precisely scoped written arguments after explicit repairs. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete authored mathematical reconstruction and correction arguments are retained. Copied source documents, source text and images, executable code, raw check arrays, datasets and private coordination material are not distributed.

Source retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Finite checks corroborate the arguments; infinitude and unbounded conclusions rest on the written proofs.

## Finding

The linked manuscript was recovered and inspected in full. The main disproof is mathematically correct after a local correction to an auxiliary graph statement and clarification of the exact-r definition. The stated general-k inequalities also survive these corrections. This is an audit of a specifically matching prior result, not a new solution or a novelty claim.

The first-part conclusion is: for infinitely many integers n, f(pi(n)+1,n) = 2 pi(sqrt(n)) + 1. Therefore the proposed difference equals -1 infinitely often and cannot tend to positive infinity. The broad request to estimate f(k,n), especially throughout pi(n)+1 < k = o(n), is only partially addressed. The manuscript gives lower bounds and a universal upper bound, not a general asymptotic solution.

The graph lemma as printed is false in one direction. This report supplies an explicit counterexample, the correct identity, and a complete repair. The main theorem does not need that false direction. The opening equality between two possible readings of f also needs care: the manuscript's argument identifies each set's minimum support size but does not itself justify an exact-r universal quantifier. A direct exact-r upper-bound proof below avoids relying on that unproved interchange. No uncorrected blanket acceptance of the manuscript is asserted.

## Source identity and inspection scope

Liam Price's public forum post of 30 April 2026 at 17:02 links https://www.overleaf.com/read/txdtmxbdctvr#0deab3 and attributes the claimed disproof and further bound to GPT-5.5 Pro. A public archival copy at commit 4b4ec96f1c81492af02f814c65825a5106e0af60 records post 6104 and the author-linked pointer; a separate public note at commit c58f8589136880d44f4a4299e5fc01fd5084506f corroborates it. The copies establish historical attribution and the pointer, not mathematical correctness. Direct live forum access was unavailable during the original audit.

The author-linked manuscript, titled “A Sharp Hall Obstruction”, was recovered and inspected in full. Its six-page PDF and the complete displayed source were read, with all six PDF pages visually inspected. The PDF is 225269 bytes, SHA-256 a6de60927f463eef60f1742f78cc90ecbb3db83b3a6da6283d5c72cc407f4e25; its service-created timestamp is 2026-10-11 04:36:30 UTC. This is the current snapshot recovered at the author-linked URL, not a verified byte-identical copy of the exact 30 April revision. Completeness of revision history is not claimed. No source-author code was executed.

Erdős's printed pages 138–140 and Pomerance's printed page 399 were visually inspected in the original audit. SOURCES.json records their public citations, PDF identities and exact inspection boundaries. This edition contains authored mathematics and public verification metadata, with no copied manuscript, source text or source images.
## Definition and conventions

Let n >= 2, pi(n) < k <= n, and P(a) be the set of all prime divisors of a. Set P(1) = empty set. For a finite set S of distinct primes, A[S] consists of a in A for which P(a) is a subset of S. The strict inequality is |A[S]| > |S|. Having merely one prime divisor in S, or replacing > with >=, is a different problem. The prime set may depend on the adversarially chosen A.

For each A, define rho(A) as the minimum |S| with |A[S]| > |S|; equivalently it is the minimum |P(B)| over B subset A with |B| > |P(B)|. This equivalence is valid: a supporting S gives such B with no larger support, and a deficient B supplies S = P(B). Existence follows directly by taking B=A, since |P(A)| <= pi(n) < |A|; invoking Hall is optional.

For maximum-minimum notation write f_at_most(k,n) = max_A rho(A). For the literal fixed-cardinality wording write f_exact(k,n) = min{r: for every k-set A there is S with |S|=r and |A[S]|>r}. Always f_at_most <= f_exact. An arbitrary small deficient support cannot simply be padded by unused primes without risking loss of strict deficiency. We do not claim these two quantities agree in every parameter range based solely on equation (1) of the manuscript. The disproof and every stated inequality below hold for both: the lower witnesses exclude every smaller cardinality; the upper proof constructs a common exact cardinality.

We allow r=0. Thus rho(A)=0 exactly when 1 belongs to A, and either universal quantity is 0 when k=n. For k<n, an admissible A omitting 1 exists, so the universal quantity is not 0. If one instead insists r>=1, the relevant first-part result and all positive lower bounds are unchanged. Every construction used below omits 1. Primes greater than n never support an element greater than 1, and do not defeat any lower bound. For upper bounds we only use primes <=n.

## Universal upper bound with exact cardinality

Set M=pi(n), m=pi(sqrt(n)), and R=min(M,2m+1). We prove that every A with |A|>M has R primes supporting at least R+1 elements. This proves f_exact(k,n) <= R <= 2m+1, and also the same bound for f_at_most.

If R=M, select all primes <=n. They support all of A, so the claim is immediate. Otherwise there are L=M-m >= m+1 primes q above sqrt(n). Every integer <=n contains at most one such prime. Partition A into the a0 elements with no such prime and groups of sizes c1,...,cL by their unique such divisor. Sort the c_i in nonincreasing order and select all m small primes and the first m+1 large primes. The selected primes support exactly a0+c1+...+c_(m+1) elements. If c_(m+1)>=2, this count is at least 2m+2. Otherwise every unselected group has size at most 1, whence the count is at least |A|-[L-(m+1)] >= M+1-L+m+1 = 2m+2. The selected set has exactly 2m+1 primes, as required.

The manuscript's separate minimal-defect proof correctly proves the at-most version: inclusion-minimal deficient B has |B|=|P(B)|+1 and each prime in its support divides at least two elements of B. At most one large prime divides each integer, giving r<=2m+1. It also handles B={1}, where r=0. It should not be used as an unexplained padding argument for the exact-r wording.

## Infinitely many balanced prime indices

The manuscript's balanced-prime assertion is correct and is prior literature: Carl Pomerance, “The Prime Number Graph”, Mathematics of Computation 33 (1979), 399–408, https://math.dartmouth.edu/~carlp/PDF/paper19.pdf . Page 399 explicitly states that infinitely many N satisfy p_(N-i) p_(N+i) < p_N^2 for every integer 1<=i<N. Its proof is geometric. The manuscript supplies an elementary supporting-line argument for the same fact but omits this attribution.

For completeness, its proof checks out. The central binomial coefficient satisfies 4^t/(2t+1) <= binom(2t,t) <= (2t)^{pi(2t)}, because each p-adic valuation is at most log_p(2t). Hence pi(x) is at least a positive constant times x/log x for all sufficiently large x. Taking x=C j log(2j), with C a sufficiently large constant, yields p_j<=x. Therefore a_j=log p_j is o(j) and tends to infinity.

For lambda>0, the sequence a_j-lambda j tends to minus infinity, so it has a maximizing index N. Comparing with N-i and N+i gives a_(N-i)+a_(N+i)<=2a_N. Unique factorization makes the resulting product inequality strict. Given any fixed M, choose J>M with a_J>max_{j<=M} a_j+1. When lambda is sufficiently small, a_J-lambda J exceeds every a_j-lambda j with j<=M. Every maximizer then exceeds M. Thus such N are unbounded, hence infinite. No uniqueness of the maximizer is required.

Take N>=2 throughout the construction. The extra bound 2p_(2N-1)<p_N^2 is already the i=N-1 instance of the balanced inequality. The manuscript's separate asymptotic proof of this extra bound is valid but unnecessary. N=1 is excluded because the two intended endpoint primes coincide and would not provide two distinct elements. Removing this finite exceptional index does not affect infinitude.

## Correct graph lemma and explicit defect in the manuscript

For a selected edge family F in a path with at most one loop at each vertex, include all vertices incident to selected edges or selected loops. The selected ordinary edges form a forest on those vertices; a loop-only vertex is an isolated component. Let c be its number of components and ell the total number of selected loops. The exact identity is

|F| - |V(F)| = ell - c.

Consequently F is deficient precisely when ell>c. Deficiency implies that at least one component contains two or more selected loops. The converse for the whole family F is false: positive excess in one component can be canceled by a loopless component.

A minimal counterexample uses the ambient path v0-v1-v2-v3 and allowed loops at v0,v1. Select those two loops and the ordinary edges v0v1 and v2v3, omitting v1v2. One component has two loops, but |F|=4=|V(F)|, so F is not deficient. This directly refutes the manuscript's “if and only if” on page 3. Replacing that sentence by the identity above repairs it.

The claimed minimum-support formula (7) remains correct. For a given allowed loop set T with at least two vertices, put d=min{|i-j|: v_i,v_j in T, i!=j}. A deficient family must have a component containing two loops, so its support contains the entire interval between that pair and has at least d+1 vertices. Conversely the interval connecting a closest pair, together with its two loops, has d+2 edges on d+1 vertices and is deficient. Thus the minimum support is exactly d+1. This argument uses only the valid implication, and the construction supplying the reverse bound is a single component.

## Audit of the exact sharp construction

Choose any balanced N>=2, set P=p_N, n=P^2-1, and m=N-1. Then P-1<sqrt(n)<P, so exactly p1,...,p_(N-1) lie below sqrt(n), and pi(sqrt(n))=m.

The path has the 2N-1 distinct prime vertices

p_(2N-1), p1, p_(2N-2), p2, ..., p_(N+1), p_(N-1), p_N.

Equivalently q0=p_(2N-1), q_i=p_(2N-i-1) for 1<=i<=m-1, q_m=p_N, and the path alternates q0,p1,q1,...,p_m,q_m. All these vertices are distinct; the large vertices have indices N through 2N-1 and the small vertices indices 1 through N-1.

All ordinary edge products lie in [1,n]. The first is 2p_(2N-1)<P^2. The last is p_(N-1)P<P^2. Each internal q_i p_(i+1) is p_(N+h)p_(N-h) with h=N-i-1 in [1,N-2], hence is below P^2; q_i p_i is smaller still. Since these products are integers they are at most P^2-1=n. Each vertex itself is also at most n, since it divides an incident positive edge product. Unique factorization and distinct endpoint pairs ensure all edge products are distinct; none is prime.

Let V be this vertex set and C consist of all 2m ordinary edge products and the two endpoint primes q0,q_m as singleton-support loops. Then |V|=2m+1 and |C|=2m+2. Define

A = C union {q<=n: q prime and q not in V}.

The union is disjoint and |A|=pi(n)+1. This is exactly how the recovered manuscript defines A. In contrast, the indexed discussion sketch says primes outside C; that literal phrase is erroneous because it would add the internal path primes. The manuscript itself does not have this error.

For any B subset A, split B into its core part B0 subset C and its outside primes B1. The supports are disjoint, and |B1|=|P(B1)|. Therefore |B|-|P(B)|=|B0|-|P(B0)|. If B is deficient, so is B0. The corrected graph lemma forces B0 to include both endpoint loops and every edge connecting them, hence B0=C. Thus every deficient B has support at least |V|, whereas C attains it. Hence rho(A)=2m+1, and A has no supporting prime set of any smaller size. This proves the lower bound for both definitions. The exact-r universal upper bound proves equality for both.

Unbounded N give unbounded n=p_N^2-1, and the difference is identically -1 on this subsequence. This rigorously disproves the first-part limit.

## Audit of all stated general-k bounds

All variables h and r in these formulas are integers. The range pi(n)<k<=n is assumed.

1. Equation (8): f(k,n)<=2m+1 for every k>pi(n). Correct, with the direct exact-r proof above. The additional elementary bound f<=pi(n) also holds.

2. Equation (9): f(pi(n)+h,n)>=floor((m-1)/h)+1 for 1<=h<=m-1. Correct. Form the path p1,...,p_m, all of whose adjacent products are <=n. Place h+1 loops at positions floor(j(m-1)/h), 0<=j<=h, using zero-based positions. Consecutive gaps are either floor((m-1)/h) or its ceiling; their minimum is the floor. Distinctness follows because h<=m-1. The core contains m-1 products and h+1 primes, so has m+h distinct integers. Add all primes outside the m path vertices to obtain exactly pi(n)+h elements. Outside prime supports contribute zero excess. The corrected minimum-support formula yields exactly floor((m-1)/h)+1 for this witness. For m<2 the displayed h-range is empty; no division by zero is taken. The construction itself also verifies that its stated k is <=n.

3. Equation (10): along the same infinite subsequence, simultaneously for every 1<=h<=2m, f(pi(n)+h,n)>=floor(2m/h)+1. Correct. The long path has 2m edges on 2m+1 vertices. Select loops at zero-based positions floor(j(2m)/h), j=0,...,h; their minimum gap is floor(2m/h). There are 2m+h+1 distinct core elements and pi(n)-(2m+1) outside primes, giving pi(n)+h. Every loop prime and edge is <=n by the construction already checked. This proves the assertion for the whole integer h-range at each selected n, not merely a separately chosen subsequence for each h. For h=1 it recovers equality. For h=2m every vertex has a loop and the witness's minimum support is 2, as the formula requires.

4. Equation (11): with W_r(n)=#{a<=n: omega(a)>r}, f(k,n)>=1+max{r in Z_{>=0}: W_r(n)>=k}, the empty maximum being -1. Correct. If W_r(n)>=k, choose k distinct such integers. No set of at most r primes supports even one of them, so every witness requires at least r+1 primes. The maximum is finite since omega(a) is bounded for a<=n. At k=n the set of eligible r is empty because omega(1)=0, yielding only the valid bound f>=0. This is a lower bound expressed in a counting function; the manuscript does not estimate that tail throughout k=o(n).

5. The final fixed-h consequence is correct. For each fixed h, m tends to infinity along the balanced-prime subsequence; eventually h<=2m and floor(2m/h)+1 >= 2m/h. Thus f(pi(n)+h,n) is bounded below by a positive h-dependent multiple of pi(sqrt(n)) infinitely often. Together with (8), this gives the stated order on that subsequence, not an asymptotic formula for arbitrary growing h or arbitrary k=o(n).

## Presentation and attribution corrections

The inspected manuscript source omits declarations for its lemma, theorem, and proposition environments, and its displayed PDF has unlabelled theorem statements and repeated references to “Lemma 1”. No source-author code was executed. Inserting theorem-environment declarations and recompiling is an editorial task for the author; this audit uses the source labels lem:upper, lem:prime-growth, lem:balanced, lem:path, thm:sharp, prop:basic-estimates, prop:special-h, and prop:omega to identify results unambiguously.

Cite Erdős, “Some applications of graph theory to number theory” (1970), pp. 138–140, for the problem, its previously known upper bound and asymptotic constructions: https://www.renyi.hu/~p_erdos/1970-20.pdf . Cite Pomerance (1979) for the balanced-prime theorem. Credit the current disproof construction to the prior Price/GPT-5.5 Pro claim; Sothanaphan's 19 May 2026 explanation independently identifies its relationship to Erdős. Neither this audit nor the attribution establishes a complete priority search.

## Verification and stopping scope

The original audit's independent standard-library checks verified the graph counterexample; the corrected minimum-support formula for every loop subset on paths of 1 through 6 edges (219 loop sets); 100308 finite group-count instances of the exact-r upper-bound argument; the sharp construction for all 49 balanced N between 2 and 200; and 12 selected general-h cases. For n=24, A={5,11,13,14,15,17,19,21,22,23}, all 512 prime subsets were checked and the minimum support is 5. The explicit mathematical witness is retained here; raw enumerated check arrays are not. Normal Python, -O and -OO recorded identical summary bytes. These finite checks are corroboration. Infinitude and all unbounded statements follow from the proofs above, not finite testing.

Historical revision identity remains unverified. The mathematical audit accepts the first-part disproof and the listed inequalities only with the explicit repairs and scope limitations above. The original manuscript as written is not accepted without those repairs. The broad general-k estimation question is only partially addressed. No novelty, exhaustive priority search, external peer review or formal proof certification is claimed.
