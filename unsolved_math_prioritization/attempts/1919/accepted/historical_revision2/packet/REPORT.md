# Cycle-set counting: exact scope and five lower-bound approaches

Problem 1919 / EP-84, queue rank 1017. Checked 8 October 2026 (UTC).

## Disposition

The combined problem remains **unsolved here, five substantive approaches used**. Its first assertion is an already published theorem; its second assertion is not proved or refuted by this packet. No new-solution, novelty, formal-verification, or peer-review claim is made.

For a finite simple undirected graph G on exactly n vertices, let C(G) be the set of lengths of its simple cycles. Let f(n) be the number of distinct sets C(G) as G varies. Thus f counts sets, not graphs or isomorphism classes. The empty set counts; isolated vertices are allowed. Labels have no effect on f. Cycles need not be induced. They have at least three edges, and their edge and vertex counts coincide.

The two target assertions are:

1. f(n)/2^n tends to zero as integer n tends to infinity.
2. f(n)/2^(n/2) tends to infinity as integer n tends to infinity, through both parities.

The accompanying question about existence and value of lim f(n)^(1/n) is separate. We do not resolve it. Padding with isolated vertices proves f(n+1) >= f(n); this alone does not establish either requested limit. In particular a lower bound along a sparse subsequence is insufficient for assertion 2 without a quantitatively adequate interpolation argument.

## Sources, credit, and present-status limits

The official indexed history and LaTeX pages reproduce both assertions and distinguish the first solved assertion from the remaining one. Direct retrieval of the problem, history, and LaTeX pages returned HTTP 403 during this check; their indexed contents were available. Consequently this is not a claim of an unrestricted live-page/comment inspection.

- Jacques Verstraëte, *On the Number of Sets of Cycle Lengths*, Combinatorica 24 (2004), 719–730, DOI https://doi.org/10.1007/s00493-004-0043-6. Theorem 1.2 in the author's PDF proves a saving in the exponent, and settles assertion 1. The first three PDF pages were rendered; page 2 was visually inspected because the embedded text extraction is corrupt. Author PDF: https://mathweb.ucsd.edu/~jverstra/numcyc.pdf.
- Rajko Nenadov, *Improved bound on the number of cycle sets*, Combinatorial Theory 6(1) (2026), article 17, published 20 April 2026, https://doi.org/10.5070/C66165704. Theorem 1.1 gives f(n) <= 2^(n - Omega(sqrt(n)/(log n)^(3/2))). Its positive exponent saving tends to infinity, so division by 2^n proves assertion 1. This bound gives no diverging-factor lower bound. The published PDF and arXiv v2 were retrieved and their introductions inspected separately: https://escholarship.org/content/qt4k75b3z7/qt4k75b3z7.pdf and https://arxiv.org/abs/2501.09904v2.
- Alvin Dunås, *The number of sets of cycle lengths for graphs on n vertices*, Uppsala University, U.U.D.M. Project Report 2026:24, master's degree project, June 2026. Abstract and Section 2 expressly leave assertion 2 open. Proposition 2.2 gives f(n+1) >= d(n), counting distinct positive distance sets of subsets of an n-point interval. Corollary 2.5 proves f(n) >= (3/2)2^(n/2)-2 for even n, and f(n) >= sqrt(2)2^(n/2)-2 for odd n. These improve constants, not their divergence. This is a completed master's thesis, not described here as a peer-reviewed journal article. Record: https://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-591570; PDF: https://uu.diva-portal.org/smash/get/diva2%3A2077189/FULLTEXT01.pdf.
- Official scope: https://www.erdosproblems.com/84, https://www.erdosproblems.com/history/84, https://www.erdosproblems.com/latex/84. The indexed official record attributes the conjectures to Erdős and Faudree and cites Erdős sources from 1994, 1995, 1996, and 1997. We do not claim to have inspected all those historical originals. The 2026 primary paper explicitly identifies Erdős's 1997 Problem 5.

The source check found no primary resolution of assertion 2. That search result is not proof of universal current openness. The two preserved corpus inputs match ID 1919 / EP-84; the research-results corpus has no directly keyed record for that ID. Corpus bytes and records are not in this packet. Public hash metadata is in SOURCES.json. A bounded live PR/branch and retained-artifact duplicate gate found no previous substantive campaign attempt, rather than treating a stale queue status as authoritative.

## Approach 1: widen a decodable one-hub family

### Exact graph identity

Let P_N have vertices 0,...,N-1 and consecutive edges. Add an apex x adjacent precisely to A subset {0,...,N-1}. Let D(A)={|a-b|:a,b in A,a != b}. Then

C(P_N plus x) = {d+2:d in D(A)}.                                      (1)

Indeed every cycle uses x, since the remaining graph is a tree. Removing x from a simple cycle leaves the unique path between two distinct neighbors a,b, whose length is |a-b|. Conversely every such pair produces a simple cycle. This is the distance-set construction credited above, not a newly claimed reduction.

For a direct baseline on n=2m vertices with m>=2, take the path 1,...,2m and edges {1,a} for a in B subset {m+1,...,2m}. The apex formulation, with vertex 1 removed from the path, shows that cycles have lengths a or b-a+2 (a<b in B, allowing path-neighbor 2). Among the selected-selected differences, the only possible value exceeding m is m+1, and attaining it requires m+1 already to belong to B. Thus lengths exceeding m recover B exactly. Thus f(2m) >= 2^m, the Faudree family reviewed by Nenadov. The restriction m>=2 is essential: for m=1 the proposed edge {1,2} is already the path edge, no simple 2-cycle arises, and f(2)=1.

### Attempt to gain an unbounded factor

Allow more independently selected neighbors below the formerly safe halfway threshold. The desired extra bits cease to be decodable, because differences between selected neighbors enter the same band as anchor-to-neighbor distances. This is a real collision, not merely label symmetry: the sets

A={0,1,4,6}, B={0,1,2,3,6}

have the same positive distance set {1,2,3,4,5,6}. They are not reflections (they even have different cardinalities). Both belong to the widened interval family with m=3, endpoints 0 and 2m fixed, and all other points at least m-2. Their apex graphs have the same cycle set {3,4,5,6,7,8}.

More precisely, with free points from [m-s,2m] and the anchor 0, selected-selected differences may reach m+s. Only positions strictly above m+s can be read without further argument from the distance set; their number is m-s. Widening the interval therefore cannot justify counting all its subsets by the original high-band decoder. A clever global decoder or an image/fiber bound could still work; this observation does not disprove that possibility.

Remaining gap: for a growing width s, prove a lower bound on the number of distinct complete distance sets large enough to overcome the vertex cost. A count of neighbor subsets, or a bound that ignores their fibers, does not supply it. The harness recomputes distance-set counts through N=16 and the collision, but finite growth is not extrapolated to a limit.

## Approach 2: random subsets and image entropy

The next attempt was to show that most of the 2^N apex-neighbor choices give distinct enough distance sets. A uniform random choice actually concentrates on a very small collection of outputs.

Fix 1<=d<=N-1. The graph whose edges are {i,i+d}, 0<=i<N-d, is a disjoint union of paths. It has N-d edges and a matching of size at least (N-d)/2: each path with e edges has a matching of size ceil(e/2), and these matchings are disjoint. In a uniform random A, the events that each matching edge is not entirely selected are independent and have probability 3/4. Therefore

Pr(d not in D(A)) <= (3/4)^((N-d)/2).                                (2)

For an integer t with 1<=t<N, the union bound gives

Pr({1,...,N-t} not subset D(A)) <= N (3/4)^(t/2).                     (3)

Take t=ceil(6 log N / log(4/3)); for sufficiently large N this is below N, and the right side is at most N^-2. Thus at least (1-N^-2) of all inputs have every distance through N-t. Their outputs can differ only at t-1 distances, so they yield at most 2^(t-1), a polynomial in N, distinct distance sets.

This is an obstruction to a naive uniform-random typical-input injection, not an upper bound of polynomial size on all distance sets. The exceptional inputs may contain exponentially many distinct outputs. No control of those exceptional fibers sufficient for assertion 2 was obtained. Biased sampling or deliberately sparse/fringed families remain outside this obstruction.

As a separate finite check, missing-distance counts are computed by exhaustive subsets and by a path-independent-set recurrence: if N=qd+r, 0<=r<d, the count is F_(q+2)^(d-r) F_(q+3)^r. The two procedures agree in the checked range. This identity also appears as Dunås's Lemma 2.6; the matching argument above does not depend on his asymptotic upper bound for d(N).

## Approach 3: independent blocks and cactus multiplication

One might combine independently chosen cycle gadgets by disjoint union or identification at a cut vertex. All simple cycles remain in individual blocks, so the output is the union of their length sets. This has no automatic product count: adjoining a triangle makes the distinct old spectra empty and {3} identical, both now {3}.

For the natural class of cactus graphs this strategy has a sharp vertex-budget obstruction. A cactus is a graph each of whose nontrivial blocks is a single edge or a cycle; equivalently its distinct simple cycles meet in at most one vertex. A finite set S subset {3,4,...} is the cycle set of a cactus on at most n vertices if and only if

sum_(ell in S) (ell-1) <= n-1.                                     (4)

For necessity, in each connected component the block decomposition gives vertices minus one equal to the sum over blocks of vertices minus one. Select one cycle block for every distinct required length; the omitted blocks only increase this cost. Summing over components yields at least 1+sum(ell-1) vertices when S is nonempty. The empty S is realized by isolated vertices. For sufficiency, attach one ell-cycle for each ell in S at one common vertex, and pad with isolated vertices. This construction has exactly the claimed cost and no other cycles.

Let a(M) count sets of distinct positive integer weights summing to at most M. For every t>0,

a(M) <= exp(tM) product_(j>=1)(1+exp(-tj))
      <= exp(tM + sum_(j>=1) exp(-tj))
      <= exp(tM + 1/t).

The last inequality uses exp(t)-1>=t. Taking t=1/sqrt(M) gives a(M)<=exp(2 sqrt(M)) for M>0. Applying this with weights ell-1 (which actually start at 2) bounds the number of all cactus cycle sets on n vertices by exp(2 sqrt(n-1)). This is o(2^(n/2)). It rules out cactus-only product constructions outright. It does not rule out adding carefully chosen blocks to a dense non-cactus core, where spectral collisions and the growth of that core must be controlled separately.

## Approach 4: many parallel paths and additive coding

A different construction joins two terminals by k internally vertex-disjoint simple paths of lengths l_1,...,l_k. For a simple graph, lengths are positive integers, and at most one path has length 1. Padding with isolated vertices is permitted. The vertex count of the nontrivial component is

2 + sum_i(l_i-1).

Every simple cycle uses exactly two of these paths, and conversely any pair produces a cycle. Hence its spectrum is

{l_i+l_j: i<j}.                                                    (5)

This seems to offer quadratically many pairwise-sum markers using k choices. But the budget counts the total path lengths, while the cycle set forgets their ordering. For n vertices, the positive numbers l_i-1 form an integer partition of some s<=n-2; the optional direct edge contributes a single zero. Thus the number of possible spectra in this entire family is at most

2 sum_(s=0)^(n-2) p(s),                                            (6)

including harmless overcounting of degenerate choices.

For completeness, with M>=1 and t>0,

sum_(s=0)^M p(s) <= exp(tM) product_(j>=1)(1-exp(-tj))^-1.

The logarithm of the product equals sum_(r>=1) [r(exp(tr)-1)]^-1, at most (1/t) sum_(r>=1) r^-2 <= 2/t. Taking t=sqrt(2/M) yields an upper bound exp(2 sqrt(2M)). Therefore (6) is subexponential and again o(2^(n/2)). This is a rigorous failure of the single parallel-path family even when k is allowed to grow, stronger than a fixed-k polynomial bound. More complicated networks whose cycles can pass through several branching locations are not covered.

## Approach 5: two hubs and interference between cycle types

The final attempt allows cycles through either or both of two hubs, so it genuinely exits both the one-hub and parallel-path models. Add nonadjacent vertices x,y to P_N, with neighborhoods A,B subset {0,...,N-1} respectively.

The exact spectrum is the union of three parts:

- D(A)+2;
- D(B)+2;
- d+e+4, for two vertex-disjoint path intervals on P_N, each joining an A-neighbor to a B-neighbor, of lengths d and e.

Intervals of length zero are allowed in the third part, corresponding to a common neighbor of x and y. Two such intervals at distinct vertices produce a 4-cycle. The disjointness condition is on vertices, not just edges. To prove the formula, remove the hubs from a cycle. A cycle using one hub gives the first or second part. A cycle using both leaves two disjoint path intervals with the specified endpoints, possibly singletons. Conversely these pieces join to a simple cycle. These exhaust all possibilities.

### A tempting amplification, and the term that invalidates it

Take N=2m, let x have neighbors {0,t}, let y have neighbors {0} union B, where B subset {m,...,2m-1}, and 0<t<m. The exact specialization is

C = (B+2) union (D(B)+2) union {t+2} union (B-t+4).                  (7)

Indeed two nonzero cross intervals would overlap because the interval starting at 0 and ending in B already contains t. The only both-hub cycles use the common neighbor 0 as one singleton interval.

Ignoring D(B)+2 suggests encoding B by the union of B and its translate. When the shift t-2 is at least ceil(m/2), each residue-class chain of B has length at most two; the endpoints of the dilated chain recover both bits. Varying t appears to promise many distinguishable copies of the same exponential family. That argument is invalid for actual cycle sets: D(B)+2 hides the lower-copy endpoint bits, and can also destroy a claimed minimum-length marker.

A concrete counterexample is m=6, t=5, with endpoints 6 and 11 forced:

B_1={6,7,9,11}, B_2={6,7,8,9,11}.

Both fourteen-vertex graphs have precisely

{3,4,5,6,7,8,9,10,11,13}.

Thus even within the proposed separated-shift range, with fixed extremes, the two-hub decoder is not injective. The independent graph-cycle enumerator verifies this equality from edges, not merely by reusing formula (7).

For a broader symmetric family on 2m+2 vertices, give both hubs the neighbor 0 plus arbitrary subsets of {m,...,2m-1}. Direct image enumeration gives, for m=1,...,7, respectively

3, 6, 19, 46, 127, 310, 721

distinct spectra. The formula is cross-checked against an independent cycle enumerator exhaustively for path orders 1,...,5; larger displayed image counts use the proved formula. These counts are construction-specific lower bounds, not f(2m+2). They suggest testing structured two-hub subfamilies, but neither their ratios nor a guessed recurrence proves the target.

Remaining gap: obtain, for all sufficiently large n, an explicitly counted family of genuinely different complete spectra with cardinality g(n)2^(n/2), where g(n) tends to infinity. Any decoder must retain selected-selected and mixed-cycle contributions. No such decoder, lower image bound, or recurrence was established.

## Verification and limits

The executable checks are finite diagnostics and an integrity harness. They do not check the full analytical arguments in a proof assistant, establish an infinite limit, or certify the literature's theorems. The report's asymptotic deductions are ordinary mathematical proofs for their stated restricted scopes. All theorem credit above is prior work. The packet contains authored text/code and public verification metadata only; PDFs, extracts, rendered pages, corpus records, and private coordination are separate.

Five mathematical approaches, not five source searches or packaging actions, are recorded in LEDGER.json. No source lookup, gate, audit, test repair, freezing, or packaging step increases that count. No remote write was made in preparing this packet.
