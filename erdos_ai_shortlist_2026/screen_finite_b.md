# Screen B: falsifiable problems and finite-certificate candidates

**Snapshot:** 2026-07-24 (America/Los_Angeles)
**Scope:** Problems #548, #583, #617, #628, #699, #723, #743, #779, #982, #993, #1020, #1041, and #1082, plus a small database-wide search for stronger alternatives. Problem #84 was excluded. This was a screening exercise only; no solution attempt was made.

## Bottom line

None of the 13 assigned problems is a clean top-ten “dispatch an AI now and plausibly be first” choice.

- **Best assigned problem:** [#583](https://www.erdosproblems.com/583), because its statement is elementary, it has no proof claim or listed worker on the database, and a counterexample would be finite. It is nevertheless a 55-year-old conjecture with no useful finite cutoff, a substantial theorem gap, and a live July 2026 SciNet effort.
- **Best finite-witness target:** [#993](https://www.erdosproblems.com/993), because one explicit tree with a non-unimodal independence sequence would settle it negatively and verification is easy. The computational frontier is already beyond an M1 Pro/16 GB machine, however, and several public AI/computational efforts are active.
- **Best alternate found:** [#273](https://www.erdosproblems.com/273), a covering-system existence problem. A positive answer admits a finite, independently checkable certificate. It is still only a cautious reserve candidate: a July 2026 AI-assisted search established meaningful necessary conditions and reported unsuccessful searches.

Thus this screen contributes **one conditional shortlist candidate (#273)** and at most **three reserves (#583, #993, #1210)**. It would be misleading to promote any of them as likely easy.

The site’s labels are not difficulty certifications: “falsifiable” only says that a finite counterexample could disprove the statement. It does not provide a finite search bound, and the site notes that statuses represent the maintainer’s current assessment rather than an exhaustive literature determination.

## Ranked candidates

| Rank | Problem | Why it is comparatively tractable | Decisive certificate | Competition / obstacle | Recommendation |
|---:|---|---|---|---|---|
| 1 | [#273](https://www.erdosproblems.com/273) | Elementary covering congruences; constructive “yes” target; amenable to exact-cover/SAT/ILP and modular pruning | A finite list of distinct congruences, all moduli \(p-1\) with \(p\ge 5\) prime, plus an exact coverage check | A [July 2026 thread update](https://www.erdosproblems.com/forum/thread/273) reports AI-assisted necessary conditions, that moduli from primes \(p\le877\) cannot suffice, and unsuccessful searches | **Conditional dispatch (B-/C+)**; strongest item in this screen, but not low-hanging fruit |
| 2 | [#583](https://www.erdosproblems.com/583) | Very short graph statement; small cases and graph classes can be searched with SAT/ILP | Counterexample graph plus a checkable certificate that no decomposition into \(\lceil n/2\rceil\) paths exists; or a complete proof | Famous Gallai conjecture, no finite cutoff, best general theorem still materially weaker; [SciNet task](https://api.scinet.pub/p/a44c567c-217d-4fb6-9daf-8af53f86b33f) opened 2026-07-05 | **Reserve (C)**; best of the assigned set, not a confident first-to-solve target |
| 3 | [#993](https://www.erdosproblems.com/993) | A negative solution is a single finite tree; its independence polynomial is easy to recompute | Explicit tree and coefficient list showing a decrease followed by an increase | Exhaustive verification already reaches 29 vertices; roughly 14.8 billion unlabeled trees occur at 30 vertices; [thread](https://www.erdosproblems.com/forum/thread/993) and public PatternBoost work show active competition | **Reserve (C)** only for structured/generative search, not exhaustive enumeration |
| 4 | [#1210](https://www.erdosproblems.com/1210) | Self-contained pairwise-coprime extremal inequality; formalized; two public “tractable” votes | A proof with an absolute \(O(1)\) constant, or a family contradicting every such constant | A tempting sieve argument was rejected; the problem touches the hard prime-interval problem #855, and a [June 2026 preprint](https://arxiv.org/abs/2606.17955) studies its average order | **Reserve (C-)**; clean statement but active and not truly finite-searchable |
| 5 | [#982](https://www.erdosproblems.com/982) | A counterexample would be a finite point configuration | Exact coordinates and exact distance-equality/convexity verification | Continuous realization search; current lower bound is far from the conjectured \(n/2\); one listed worker | **Do not use for the primary ten** |

## Assigned-problem audit

### #548 — Erdős–Sós tree embedding

[Problem](https://www.erdosproblems.com/548) · [discussion](https://www.erdosproblems.com/forum/thread/548)

For \(n\ge k+1\), every \(n\)-vertex graph with at least \((k-1)n/2+1\) edges should contain every tree on \(k+1\) vertices. The database currently labels it falsifiable, with no proof claim or listed worker. Numerous substantial cases are known: paths, stars, several host-graph classes, spiders, \(k\le 9\), and host orders close to \(k\). A proof by Ajtai–Komlós–Simonovits–Szemerédi was announced, but a complete public proof is not available.

There is no effective finite cutoff. Even testing one \((n,k)\) naïvely ranges over \(2^{\binom n2}\) host graphs and all \(k\)-edge trees. Its fame, the announced proof, and the depth of existing partial theory make it a poor “be first” target. **Reject.**

### #583 — Gallai’s path-decomposition conjecture

[Problem](https://www.erdosproblems.com/583) · [discussion](https://www.erdosproblems.com/forum/thread/583)

Every connected \(n\)-vertex graph should have its edge set partitioned into at most \(\lceil n/2\rceil\) paths. Known results cover trees and several broad graph classes, while the general bound remains weaker (the page records a \(\lceil2n/3\rceil\)-type bound in the relevant general setting). A 2026 result added a further induced-subgraph class.

A small counterexample could be found by graph generation followed by an exact path-decomposition solver. To be conclusive, the output must include more than a graph: it needs a verifiable optimization/UNSAT certificate showing that \(\lceil n/2\rceil\) paths cannot suffice. No theorem bounds a counterexample’s order. The database itself shows only three comments and no claim/worker, but a [public SciNet task](https://api.scinet.pub/p/a44c567c-217d-4fb6-9daf-8af53f86b33f) began on 2026-07-05. **Best assigned reserve, not a strong shortlist item.**

### #617 — balanced edge-colourings

[Problem](https://www.erdosproblems.com/617) · [proof claims](https://www.erdosproblems.com/forum/thread/617/proof-claims)

For \(r\ge3\), every \(r\)-edge-colouring of \(K_{r^2+1}\) should contain \(r+1\) vertices whose induced clique omits at least one colour. The cases \(r=3,4\) are known; the analogous assertion on \(r^2\) vertices fails infinitely often.

This initially looked like a good fixed-parameter SAT target, but it is now crowded. The live page lists four workers and **five public fixed-case proof claims submitted 2026-07-18 through 2026-07-21**, covering \(r=5\), \(6\), \(7\), \(8\), and \(9\). For scale, a counterexample search at \(r=5\) has 325 edge-colour variables and 230,230 six-vertex subsets, yielding about 1.15 million basic colour-presence constraints before symmetry machinery. A fixed-\(r\) UNSAT result also would not prove the universal statement. **Exclude because the computationally accessible cases are already claimed and actively worked.**

### #628 — Erdős–Lovász Tihany conjecture

[Problem](https://www.erdosproblems.com/628) · [discussion](https://www.erdosproblems.com/forum/thread/628)

If \(\chi(G)=k>\omega(G)\) and \(a,b\ge2\) with \(a+b=k+1\), there should be disjoint subgraphs of chromatic number at least \(a\) and \(b\). The \(a=b=3\) case and important graph classes are known; a July 2026 thread update gives another class.

This is a major structural graph-colouring conjecture with no finite cutoff. Exhaustive graph search additionally requires exact chromatic-number and subgraph-colouring certificates. **Reject as too deep and too active.**

### #699 — common prime divisors of binomial coefficients

[Problem](https://www.erdosproblems.com/699) · [proof claims](https://www.erdosproblems.com/forum/thread/699/proof-claims)

For \(1\le i<j\le n/2\), there should be a prime \(p\ge i\) dividing both \(\binom ni\) and \(\binom nj\). Computation has found no counterexample through \(n=10^7\). More importantly, the live page lists three workers and an **accepted partial proof claim**: a GPT-5.6-assisted argument posted 2026-07-18 proves the assertion when \(j\le3i/2\) or \(n=2j\). The page also records a prior invalid proof attempt.

Individual triples are inexpensive to test, but negative computation has no closing bound and the easy region is now publicly occupied. **Exclude for competition and strong negative evidence.**

### #723 — prime-power order of finite projective planes

[Problem](https://www.erdosproblems.com/723) · [discussion](https://www.erdosproblems.com/forum/thread/723)

Must the order of every finite projective plane be a prime power? The conjecture is verified through order 11; order 12 is the first open case. An order-12 plane would have 157 points and lines, each line containing 13 points.

The nonexistence of order 10 required a historically enormous computer search, and order 12 is much larger. A construction would be a finite certificate, but there is no evidence that one exists; a nonexistence certificate is far beyond local hardware. **Reject.**

### #743 — Ringel-type tree packing

[Problem](https://www.erdosproblems.com/743) · [discussion](https://www.erdosproblems.com/forum/thread/743)

Given trees \(T_i\) on \(i\) vertices for \(i=2,\ldots,n\), can they be packed edge-disjointly into \(K_n\)? The conjecture is known through \(n=9\) and in several broad regimes.

Although the database’s formal proof-claim count is zero, the discussion contains a public full-proof claim, [arXiv:2410.13840](https://arxiv.org/abs/2410.13840), together with community reports of serious gaps. Under a “no already claimed problem” rule, a claim in a preprint counts even if flawed. **Exclude.**

### #779 — primes near a primorial

[Problem](https://www.erdosproblems.com/779) · [discussion](https://www.erdosproblems.com/forum/thread/779)

Let \(P=\prod_{i=1}^n p_i\), \(n>1\). Is there a prime \(p\) with \(p_n<p<P\) such that \(P+p\) is prime? It has been checked for \(n\le1000\), and heuristics make failure look extremely unlikely.

The direct disproof search would have to exclude primes over an interval whose endpoint is the primorial \(P\); computation does not scale. The discussion notes that even a weaker consequence is tied to difficult prime-pair phenomena. **Reject.**

### #982 — distinct distances from a vertex of a convex polygon

[Problem](https://www.erdosproblems.com/982) · [discussion](https://www.erdosproblems.com/forum/thread/982)

Every convex \(n\)-gon should have a vertex from which at least \(\lfloor n/2\rfloor\) distinct distances occur. The regular polygon is sharp. The best recorded linear lower bound is only about \((13/36+1/22701)n-O(1)\).

A counterexample is finite but lives in a continuous realization space. Numerical coordinates are not conclusive without exact convexity and distance-equality certificates. There is one listed worker and no finite-order reduction. **Low reserve only; reject for the main list.**

### #993 — unimodality of the independence polynomial of a tree

[Problem](https://www.erdosproblems.com/993) · [discussion](https://www.erdosproblems.com/forum/thread/993)

The numbers of independent sets of each size in every tree (equivalently, every forest) should form a unimodal sequence. A counterexample tree would be immediately checkable by dynamic programming.

This is the assigned item best suited to generative counterexample search, but the obvious exhaustive route is exhausted locally: all trees through 29 vertices have been checked, including 2,023,443,032 trees at order 28 and 5,469,566,585 at order 29. Order 30 has about 14.8 billion unlabeled trees, unsuitable for this 16 GB machine while other research runs. The thread links active PatternBoost/AI work and public datasets; sampled non-log-concave trees through much larger orders have remained unimodal. **Reserve only for a new structural generator, not brute force.**

### #1020 — Erdős matching conjecture

[Problem](https://www.erdosproblems.com/1020) · [discussion](https://www.erdosproblems.com/forum/thread/1020)

For an \(r\)-uniform family on \(n\) vertices with no \(k\) pairwise disjoint members, the proposed maximum is
\[
\max\left\{\binom{rk-1}{r},\ \binom nr-\binom{n-k+1}{r}\right\}.
\]
The \(r=2,3\) cases and many parameter ranges are known.

The thread records a full-proof preprint claim with an identified crucial error, which alone violates the no-claimed-problem criterion. The area is also moving quickly: [arXiv:2605.26060](https://arxiv.org/abs/2605.26060) proves a large-parameter \(r=4\) range with exact finite-board certificates, and [arXiv:2602.19230](https://arxiv.org/abs/2602.19230) gives further \(r=4\) progress. Prerequisites are substantial extremal set theory. **Exclude.**

### #1041 — short paths in polynomial lemniscates

[Problem](https://www.erdosproblems.com/1041) · [discussion](https://www.erdosproblems.com/forum/thread/1041)

If all roots of a polynomial lie in the open unit disk, must two roots be joinable by a path of length less than 2 lying in \(\{|f|<1\}\)? The page gives an equivalent component formulation.

The problem has 47 comments and high AI attention. A March 2026 AI-assisted full-proof claim was publicly withdrawn after a fatal topological error was found; the author agreed that a key proposition was false. Even setting the claim rule aside, this requires advanced complex analysis, geometry, and topology, while numerical pictures cannot certify the universal result. **Exclude.**

### #1082 — few-distance point sets

[Problem](https://www.erdosproblems.com/1082) · [discussion](https://www.erdosproblems.com/forum/thread/1082)

For \(n\) planar points with no three collinear: (1) must the set determine at least \(\lfloor n/2\rfloor\) distances, and (2) must some point determine at least \(\lfloor n/2\rfloor\) distances to the others?

The page explicitly records that the stronger second question is already false via an eight-point construction; only the first remains open. It also has 21 comments and prior AI rediscovery activity. Because the numbered entry is partially resolved and visibly crowded, **exclude.**

## Alternate database survey

### #273 — covering systems with moduli one below primes

[Problem](https://www.erdosproblems.com/273) · [discussion](https://www.erdosproblems.com/forum/thread/273)

The problem asks for a distinct-modulus covering system in which every modulus is \(p-1\) for a prime \(p\ge5\). Selfridge’s construction works if \(p=3\) is allowed, so the exclusion of modulus 2 is essential.

Why it beats the assigned set:

- A positive solution is a finite object and can be checked independently.
- Search variables and constraints are discrete and naturally support exact cover, SAT, ILP, or recursive density arguments.
- The mathematical prerequisites are moderate: congruences, covering systems, CRT compatibility, and exact certification.

Why it is only conditional:

- A 2026-07-12 update reports AI-assisted necessary conditions.
- In particular, the eligible moduli arising from primes through 877 cannot cover by themselves, so any solution must reach beyond that range.
- The same update reports unsuccessful computational searches. There is therefore visible competition, although no proof claim or listed worker appears on the problem header.

If dispatched, the AI should target a **constructive positive certificate**, not an unbounded nonexistence search.

### #1210 — shifted reciprocal sums over pairwise-coprime sets

[Problem](https://www.erdosproblems.com/1210) · [discussion](https://www.erdosproblems.com/forum/thread/1210)

For pairwise coprime \(A\subset[1,n)\), the requested bound is
\[
\sum_{a\in A}\frac1{n-a}\le \sum_{p<n}\frac1p+O(1).
\]
It is formalized and has two public tractability votes, no proof claim, and no listed worker. Its surface form is unusually self-contained.

However, the discussion rejects a natural sieve proof and explains a connection to the difficult prime-interval problem #855. The new preprint [“An Average-Order Theorem for a Shifted Pairwise-Coprime Extremal Problem”](https://arxiv.org/abs/2606.17955) is direct evidence of current competition and of the gap between average-order progress and the pointwise claim. It is a reserve, not a better bet than #273.

## Practical recommendation to the parent screen

1. Carry **#273** forward as a conditional candidate, explicitly noting the July 2026 search barrier and competition.
2. Keep **#583** and **#993** only as backups if the final ten needs breadth; neither deserves a high confidence score.
3. Keep **#1210** as a proof-oriented backup only.
4. Do not nominate #617, #699, #743, #1020, or #1041 under the user’s “not already claimed” rule.
5. Do not nominate #1082 because one of its two questions is already refuted.
6. Reject #548, #628, #723, and #779 as famous/deep problems whose finite certificates do not translate into a plausible bounded search.

## Follow-up: skeptical screen of quiet ordinary-open entries

**Additional snapshot:** 2026-07-24. I checked [#385](https://www.erdosproblems.com/385), [#430](https://www.erdosproblems.com/430), [#463](https://www.erdosproblems.com/463), [#585](https://www.erdosproblems.com/585), [#611](https://www.erdosproblems.com/611), [#789](https://www.erdosproblems.com/789), [#893](https://www.erdosproblems.com/893), and [#917](https://www.erdosproblems.com/917). Their live headers all say `OPEN`, with zero comments, zero claimed proofs, and no listed current worker. That superficial quietness does not survive scrutiny.

### Verdict

**None should displace a bottom member of a tractability-first top ten.** The least implausible sleeper is #789, but it is only a watchlist item: it asks for an asymptotic exponent across arbitrary integer sets, and the recorded \(n^{1/3}(\log n)^{1/3}\)-to-\(n^{1/2}\) gap has survived since the 1960s–70s. #893 has the clearest recent runway, but a 2025 paper is already directly attacking it and reduces the remaining question to difficult Mersenne-factor behavior.

| Order | Problem | Live mathematical position and recent activity | Conclusive route | Skeptical rating |
|---:|---|---|---|---|
| 1 | [#789](https://www.erdosproblems.com/789) | For every \(n\)-element \(A\subset\mathbb Z\), seek the largest guaranteed \(B\subseteq A\) such that equal subset sums have equal cardinalities. Known \((n\log n)^{1/3}\ll h(n)\ll n^{1/2}\); targeted search found no newer direct improvement beyond the classical Erdős–Choi and Straus bounds. Formalized. | A matching asymptotic upper/lower theory or a major exponent improvement; finite computation on selected sets cannot settle the worst-case asymptotic | **Best of eight, but watchlist only (C-/D+)** |
| 2 | [#893](https://www.erdosproblems.com/893) | For \(f(n)=\sum_{k\le n}\tau(2^k-1)\), ask whether \(f(2n)/f(n)\) has a limit. [Kovač–Luca (2025)](https://arxiv.org/abs/2506.04883) proved the ratios unbounded, gave conditional routes to divergence to \(+\infty\), and supplied numerical evidence. The remaining alternatives are divergence to infinity versus oscillation without a limit. The paper’s author marks the problem difficult on the site. | A proof of divergence to infinity, or two rigorously controlled subsequences; more finite factorization data is not decisive | **No: active and arithmetic-depth heavy** |
| 3 | [#611](https://www.erdosproblems.com/611) | If every maximal clique has at least \(cn\) vertices, ask whether the clique-transversal number is \(o_c(n)\), and estimate the threshold forcing \(\tau(G)<(1-c)n\). The old general bounds on the page remain far apart; targeted search found modern work on clique-transversal algorithms/variants, but no direct resolution of this asymptotic question. | A universal probabilistic/structural proof, or an infinite counterexample family with linear maximal cliques and linear transversal number | **No: genuinely quiet, but broad and non-finite** |
| 4 | [#585](https://www.erdosproblems.com/585) | Maximize the edges in an \(n\)-vertex graph with no two edge-disjoint cycles on the same vertex set. Lower bound \(\gg n\log\log n\); [Chakraborti–Janzer–Methuku–Montgomery (2024)](https://arxiv.org/abs/2404.07190) proved an \(n(\log n)^{O(1)}\) upper bound using sublinear expanders, absorption, and new regularization machinery. | Matching asymptotic construction and upper bound; any single finite graph only improves a lower-bound data point | **No: recent major progress, sophisticated remaining gap** |
| 5 | [#463](https://www.erdosproblems.com/463) | Ask whether some \(f(n)\to\infty\) guarantees, for every large \(n\), a composite \(m\) with \(n+f(n)<m<n+p(m)\), where \(p(m)\) is the least prime factor. The page links it to #385; a targeted search found no direct new theorem. | Uniform short-interval control of composites by least prime factor; no bounded verification route | **No: analytic-number-theory depth with no certificate route** |
| 6 | [#385](https://www.erdosproblems.com/385) / [#430](https://www.erdosproblems.com/430) | The first question of #385 and all of #430 are explicitly equivalent. #385 asks whether \(F(n)=\max_{m<n,\ m\text{ composite}}(m+p(m))\) eventually exceeds \(n\), and whether the excess tends to infinity. In his [2024 analysis](https://terrytao.wordpress.com/2024/08/19/erdos-problem-385-the-parity-problem-and-siegel-zeroes/), Tao says present approaches hit the parity barrier and that resolution likely needs at least enough of a breakthrough to exclude Siegel zeros; he marks both entries difficult on the site. | A major uniform sieve/inverse-sieve theorem; checking any finite range proves nothing asymptotic | **Strong reject** |
| 7 | [#917](https://www.erdosproblems.com/917) | The displayed multi-question entry is misleadingly “open”: Toft already proved \(f_k(n)\gg_k n^2\), and Stiebitz disproved the displayed general asymptotic when \(k\not\equiv0\pmod3\). What remains includes \(f_6(n)\sim n^2/4\) and the correct constants. [Luo–Ma–Yang (2023)](https://arxiv.org/abs/2301.01656) obtained the first general upper-bound improvement in 35 years. A [SciNet task](https://api.scinet.pub/p/23c74681-0438-4d48-89f5-d09cfe9d0a5d) was opened on 2026-07-14 specifically for AI/enumeration attacks. | Infinite construction families plus exact criticality proofs, or new structural extremal bounds; small-\(n\) enumeration is only partial progress | **Strong reject: partly settled, deep, and externally active** |

### Per-problem notes

- **#385 and #430:** Treat as one problem, not two shortlist slots. #430 defines a decreasing sequence \(a_1=n-1\), taking each next \(a_k\) as the greatest smaller integer all of whose prime factors exceed \(n-a_k\), and asks whether an eventually composite term must occur. The database proves its equivalence to the first half of #385. Tao’s parity-barrier diagnosis is unusually strong negative expert evidence; zero forum comments are irrelevant.
- **#463:** It is self-contained but not computationally falsifiable in the useful sense. A finite computation can illustrate candidate gap functions, but the quantifiers “there is \(f(n)\to\infty\)” and “for all large \(n\)” demand an asymptotic theorem.
- **#585:** The 2024 paper calls its result a resolution up to a polylogarithmic factor, but the database correctly keeps the exact extremal-growth question open. Closing \(\log\log n\) versus \((\log n)^C\) is not a finite-certificate task.
- **#611:** Even verifying \(\tau(G)\) can be algorithmically awkward because a graph may have exponentially many maximal cliques. More importantly, one finite extremizer cannot answer the asymptotic statement. Its lack of recent direct progress makes it quiet, not tractable.
- **#789:** The formalization clarifies that the sums are over subsets, so equal sums are allowed only for subsets of the same size. It is a clean additive-combinatorics prompt and the one entry worth retaining on a long watchlist. Nevertheless, “estimate \(h(n)\)” is underspecified as a finish line unless the dispatched task chooses a concrete target such as either known endpoint being the correct order; that target would still be a decades-old exponent problem.
- **#893:** The 2025 paper already proves that no finite limit exists and isolates concrete conjectural sufficient conditions for an infinite limit. This is useful scaffolding for research, but it also means visible expert competition and a bottleneck involving prime factors of cyclotomic/Mersenne values.
- **#917:** Zero comments on Erdős Problems misses both the current literature and current AI competition. It also violates the spirit of “not already solved/claimed” because two of the three displayed questions are respectively solved and partly disproved.

**Net recommendation:** add none. If the parent shortlist needs one extra ultra-quiet backup, use **#789 only**, below #273, #583, #993, and #1210, and label it a proof-oriented long shot rather than a finite-search candidate.
