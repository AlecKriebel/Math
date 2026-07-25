# Screen A: finite-one-sided Erdős problems

**As of:** 2026-07-24 (America/Los_Angeles)
**Scope:** #7, #23, #64, #97, #106, #107, #114, #128, #167, #242, #287, #307, #364, #366, #375, #398, #458, #488, #647, #672, #835. Problem #84 was not considered.
**Sources:** the live problem pages and public discussion threads at [erdosproblems.com](https://www.erdosproblems.com/). No outreach was performed.

The site's word “verifiable” means only that a positive answer could be certified by one finite example; “falsifiable” means only that a negative answer could be certified by one finite counterexample. It does **not** mean that the relevant finite search is bounded or realistically small. The site also explicitly warns that its open status is the owner's current belief and not a substitute for a literature search. Forum claims below are identified as such and should not be treated as vetted results.

## Bottom line

This batch contains **no high-confidence fire-and-forget problem**. The best three are #106, #23, and #128: each has a concrete, exactly checkable finite witness format at a plausible first search scale. They are still serious research bets, not routine computations. If the overall project needs only ten problems, I would take at most these three from this screen before drawing from other screens.

The next tier (#7, #488, #64) has an attractive exact-search formulation but either a very hot race, a frontier already pushed far beyond naive computation, or an unknown witness scale. #307 and #835 are finite in a literal sense but already too large for direct search on the available 16 GB M1 Pro. #114 has a coherent finite-complement program but active competitors already own the computational pipeline. #167 has low visible site activity but is the mature and famously hard Tuza conjecture.

## Ranked dispatch list

| Rank | Problem | Why it survives the screen | Main reason it may fail | Dispatch verdict |
|---:|---|---|---|---|
| 1 | [#106](https://www.erdosproblems.com/106) | The first unsettled case exposed by the remarks is the concrete \(k=3\) case: ten squares. A disproof is one explicit packing with total side length \(>3\), checkable by exact coordinates/inequalities. | Continuous non-convex geometry and rotations make exhaustive certification much harder than a graph SAT instance; two users say they are working on it. | **Best of this batch.** Assign a geometry/optimization AI to hunt a certified \(k=3\) construction, not to attack all \(k\) abstractly. |
| 2 | [#23](https://www.erdosproblems.com/23) | For fixed \(n\), a witness is a finite triangle-free graph on \(5n\) vertices whose minimum edge-bipartization number is \(>n^2\). This is an exact SAT/MaxSAT or graph-enumeration target, and a found graph is easy to audit. | No bound says a counterexample is small; the best theorem is already close (\(1.064n^2\)), suggesting subtle structure rather than a tiny missed graph. One user is marked working. | **Good finite counterexample hunt.** Begin at small \(n\) with proof-producing optimization and symmetry breaking. |
| 3 | [#128](https://www.erdosproblems.com/128) | For fixed order \(n\), search for a triangle-free graph whose every \(\lfloor n/2\rfloor\)-vertex subset spans \(>n^2/50\) edges. A cutting-plane MILP/CP-SAT formulation has exact witness verification. | This is a sharp extremal problem with sophisticated partial results; two users mark it tractable, working, and being formalised, so the race is active. | **Good but competitive.** A finite counterexample search is more plausible than asking an AI for the full proof. |
| 4 | [#7](https://www.erdosproblems.com/7) | Fixing the odd l.c.m. \(L\) turns the problem into an exact-cover/SAT problem on \(\mathbb Z/L\mathbb Z\), with distinct moduli among divisors of \(L\). The remarks give strong filters: \(L\) must be divisible by \(9\) or \(15\); the thread notes \(L\) must be odd abundant, hence \(L\ge945\). | Twenty-one comments, two users marked working, one formalising, and multiple flawed AI/Lean proof attempts. Witness scale is unbounded and the modern sieve theory is nontrivial. | **Speculative construction search.** Worth a bounded \(L\)-by-\(L\) exact-cover program, but not a likely quick solve. |
| 5 | [#488](https://www.erdosproblems.com/488) | For fixed \(A\), counts of the union of multiples are exact and periodic modulo \(\operatorname{lcm}(A)\). The newest thread gives a short claimed proof for \(|A|=2\), leaving primitive sets of size at least \(3\) as the first counterexample search. | This is the hottest thread here: 30 comments, two users marked working, extensive AI-assisted special cases and searches, and Tao remarks that even weakened versions are nontrivial. A counterexample has not appeared in the posted searches. | **Technically attractive, poor first-mover odds.** Dispatch only if racing immediately with a distinct exhaustive primitive-triple search. |
| 6 | [#64](https://www.erdosproblems.com/64) | A counterexample is one finite graph of minimum degree \(3\) with no cycle of length \(4,8,16,\ldots\). Cubic graph/SAT generation plus certified cycle exclusion is concrete; the thread says a cubic counterexample has at least 30 vertices. | Three users mark themselves working; the problem carries a \$1000 prize and has been studied across many graph classes. Naive enumeration at order 30 is already far beyond laptop scale. | **Possible targeted SAT project, not naive enumeration.** |
| 7 | [#307](https://www.erdosproblems.com/307) | A solution is an exact rational identity between two finite prime reciprocal sums. Verification is trivial once \(P,Q\) are found, and modular/factor constraints can drive a branch-and-bound search. | The site proves \(P,Q\) are disjoint and \(|P\cup Q|\ge60\), so the first search space is already enormous. Three users are marked working; the thread calls the natural factorisation approach computationally challenging. | **Long-shot exact arithmetic search.** More memory/parallel hardware would materially help. |
| 8 | [#835](https://www.erdosproblems.com/835) | A positive coloring is a finite certificate. Recent forum reductions leave the first plausible case at \(k=16\), connecting it to a highly constrained large set of Steiner systems; structure and symmetry may permit a design search. | \(J(32,16)\) has \(\binom{32}{16}=601{,}080{,}390\) vertices, so direct SAT is impossible on 16 GB. Ruling out one \(k\) does not solve the existential question. Recent comments show active mathematical progress even though no user is marked working. | **Only with a symmetry/design breakthrough.** This is where substantially larger hardware could help, but hardware alone is insufficient. |
| 9 | [#114](https://www.erdosproblems.com/114) | Tao proved the conjecture for all sufficiently large degrees, so there is a conceptual finite complement. Recent forum claims certify degrees through \(14\); degree \(15\) is the first posted computational gap. A counterexample at any remaining degree settles the problem negatively. | The high-degree threshold is not made explicit on the site, equality of real curve lengths complicates decidability, and three users are working. One team already has interval-arithmetic branch-and-bound infrastructure. | **Do not race unless reusing a fundamentally better certificate method.** |
| 10 | [#167](https://www.erdosproblems.com/167) | A disproof is one graph with triangle transversal number \(>2\) times its edge-disjoint triangle packing number. Both quantities admit exact integer-programming certificates for a fixed graph, and the site shows no current worker. | This is Tuza's long-standing conjecture with a large external literature; low site activity is misleading. There is no plausible order bound for a counterexample. | **Theory-heavy backup, not a tractable finite search.** |

### Hardware note

More RAM/cores would materially improve bounded searches for #7, #23, #64, #128, and #307. It would be most noticeable for proof-producing SAT enumeration and prime-subset branching. For #835, the raw \(k=16\) instance is so large that even a large workstation does not remove the need for a new symmetry or design-theoretic reduction.

## Detailed verification of the top ten

### 1. Problem #106 — rotated square packing

- **Exact current statement:** “Draw \(n\) squares inside the unit square with no common interior point. Let \(f(n)\) be the maximum possible sum of the side-lengths of the squares. Is \(f(k^2+1)=k\)?”
- **Current site label:** **FALSIFIABLE**, open; zero claimed proofs. [Problem](https://www.erdosproblems.com/106) · [discussion](https://www.erdosproblems.com/forum/discuss/106?order=newest)
- **Remarks/status that matter:** Erdős proved \(f(2)=1\), and Newman proved \(f(5)=2\), so the first exposed case is \(f(10)=3\). The axis-parallel analogue \(g(k^2+1)=k\) has been proved, including its more general exact formula. Praton's result makes the stated conjecture equivalent to a larger family of exact formulas. Page last edited 2026-03-06.
- **Finite attack:** optimize ten square centers, side lengths, and angles inside the unit square under disjoint-interior constraints. A strict objective \(>3\) gives numerical slack; convert a numerical hit into rational/algebraic coordinates and verify the separation inequalities exactly.
- **Prerequisite load:** medium—computational geometry, nonlinear optimization, exact real algebra/interval arithmetic. No deep number theory.
- **Visible competition:** 2 comments; Jineon Baek and Vugar Guliyev are marked currently working; Baek marks it difficult. No posted attack on the rotated \(k=3\) case.

### 2. Problem #23 — triangle-free edge bipartization

- **Exact current statement:** “Can every triangle-free graph on \(5n\) vertices be made bipartite by deleting at most \(n^2\) edges?”
- **Current site label:** **FALSIFIABLE**, open; zero claimed proofs. [Problem](https://www.erdosproblems.com/23) · [discussion](https://www.erdosproblems.com/forum/discuss/23?order=newest)
- **Remarks/status that matter:** a blow-up of \(C_5\) makes \(n^2\) sharp. Balogh–Clemen–Lidický prove \(1.064n^2\) deletions suffice. Page last edited 2026-01-18.
- **Finite attack:** for each small \(n\), encode triangle-freeness and require \(|E|-\operatorname{maxcut}(G)>n^2\). This can be handled by SAT/MaxSAT with cut-separation, or canonical graph generation plus an exact max-cut certificate.
- **Prerequisite load:** medium—extremal graph theory and exact combinatorial optimization.
- **Visible competition:** 3 comments, but no substantive attempted solution in the thread; Sam Petkov is marked interested, currently working, and regards it as difficult.

### 3. Problem #128 — sparse halves in triangle-free graphs

- **Exact current statement:** “Let \(G\) be a graph with \(n\) vertices such that every induced subgraph on \(\geq\lfloor n/2\rfloor\) vertices has more than \(n^2/50\) edges. Must \(G\) contain a triangle?”
- **Current site label:** **FALSIFIABLE**, open; zero claimed proofs. [Problem](https://www.erdosproblems.com/128) · [discussion](https://www.erdosproblems.com/forum/discuss/128?order=newest)
- **Remarks/status that matter:** blow-ups of \(C_5\) and the Petersen graph show sharpness. Known positive results cover constants \(1/16\), \(27/1024\), and several density regimes, but not \(1/50\). Page last edited 2025-10-31.
- **Finite attack:** for a fixed \(n\), use edge variables, triangle constraints, and a separation oracle that repeatedly finds a sparsest \(\lfloor n/2\rfloor\)-vertex induced subgraph. A counterexample graph plus exhaustive half-set certificate is conclusive.
- **Prerequisite load:** medium-high—extremal graph theory/flag-algebra context plus MILP or CP-SAT.
- **Visible competition:** 5 comments; Sam Petkov and Aurelien Col are both marked working, tractable, formalisable, and formalising. The public comments themselves are bibliographic/clarificatory rather than progress reports.

### 4. Problem #7 — odd distinct covering system

- **Exact current statement:** “Is there a distinct covering system all of whose moduli are odd?”
- **Current site label:** **VERIFIABLE**, open; zero claimed proofs; \$25 listed (with the remarks reporting Selfridge's separate \$2000 offer for an explicit example). [Problem](https://www.erdosproblems.com/7) · [discussion](https://www.erdosproblems.com/forum/discuss/7?order=newest)
- **Remarks/status that matter:** the squarefree version is impossible. Any odd example's l.c.m. must be divisible by \(9\) or \(15\). A forum note gives the elementary necessary condition that the odd l.c.m. \(L\) be abundant, hence \(L\ge945\). Page last edited 2026-01-22.
- **Finite attack:** enumerate promising odd abundant \(L\); choose distinct divisor moduli \(m\mid L\) and one residue class for each, requiring every residue modulo \(L\) to be covered. Use exact-cover/SAT with automorphism breaking and density/sieve cuts.
- **Prerequisite load:** medium-high—covering systems and exact-cover engineering; deeper sieve theory is needed to understand failed regions.
- **Visible competition:** 21 comments; duckmerc and Aurelien Col are marked working, and Col marks it tractable/formalisable/formalising. The thread contains multiple AI/Lean proof attempts that were found to have serious gaps.

### 5. Problem #488 — density of a union of multiples

- **Exact current statement:** for finite \(A\), set \(B=\{n\ge1:a\mid n\text{ for some }a\in A\}\). Is it true that for every \(m>n\ge\max(A)\),
  \[
  \frac{|B\cap[1,m]|}{m}<2\frac{|B\cap[1,n]|}{n}\,?
  \]
- **Current site label:** **FALSIFIABLE**, open; zero claimed proofs. [Problem](https://www.erdosproblems.com/488) · [discussion](https://www.erdosproblems.com/forum/discuss/488?order=newest)
- **Remarks/status that matter:** the constant \(2\) is sharp in the limit via a singleton \(A\). The current “multiples” definition corrects an apparent typo in one original source; counterexamples to the alternate “nonmultiples” version do not count. Page last edited 2026-04-08.
- **Finite attack:** reduce to primitive \(A\), begin with \(|A|=3\), exploit exact inclusion-exclusion and periodicity modulo \(\operatorname{lcm}(A)\), and use branch-and-bound over ordered triples. A candidate \((A,n,m)\) is checked by integer counts alone.
- **Prerequisite load:** low-medium—elementary sieve/counting plus careful exact computation.
- **Visible competition:** 30 comments; will0708 and wesleyaweaverjr are marked working; two users mark it tractable. The thread reports many AI-assisted special cases and searches. A 2026-06-06 forum post claims a short proof for all two-element \(A\); this is not yet incorporated into the vetted remarks.

### 6. Problem #64 — Erdős–Gyárfás power-of-two cycle conjecture

- **Exact current statement:** “Does every finite graph with minimum degree at least \(3\) contain a cycle of length \(2^k\) for some \(k\ge2\)?”
- **Current site label:** **FALSIFIABLE**, open; zero claimed proofs; \$1000. [Problem](https://www.erdosproblems.com/64) · [discussion](https://www.erdosproblems.com/forum/discuss/64?order=newest)
- **Remarks/status that matter:** the conjecture is known for sufficiently large minimum degree and many graph families. The thread reports that a cubic counterexample must have at least 30 vertices and a bipartite counterexample at least 32. Page last edited 2026-04-10.
- **Finite attack:** generate cubic or predominantly cubic candidates with forbidden-cycle constraints built into SAT, rather than enumerate all cubic graphs. For order \(N\), forbid cycles of every power-of-two length at most \(N\) and produce a DRAT/LRAT-style unsatisfiability certificate or a witness graph.
- **Prerequisite load:** medium—structural graph theory, canonical generation, proof-producing SAT.
- **Visible competition:** only 1 bibliographic comment, but Chillguy, Sam Petkov, and mattryanwatts are marked working; Chillguy marks it tractable/formalisable/formalising. A May 2026 preprint adds strong structure for minimal counterexamples.

### 7. Problem #307 — product of two prime reciprocal sums

- **Exact current statement:** “Are there two finite sets of primes \(P,Q\) such that
  \[
  1=\left(\sum_{p\in P}\frac1p\right)\left(\sum_{q\in Q}\frac1q\right)?
  \]”
- **Current site label:** **VERIFIABLE**, open; zero claimed proofs. [Problem](https://www.erdosproblems.com/307) · [discussion](https://www.erdosproblems.com/forum/discuss/307?order=newest)
- **Remarks/status that matter:** \(P,Q\) must be disjoint and \(\sum_{p\in P\cup Q}1/p\ge2\), hence \(|P\cup Q|\ge60\). Weakened relatively-coprime versions have examples, but none of those solve the prime problem.
- **Finite attack:** search one side \(P\), write its exact reciprocal sum as \(a/b\), and force the other side to sum to \(b/a\), using denominator valuations and factoring to prune. Meet-in-the-middle, modular signatures, and distributed factorization are more plausible than raw subset enumeration.
- **Prerequisite load:** medium—unit fractions, \(p\)-adic constraints, high-performance exact arithmetic.
- **Visible competition:** 6 comments; aditya, will0708, and Ary300 are marked working; two users mark it difficult and none marks it tractable. A May 2026 comment points to a MathOverflow discussion.

### 8. Problem #835 — coloring a Johnson graph

- **Exact current statement:** “Does there exist a \(k>2\) such that the \(k\)-sized subsets of \(\{1,\ldots,2k\}\) can be coloured with \(k+1\) colours such that for every \(A\subset\{1,\ldots,2k\}\) with \(|A|=k+1\) all \(k+1\) colours appear among the \(k\)-sized subsets of \(A\)?”
- **Current site label:** **VERIFIABLE**, open; zero claimed proofs. [Problem](https://www.erdosproblems.com/835) · [discussion](https://www.erdosproblems.com/forum/discuss/835?order=newest)
- **Remarks/status that matter:** equivalently, ask whether \(\chi(J(2k,k))=k+1\). The main remarks exclude \(3\le k\le8\) and all \(k>2\) for which \(k+1\) is composite. Recent forum posts give further exclusions through \(k=14\) and reduce a coloring to a large set of Steiner systems; these posts leave \(k=16\) as the first apparent case not excluded. Page last edited 2026-01-22.
- **Finite attack:** seek a highly symmetric large set at \(k=16\), working in orbit variables under a chosen subgroup; any resulting coloring is a finite certificate. Direct vertex-color SAT is not viable.
- **Prerequisite load:** high—Johnson schemes, constant-weight codes, Steiner designs, group actions.
- **Visible competition:** 7 substantive comments; nobody is marked currently working, but two users are interested and the thread had several nontrivial advances in May 2026.

### 9. Problem #114 — lemniscate length

- **Exact current statement:** “If \(p(z)\in\mathbb C[z]\) is a monic polynomial of degree \(n\), then is the length of the curve \(\{z\in\mathbb C:|p(z)|=1\}\) maximised when \(p(z)=z^n-1\)?”
- **Current site label:** **FALSIFIABLE**, open; zero claimed proofs; \$250. [Problem](https://www.erdosproblems.com/114) · [discussion](https://www.erdosproblems.com/forum/discuss/114?order=newest)
- **Remarks/status that matter:** the conjecture is proved for \(n=2\), asymptotically, locally at \(z^n-1\), and by Tao for all sufficiently large \(n\). Forum posts claim a cubic proof and interval certificates for every \(n\le14\). Page last edited 2026-01-23.
- **Finite attack:** either find one degree-\(n\) polynomial with a strict certified length improvement, or turn Tao's high-degree result into an effective threshold and interval-certify every remaining degree. The former is a clean disproof route; the latter is a large proof program.
- **Prerequisite load:** very high—complex analysis, lemniscate geometry, global optimization, certified quadrature/interval arithmetic.
- **Visible competition:** 7 comments; KMendoza, dahlkebj, and Sam Petkov are marked working. Mendoza's public implementation already reaches degree 14.

### 10. Problem #167 — Tuza's conjecture

- **Exact current statement:** “If \(G\) is a graph with at most \(k\) edge disjoint triangles then can \(G\) be made triangle-free after removing at most \(2k\) edges?”
- **Current site label:** **FALSIFIABLE**, open; zero claimed proofs. [Problem](https://www.erdosproblems.com/167) · [discussion](https://www.erdosproblems.com/forum/discuss/167?order=newest)
- **Remarks/status that matter:** \(K_4\) and \(K_5\) show the factor \(2\) would be sharp. The best general bound cited is \((3-3/23+o(1))k\); the conjecture is known for random graphs. Page last edited 2025-10-13.
- **Finite attack:** jointly optimize triangle packing and triangle edge-cover numbers for generated graphs; require \(\tau_\triangle(G)>2\nu_\triangle(G)\). Both sides can be certified by integer programs, but searching graph space remains unbounded.
- **Prerequisite load:** high—packing/covering duality, extremal graph theory, hypergraph methods.
- **Visible competition:** just 1 bibliographic comment and no user marked working. This understates the mature external research literature.

## Rejected or deprioritized problems

| Problem | Exact current statement (abridged only where the displayed formula is retained) | Current remarks and finite-search reality | Activity / verdict |
|---|---|---|---|
| [#97](https://www.erdosproblems.com/97) | Does every convex polygon have a vertex with no other four vertices equidistant from it? | **FALSIFIABLE**, open. Danzer has a 9-point example with three equidistant neighbors at every vertex, and Fishburn–Reeds a 20-point uniform-distance example for three. A finite geometric counterexample would be checkable. | 7 comments; 2 users marked working. More importantly, a 2026-07-14 [forum post](https://www.erdosproblems.com/forum/discuss/97?order=newest) says the author has all but one residual case closed and expects to announce a solution soon. **Reject on first-mover risk**, regardless of intrinsic tractability. |
| [#107](https://www.erdosproblems.com/107) | For the Erdős–Szekeres number \(f(n)\), prove \(f(n)=2^{n-2}+1\). | **FALSIFIABLE**, open; \$500. This is the classic Happy Ending problem. Current upper bound is \(2^{n+O(\sqrt{n\log n})}\), far from exact. A counterexample at one \(n\) is finite only formally; exact order-type enumeration scales catastrophically. | 2 comments, no worker marked, but the mathematical prerequisite and historical depth are extreme. **Reject.** |
| [#364](https://www.erdosproblems.com/364) | Are there three consecutive positive integers all of which are powerful? | **VERIFIABLE**, open. No example for the middle integer below \(7.38\times10^{28}\); abc implies only finitely many. Special structural cases were ruled out in 2025. | 5 comments, no worker marked. The existing computational floor makes a laptop search noncompetitive. **Reject.** |
| [#366](https://www.erdosproblems.com/366) | Is there a 2-full \(n\) such that \(n+1\) is 3-full? | **VERIFIABLE**, open. Known consecutive powerful pairs below \(10^{22}\) have the opposite orientation. abc gives conditional finiteness. The page was edited 2026-07-16 and displays **1 claimed proof**, though the visible thread contribution is conditional rather than a site-accepted solution. | 3 comments, no worker marked, one “difficult” reaction. **Reject:** deep Diophantine search plus a current claim flag. |
| [#647](https://www.erdosproblems.com/647) | Is there \(n>24\) with \(\max_{m<n}(m+\tau(m))\le n+2\)? | **VERIFIABLE**, open; \$44. The [thread](https://www.erdosproblems.com/forum/discuss/647?order=newest) reports an exact finite certificate of no solution through \(6.157\times10^{17}\), a separate sieve through \(10^{12}\), forced congruence classes, and prime 7-tuple barriers. These are forum claims, but they decisively show that naive search is exhausted. | 13 comments; 4 users marked working; intense recent AI-assisted activity. **Reject.** |
| [#672](https://www.erdosproblems.com/672) | Can the product of a coprime positive arithmetic progression \(n,n+d,\ldots,n+(k-1)d\), \(k\ge4\), be a perfect power? | **VERIFIABLE**, open. Nonexistence is proved for \(4\le k\le34\), for sufficiently large \(k\) under other restrictions, and for very large prime exponents relative to \(k\). A positive search therefore begins only at \(k\ge35\) inside generalized-Fermat territory. | 4 comments, no worker marked. Low visible competition does not offset the Diophantine depth. **Reject.** |
| [#242](https://www.erdosproblems.com/242) | For every \(n>2\), do distinct \(x<y<z\) satisfy \(4/n=1/x+1/y+1/z\)? | **FALSIFIABLE**, open: the Erdős–Straus conjecture. Verified for all \(n\le10^{18}\), with extensive congruence and density results. | 18 comments; 4 workers; multiple difficult/tractable/formalisation reactions. Famous and computationally exhausted. **Reject.** |
| [#287](https://www.erdosproblems.com/287) | In every distinct-denominator representation \(1=\sum_{i=1}^k1/n_i\), must some adjacent denominator gap be at least \(3\)? | **FALSIFIABLE**, open. The main remark ties eventual finiteness to a strong prime condition. The 2026 [thread](https://www.erdosproblems.com/forum/discuss/287?order=newest) reports exact searches, a Lean check through \(k=18\), and a claimed certificate forcing any counterexample's first denominator above \(4.099\times10^{17}\). | 18 comments and substantial recent AI competition; 1 user marked working. **Reject.** |
| [#375](https://www.erdosproblems.com/375) | In every run \(n+1,\ldots,n+k\) of composite integers, can distinct primes \(p_i\mid n+i\) be chosen? | **FALSIFIABLE**, open: Grimm's conjecture. It implies a major prime-gap improvement and Legendre's conjecture. Verified for all \(n\le1.9\times10^{10}\). | 4 comments, no worker marked, one difficult reaction. The site itself calls it very difficult. **Reject.** |
| [#398](https://www.erdosproblems.com/398) | Are the only solutions of \(n!=x^2-1\) given by \(n=4,5,7\)? | **FALSIFIABLE**, open. No further solution below \(10^9\); abc gives conditional finiteness, and recent work handles restricted factor shapes. | 10 comments, no worker marked. A new solution would be easy to check but the search floor and Brocard–Ramanujan depth are prohibitive. **Reject.** |
| [#458](https://www.erdosproblems.com/458) | Is \([1,\ldots,p_{k+1}-1]<p_k[1,\ldots,p_k]\) for every \(k\ge1\)? | **FALSIFIABLE**, open. The remarks explain that controlling primes \(q\) with \(p_k<q^2<p_{k+1}\) would essentially require the notorious Legendre prime-gap conjecture, with additional trouble from small primes. | 3 comments, no worker marked, one difficult reaction. Fast evaluation at finite \(k\) does not create a plausible counterexample scale. **Reject.** |

## Recommended handoff order

If these are sent to separate agents, the most productive briefs would be:

1. **#106:** “Search only for an exact \(k=3\) counterexample; numerical discovery must end in an exact coordinate certificate.”
2. **#23:** “Run proof-producing SAT/MaxSAT at successive small \(n\); either return one graph and a max-cut certificate or certified exhaustions.”
3. **#128:** “Use a cutting-plane graph search at successive \(n\); return one graph and an exhaustive sparse-half certificate.”
4. **#7:** “Enumerate odd abundant l.c.m.s from \(945\) upward with exact-cover certificates; do not attempt an informal global nonexistence proof.”
5. **#488:** “Search primitive triples and small primitive sets with exact periodic counts; first independently verify the posted \(|A|=2\) reduction.”

The remaining ranked items should be backups, not part of a first ten if other screens produce genuinely bounded or lower-competition candidates.

# Addendum: ordinary-open / fresh-candidate screen

**Screened as of:** 2026-07-24
**Additional scope:** #389, #624, #839, #849, #864, #885, #912, #943, #1016, #1106, #1160, #1199, #1210, #1212.

All fourteen pages are currently labelled **OPEN** (“cannot be resolved with a finite computation”), with zero claimed proofs. This makes them intrinsically worse fire-and-forget targets than a comparably difficult verifiable/falsifiable problem: computation can discover structure or test lemmas, but the final deliverable must be a uniform construction or asymptotic theorem.

## Addendum verdict

Only **#864** deserves provisional top-10 consideration. It would enter near the bottom of a final top ten, behind the strongest finite-status candidates. **#1016** is the first alternate, and **#624** is a more speculative second alternate. None of these displaces #106, #23, or #128 from the earlier screen.

#1212 would otherwise rank highly on tractability, but it is not first-mover-clean: a substantial Lean/AI partial was posted on 2026-07-21, explicitly citing further unpublished June work. #885, #943, #389, and #1210 also have recent AI or manuscript activity. The remaining problems are either famous hard conjectures or require prime-distribution/group-enumeration advances far beyond what a separate AI is likely to close.

## Ranked ordinary-open list

| Rank | Problem | Statement crispness | First-mover situation | Relative tractability and verdict |
|---:|---|---|---|---|
| 1 | [#864](https://www.erdosproblems.com/864) | **High.** A precise asymptotic upper bound for a Sidon set with one exceptional repeated sum. | Quiet: 2 comments, no marked worker. An October 2025 post gives a \((\sqrt2+o(1))\sqrt N\) upper bound; Tao links extremizers through \(N=69\). | **Top-10 borderline—yes.** The target \(2/\sqrt3\) is sharp by construction, and the unique exceptional sum gives exploitable structure. Still a real additive-combinatorics proof, not a computation. |
| 2 | [#1016](https://www.erdosproblems.com/1016) | **High.** Prove \(h(n)\ge\log_2n+\log_*n-O(1)\) for minimum-edge pancyclic graphs. | Very quiet: 1 comment, no worker; the comment is only an AI-assisted bibliography repair from October 2025. | **First alternate.** The current \(\log_2(n-1)-1\) counting bound and matching-order construction make the missing \(\log_*n\) a focused structural gap. It is delicate but more self-contained than the number-theory candidates. |
| 3 | [#624](https://www.erdosproblems.com/624) | **Medium.** The intended extremal meaning of “\(H(n)\) be such that” should be checked against the source before work, although the page has a formalised statement. | Essentially untouched: 1 deleted/correction comment, no reactions or worker. | **Second alternate.** Alon's strong result at the exact \(k=\log_2n\) scale suggests an entropy/set-system route, but the requested divergence above \(\log_2n\) is an unbounded-family theorem. |
| 4 | [#839](https://www.erdosproblems.com/839) | **Medium-high.** Two clearly nested targets for sequences avoiding sums of consecutive earlier terms. | One AI-assisted partial posted May 2026; no marked worker. | **Watchlist, not top ten.** Multiscale forbidden-sum counting is plausible, but the posted \(2/3\) density bound is far from forcing density dips to zero, and Freud's \(19/36\) construction shows high upper density is possible. |
| 5 | [#885](https://www.erdosproblems.com/885) | **High.** Construct \(k\) integers whose factor-difference sets have at least \(k\) common values. | A new AI/Lean partial was posted April 2026; no marked worker. The post and Bloom's reply even disagree on one reported value (\(1028\) versus \(1029\)), so the finite claim needs independent checking. | **Watchlist.** It is constructive and experimentally friendly, but only \(k\le4\) is proved in the literature; the general problem becomes a simultaneous-square/Diophantine construction rather than a scalable finite search. |
| 6 | [#1212](https://www.erdosproblems.com/1212) | **High mathematically**, despite typos in the displayed prose and uncertainty in the historical remarks. | **Hot:** on 2026-07-21 a user posted a Lean-checked drift obstruction, finite-path constructions, computations suggesting percolation, and a link to a June formal-conjectures PR with further unpublished partial work. | **Do not select for a first-to-solve campaign.** An explicit infinite path might be elementary enough for AI discovery, but another AI/formal effort is visibly working the same route right now. |
| 7 | [#389](https://www.erdosproblems.com/389) | **High.** For every \(n\), find \(k\) making one block product divide the next. | Active: 8 comments, 1 marked worker, 3 interested, and a user formalising. March 2026 brought a reformulation and new large computations. | **Do not select.** The minimal \(k\) for \(n=25\) is reported as \(1{,}070{,}858{,}041{,}561\); computation supplies data but not the required uniform existence proof. The closely related #396 has 35 comments and active workers. |
| 8 | [#1160](https://www.erdosproblems.com/1160) | **High**, though the page states the conjecture declaratively and its attribution is uncertain. | Quiet: 3 January 2026 background/numerology comments, no worker. | **Not top ten.** Comparing numbers of isomorphism classes of groups requires deep finite-group enumeration. The odd-order case is only known asymptotically from \(m\ge3619\); larger hardware does not solve the general structural problem. |
| 9 | [#1106](https://www.erdosproblems.com/1106) | **Medium.** The first displayed question \(F(n)\to\infty\) is already solved; only eventual \(F(n)>n\) remains open. | Completely quiet: 0 comments, no reactions or worker. | **Not top ten.** Existing results give only \(F(n)\gg\log n\), so the remaining linear lower bound is a major leap involving prime divisors of partition values. |
| 10 | [#1210](https://www.erdosproblems.com/1210) | **Medium.** The \(O(1)\) target is clear, but Erdős said an earlier version was misstated, so source normalization matters. | Recent: a May 2026 manuscript claims partial results; an April GPT-suggested proof was publicly retracted, and two users mark it tractable. | **Not first-mover-clean and likely prime-gap-hard.** The failed reduction would imply a strong form of the second Hardy–Littlewood prime-counting conjecture. |
| 11 | [#1199](https://www.erdosproblems.com/1199) | **Very high.** Every 2-colouring of \(\mathbb N\) should admit infinite \(A\) with monochromatic \(A+A\). | Only 3 comments; an April 2026 attempted counterexample was immediately corrected. No worker. | **Reject.** This is a classical Owings/Hindman infinite Ramsey problem; the absence of forum activity is not evidence of tractability. |
| 12 | [#943](https://www.erdosproblems.com/943) | **Medium-high** once \(\ast\) is clarified as additive convolution and \(n^{o(1)}\) as a uniform \(n^\epsilon\) bound. | Active: 5 comments; a March 2026 GPT-5.4 project posted an \(n^{2/5+\epsilon}\) partial and explicitly described ongoing work. | **Reject.** The exponent gap to \(n^\epsilon\) is enormous and the posted analysis identifies a missing square-sieve/uniform-fibre theorem. Poor first-mover odds. |
| 13 | [#912](https://www.erdosproblems.com/912) | **High.** Obtain an exact asymptotic for the number of distinct exponents in \(n!\). | Two heuristic comments, including a June 2026 refinement; no worker. | **Reject.** Tao's reduction predicts \(c=\sqrt{2\pi}\) but says an unconditional proof, even on average, likely needs prime-gap information available only under strong conjectures. |
| 14 | [#849](https://www.erdosproblems.com/849) | **High.** Does every multiplicity \(t\) occur among equal binomial coefficients? | Zero comments or reactions. | **Reject decisively.** This is Singmaster's conjecture in an equivalent hostile direction: no example is known for \(t\ge5\), and Erdős/Singmaster believed a universal upper bound exists. Quietness reflects difficulty, not freshness. |

## Best three proof-side candidates

### A. Problem #864 — one exceptional Sidon sum

- **Exact current statement:** Let \(A\subseteq\{1,\ldots,N\}\) have at most one integer \(n\) with more than one representation \(n=a+b\), \(a\le b\in A\). Is
  \[
  |A|\le(1+o(1))\frac{2}{\sqrt3}N^{1/2}\,?
  \]
- **Status and remarks:** open, zero claimed proofs, 2 comments. Erdős–Freud supplied the matching lower construction by reflecting a Sidon set in \([1,N/3]\). The problem is a restricted/weaker form of [#840](https://www.erdosproblems.com/840). [Problem](https://www.erdosproblems.com/864) · [discussion](https://www.erdosproblems.com/forum/discuss/864?order=newest)
- **Existing frontier:** the public thread observes that splitting at half the exceptional sum gives two genuine Sidon pieces and hence
  \[
  |A|\le(\sqrt2+o(1))N^{1/2}.
  \]
  The sharp constant is \(2/\sqrt3\approx1.1547\), versus \(\sqrt2\approx1.4142\).
- **Realistic AI role:** enumerate extremizers to infer stability, then seek a structural theorem coupling the two Sidon pieces rather than bounding them independently. A conclusive answer requires a uniform asymptotic proof. Computation through finite \(N\) cannot certify it.
- **Why it may make the final ten:** sharp construction, elementary statement, a visible but nontrivial gap, no declared worker, and no recent AI proof campaign.

### B. Problem #1016 — sparse pancyclic graphs

- **Exact current statement:** If \(h(n)\) is minimal such that an \(n\)-vertex graph with \(n+h(n)\) edges has cycles of every length \(3,\ldots,n\), prove
  \[
  h(n)\ge\log_2n+\log_*n-O(1).
  \]
- **Status and remarks:** open, zero claimed proofs, 1 bibliographic comment, no worker. The known bounds on the page are
  \[
  \log_2(n-1)-1\le h(n)\le\log_2n+\log_*n+O(1).
  \]
  [Problem](https://www.erdosproblems.com/1016) · [discussion](https://www.erdosproblems.com/forum/discuss/1016?order=newest)
- **Existing frontier:** the elementary lower bound is essentially a count of possible cycles versus cycle-space dimension; the problem asks for the extra iterated-log loss that matches the construction.
- **Realistic AI role:** classify near-minimal pancyclic graph cores, combine cycle-space counting with collision restrictions on cycle lengths, and use small-\(n\) enumeration only to formulate structural lemmas.
- **Why it is only an alternate:** the \(\log_*n\) term signals a multiscale structural argument; a local sharpening of the counting proof will probably not suffice.

### C. Problem #624 — universal images of subset restrictions

- **Exact current display:** for an \(n\)-element set \(X\), consider a map \(f:\mathcal P(X)\to X\) such that every \(Y\subseteq X\) with \(|Y|\ge H(n)\) satisfies
  \[
  \{f(A):A\subseteq Y\}=X.
  \]
  Prove \(H(n)-\log_2n\to\infty\).
- **Status and remarks:** open, zero claimed proofs, 1 non-substantive comment, no worker. Erdős–Hajnal proved
  \[
  \log_2n\le H(n)<\log_2n+(3+o(1))\log_2\log_2n.
  \]
  Alon proved strong image-deficiency results at the exact \(|Y|=\log_2n\) scale. [Problem](https://www.erdosproblems.com/624) · [discussion](https://www.erdosproblems.com/forum/discuss/624?order=newest)
- **Realistic AI role:** first reconcile the extremal quantifiers with the original sources/formalisation, then try to extend Alon's exact-scale deficiency through several added elements using entropy, covering, or dependent-random-choice arguments.
- **Why it is speculative:** the target requires an unbounded additive gap, so proving every fixed constant gap separately is not enough unless the estimates are uniform.

## Recent-activity warnings

- **#1212:** the 2026-07-21 thread post is only three days old and explicitly says computations suggest “yes”; it links a June formal-conjectures PR and further unpublished results. This is the clearest live race in the addendum.
- **#943:** the March 2026 post says research is ongoing and supplies both a checked \(n^{2/5+\epsilon}\) partial and a map of the missing theorem.
- **#389:** one user is marked working, another formalising, and March computations/reformulations are active; related #396 is even busier.
- **#1210:** a partial-results manuscript appeared 2026-05-31, while an April AI proof route was shown to imply a major prime-counting conjecture.
- **#885:** an April AI/Lean note gives useful finite configurations, but the numerical discrepancy in the thread should be resolved before building on it.
- **#839:** the May AI partial is elementary and not close to the full limit, but it means the obvious two-term sliding-window argument is already public.

## Combined recommendation from this agent's two screens

If selecting only from the problems examined in this file, the order is:

1. #106
2. #23
3. #128
4. #7
5. #488
6. #64
7. **#864**
8. #307
9. **#1016**
10. **#624**

This combined list is deliberately first-mover-sensitive. #1212 would be mathematically competitive with the bottom half, but its July 2026 activity removes it. In a project-wide merge, retain #864 for serious consideration; treat #1016 and #624 as reserves and replace them if another screen offers crisp finite witnesses with quiet public activity.

# Addendum II: skeptical screen of zero-comment ordinary-open problems

Checked on 2026-07-24: all eight pages remain **open**, with zero comments and zero claimed proofs. Here that silence is only a weak ownership signal; most of the problems are quiet because their known barriers are deep.

| Problem | Current frontier and recent-literature signal | What a conclusive solution would look like | Tractability verdict |
|---|---|---|---|
| [#100](https://www.erdosproblems.com/100) | For \(n\) planar points whose pairwise distances and distinct distance values are each separated by at least \(1\), prove diameter \(\gg n\). The known lower bound is \(n^{3/4}\), while distinct-distance machinery gives roughly \(n/\log n\); a 9-point example even has diameter \(<5\). A 2026 high-dimensional counterexample concerns related [#670](https://arxiv.org/abs/2604.15305), not this planar problem, but shows that the family is active. | A uniform planar incidence/geometric argument removing the remaining logarithm. Finite coordinate search cannot certify it. | **No displacement.** This is a log-removal problem in incidence geometry, not a likely isolated trick. |
| [#108](https://www.erdosproblems.com/108) | For every \(r\ge4,k\ge2\), must sufficiently high chromatic number force a subgraph of girth at least \(r\) and chromatic number at least \(k\)? Rödl settled only \(r=4\); the infinite analogue and a growth-ratio question are also open. | A general structural/probabilistic graph theorem valid for every \(r,k\). | **Reject.** Major Erdős–Hajnal/Rödl territory; no short certificate route. |
| [#126](https://www.erdosproblems.com/126) | If \(f(n)\) is the guaranteed number of distinct prime factors of \(\prod_{a\ne b\in A}(a+b)\), Erdős–Turán proved \(\log n\ll f(n)\ll n/\log n\). The problem asks \(f(n)/\log n\to\infty\); even the matching-side improvement \(f=o(n/\log n)\) is not known. It carries a \$250 prize. | A uniform superlogarithmic prime-divisor lower bound for every \(n\)-set of integers. | **Reserve only.** Crisp and quiet, but the 90-year multiplicative-number-theory gap is much larger than the statement suggests. |
| [#156](https://www.erdosproblems.com/156) | Does \([N]\) contain a maximal Sidon set of size \(O(N^{1/3})\)? The easy lower bound has this exponent; Ruzsa's 1998 construction gives \(O((N\log N)^{1/3})\). A 2021 analogue in \(\mathbb F_2^n\) still retains the same logarithmic-type loss ([paper](https://arxiv.org/abs/2109.00292)), so no newer direct resolution was found. | An explicit or probabilistic construction for every large \(N\), together with a fully checkable Sidon and maximality proof. Computation can discover the construction but cannot replace the asymptotic argument. | **Promote.** Best problem in this batch: sharp exponent, one visible logarithmic gap, concrete construction certificate, and no apparent claimant. It should replace #624 and probably outrank #307. |
| [#159](https://www.erdosproblems.com/159) | Prove \(R(C_4,K_n)\ll n^{2-c}\) for some \(c>0\). The page gives a lower bound of order \(n^{3/2}/(\log n)^{3/2}\) and an upper bound of order \(n^2/(\log n)^2\), labels the problem difficult, and was edited in March 2026. | Any fixed polynomial saving over the quadratic Ramsey upper bound. | **Reject decisively.** This is a major off-diagonal Ramsey breakthrough, despite the empty discussion. |
| [#197](https://www.erdosproblems.com/197) | Can \(\mathbb N\) be partitioned into two sets, each admitting a permutation with no monotone 3-term arithmetic progression? Three sets are known to suffice. The exact problem is still listed as open in recent literature, but permutation-avoidance work appeared in 2024 ([Adenwalla](https://arxiv.org/abs/2211.04451)) and a May 2026 preprint studies adjacent subsequence-sum questions ([preprint](https://arxiv.org/abs/2605.29011)). | A recursive/automatic 2-colouring and two explicit compatible permutations, with a finite-state or inductive proof excluding every forbidden triple. | **Borderline promote.** The constructive certificate is unusually crisp and AI-searchable. It can displace #624 and competes for ranks 9–10, but the adjacent literature makes it less first-mover-clean than its empty page suggests. |
| [#213](https://www.erdosproblems.com/213) | Does every \(n\ge4\) admit \(n\) planar points with all distances integral, no three collinear, and no four concyclic? Constructions reach only \(n=7\); a uniform upper bound follows conditionally from Bombieri–Lang. A June 2026 paper is directly active in planar integral point sets ([paper](https://arxiv.org/abs/2606.26311)). | Either arbitrary-size explicit configurations with proofs of all nondegeneracy conditions, or a deep unconditional impossibility theorem. | **Reject.** The tiny construction frontier, conditional Diophantine obstruction, and current specialist activity all argue against a fast first solution. |
| [#295](https://www.erdosproblems.com/295) | For the least \(k(N)\) such that \(1=\sum_{i=1}^k1/n_i\) with distinct \(n_i\ge N\), prove \(k(N)-(e-1)N\to\infty\). Known bounds leave this additive divergence unresolved. | A uniform second-order lower bound for constrained Egyptian-fraction representations. | **No displacement.** The target is deceptively small and appears to require delicate global optimization, with no finite certificate. |

## Promotion decision

- **#156 enters around ranks 7–8.** It clearly removes #624 from this agent's previous ten and is more promising than #307.
- **#197 enters around ranks 9–10 if the project accepts modest external-race risk.** Its proof object is much more concrete than #1016's iterated-log lower bound, but the 2024–2026 adjacent activity must be disclosed.
- **#126 is the only reserve worth retaining.** The other five are structurally too deep for the intended “fire off an AI” workflow.

With this batch included, this agent's tractability-first order becomes:

1. #106
2. #23
3. #128
4. #7
5. #488
6. #64
7. #864
8. **#156**
9. **#197**
10. #1016

#307 and #624 move below the line. This is a screening recommendation, not an assertion that #156 or #197 is easy: #156 has resisted a logarithmic improvement since 1998, and #197 now has a nontrivial external-race penalty.
