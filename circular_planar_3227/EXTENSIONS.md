# Exact extension reductions for the 20/7 target

Prepared 2026-10-20. Authored partial research, not a proof of OPG-401 and not a claim of a new literature result. The statement is fixed by `SOURCE_GATE.md`: finite simple triangle-free planar graphs of maximum degree at most three should map to K_(20/7). No smaller or different target is substituted.

## 1. Exact path algebra

Use residues modulo 20 and D={7,8,9,10,11,12,13}. A prescribed pair of endpoint colors on an m-edge path extends if and only if their difference belongs to S_m=D+...+D. Since sums of ordinary integer intervals have no gaps,

- S_1={7,...,13} (size 7);
- S_2={14,...,19,0,...,6} (size 13);
- S_3={1,...,19} (size 19);
- S_m=Z_20 for every m>=4.

For the last assertion the interval [28,52] already meets every residue; adding a nonempty set to the whole group preserves it. Thus a three-edge thread fails only for equal endpoint colors, whereas a four-edge or longer thread always extends. Confusing these two statements would invalidate a minimal-counterexample argument.

## 2. Universal tripod reductions

A tripod consists of a cubic center v and its three incident threads, with distinct internal degree-two vertices and terminal vertices outside the deleted configuration. Terminals are allowed to coincide with each other, but not with v. If thread i has length l_i and terminal color a_i, the center's permissible set is a_i+S_(l_i). After selecting a center color in their intersection, the three paths extend independently.

Consequently each of (1,3,3) and (2,2,3) is universally extendable:

- (1,3,3): the three forbidden sets have sizes 13,1,1, whose union has size at most 15<20;
- (2,2,3): their sizes are 7,7,1, again totaling 15<20.

The same argument gives (2,3,3) and (3,3,3). This proof does not use terminal distinctness, planarity, or restrictions on the boundary coloring.

These four triples are exactly the universally extendable sorted triples with each length in {1,2,3}. For every other triple, the following ordered terminal-color tuple gives empty center intersection:

| Lengths | Boundary colors |
|---|---|
| (1,1,1) | (0,0,7) |
| (1,1,2) | (0,0,0) |
| (1,1,3) | (0,6,13) |
| (1,2,2) | (0,0,0) |
| (1,2,3) | (0,0,0) |
| (2,2,2) | (0,6,13) |

These are counterexamples to *arbitrary boundary extension*, not counterexamples to the conjecture. An exterior graph may impose additional boundary restrictions or allow recoloring.

## 3. Minimal counterexample consequences

In either the target planar class or the triangle-free subcubic class with maximum average degree below a specified threshold, take a counterexample with the fewest vertices. These classes are hereditary under taking subgraphs.

It is connected, has minimum degree at least two, and has no cut vertex. Indeed, independently color smaller connected pieces, rotate all colors in each piece so they agree at the shared cut vertex, and combine. For a leaf, any of the seven colors adjacent to its neighbor extends the coloring.

It is not a cycle: even cycles alternate colors 0 and 10, and every odd cycle of length at least five closes because 0 belongs to S_m for m>=4. Triangle-freeness excludes the only relevant odd exception, length three.

Thus it has a cubic vertex. Every maximal degree-two thread has cubic endpoints, which are distinct: a returning thread would form a cycle attached to the remainder at its cubic endpoint, giving a cut vertex. Delete thread interiors and extend to conclude that all threads have length at most three.

At any cubic vertex its three incident thread lengths cannot contain (1,3,3) or (2,2,3), including the larger triples listed above. Delete the center and the interiors of the three incident threads, color the strictly smaller graph, and use the universal tripod extension. Coincident terminal vertices do not spoil this reduction.

## 4. A proved sparse special case

**Proposition.** Every finite simple triangle-free graph G of maximum degree at most three and maximum average degree strictly less than 12/5 admits a (20,7)-coloring.

**Proof.** Suppose a vertex-minimal counterexample H exists. Apply Section 3. Let n_2,n_3 be its counts of degree-two and degree-three vertices. Assign to each cubic vertex v the weight

w(v)=sum over incident threads of (thread length minus one).

Every thread has length at most three. If none of the three lengths equals three, w(v)<=3. If one length equals three, another length must be one, since (2,2,3) is forbidden. There cannot be two lengths three, since (1,3,3) is forbidden. Hence w(v)<=3 also in this case. Each degree-two vertex belongs to one thread and contributes to its two endpoints, so

2 n_2=sum_v w(v)<=3 n_3.

Because n_3>0,

average_degree(H)=(2n_2+3n_3)/(n_2+n_3)=2+n_3/(n_2+n_3)>=2+1/(5/2)=12/5.

This contradicts the maximum-average-degree hypothesis on G. QED.

**Corollary.** Every finite simple planar subcubic graph of girth at least 12 admits a (20,7)-coloring.

For completeness, a vertex-minimal counterexample is 2-connected, so every facial boundary has length at least 12. Euler's formula gives 2e>=12f and n-e+f=2, hence e<=6(n-2)/5 and average degree strictly below 12/5, contradicting the same counting argument. The corollary is a special case with a much stronger girth assumption than OPG-401; it must not be presented as solving that target. No novelty claim is made.

## 5. Attempts to pass the sparse barrier

The tripod argument controls subdivision density, not the cubic planar core. In particular it does not exclude any 3-regular graph: all its incident thread lengths are (1,1,1). A discharging proof based only on the reductions above therefore cannot prove the girth-four target. Planarity gives average degree below 4 for triangle-free graphs, which supplies no contradiction to the established lower bound 12/5 (nor to cubic average degree 3).

The most immediate larger tree candidate also fails. Take two adjacent cubic centers, each with two length-two arms to boundary vertices. Terminal colors (0,5) at one center and (6,19) at the other leave feasible center sets A=S_2 intersect (5+S_2) and B=(6+S_2) intersect (19+S_2), with no D-adjacent pair. Thus the (2,2;2,2) double star is not universally reducible. Several mixed-arm variants likewise fail; their explicit boundary witnesses appear in `extension_checks.json`.

A square deletion followed by adding two boundary edges is not justified by the naive extension lemma either. Label the four exterior colors cyclically a_0,...,a_3. Requiring a_0 adjacent to a_1 and a_2 adjacent to a_3 still does not ensure extension: (0,7,7,0) is a counterexample. Requiring the opposite pairs adjacent also fails, at (0,0,7,7). These statements concern the color constraint alone; even if the replacement graph remains triangle-free and planar, that constraint is insufficient. The deterministic small checks are in `check_square.py` and `square_checks.json`.

An unconditional five-face extension is also false: with every exterior neighbor colored 0, every face vertex is restricted to {7,...,13}. No two elements of this set are adjacent in K_(20/7), so even a single face edge cannot be colored. This illustrates why arbitrary-list extension cannot eliminate cubic faces by itself.

A viable full proof would need a stronger structural reduction with a verified boundary-color relation, a recoloring theorem for the exterior, or global information beyond the elementary degree-two-thread counts. None is established here.

## 6. Reproducible checks and limits

Run `python check_extensions.py` and `python check_square.py` from the package root. Both use only Python's standard library, exact finite sets, and exhaustive searches modulo color translation. They inspect all 400 normalized boundary assignments for each universally extendable tripod; failing cases stop at their first explicit witness. The double-star and square checks likewise stop at the first obstruction. No floating-point solver or probabilistic test is used.

The scripts confirm local lemmas only. They do not enumerate planar graphs, prove completeness of a discharging configuration list, establish the conjecture, or certify current literature status. The sparse proposition above has a standalone proof independent of trusting the scripts.

## 7. A global positive class beyond the density criterion

**Proposition (fully subdivided cores).** Let G be a finite simple triangle-free subcubic graph. Suppose every maximal thread between vertices whose degrees are not two has at least two edges. Then G admits a (20,7)-coloring, regardless of planarity or maximum average degree. In particular, the conclusion holds for every graph obtained by subdividing every edge of a loopless subcubic multigraph at least once.

**Proof.** Work one connected component at a time. An isolated vertex is immediate. If every vertex has degree two, the component is a cycle and Section 3 applies. Otherwise suppress all degree-two vertices to produce a core multigraph H on the vertices of degree one or three. (A two-vertex component joined by a thread is included.) Distinct threads have disjoint interiors; parallel edges and loops in H are allowed. Count a loop twice toward degree, so the maximum degree of H is at most three.

Delete loops and merge parallel edges solely for choosing vertex colors. The resulting simple graph has maximum degree at most three. A greedy proper coloring uses at most four labels, chosen as 0,1,2,3 in Z_20. Use these as colors of the corresponding vertices of G.

For a nonloop thread, its endpoints receive distinct labels, so their residue difference is one of ±1,±2,±3. Every such difference belongs both to S_2 and S_3, and S_m is the whole group for m>=4. By hypothesis the thread has length at least two, so its interior extends. Parallel threads cause no conflict because they have disjoint interiors and each independently accepts the endpoint pair.

A loop of H corresponds to a thread returning to its own endpoint. In the simple triangle-free graph G this forms a cycle of length at least four: lengths one and two would violate simplicity, and length three would violate triangle-freeness. Equal endpoint colors therefore extend by 0 in S_m for m>=4. All thread extensions together give the coloring of G. QED.

This proof handles cut vertices and bridges directly and does not need a block decomposition. It also explains why the local (2,2,2) failure does not imply difficulty for the global class: one chooses a compatible core coloring, rather than accepting arbitrary preassigned terminal colors.

The class is not covered by the strict mad<12/5 proposition in general. For example, replacing every edge of a cubic graph by a two-edge path gives n_2=3n_3/2 and average degree exactly 12/5; its coloring is guaranteed here. Mixed threads of lengths at least two may make the graph still sparser, but no density computation is needed for the conclusion. This is another special case, not a solution of the original conjecture: the target permits length-one edges between cubic core vertices.
