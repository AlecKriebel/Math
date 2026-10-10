# An exact simplicial-core sampler for maximal parking functions

## Prose-edition and review scope

These AI-assisted authored documents are unrefereed. “Accepted” refers only to
the stated independent internal AI audit; no external human peer review,
journal acceptance, or formal proof-assistant certification is claimed.
The complete mathematical arguments are retained. This edition makes only
framing, attribution, and distribution-related editorial changes; no algorithm
or mathematical claim is changed.

Executable sampler and test programs, detailed test receipts, computational
certificates and raw datasets are omitted. Statements about implementation or
finite checks below record the review of the authenticated original artifacts;
they are not claims that this prose-only edition includes runnable code or
reproducible test receipts. Public verification metadata records the historical
checks and their limits. Hashes identify bytes and do not establish truth.

## Status and scope

**Partial result; the unrestricted AIM sampling problem is not solved.**

This note proves a constant-fiber elimination lemma and gives a fully
specified exact sampler for finite connected undirected **simple** graphs with a
specified root. It yields a polynomial-time exact sampler for every chordal
graph, and an exact fixed-parameter algorithm in the number of edges left after
root-preserving simplicial peeling. It also transfers approximate uniform core
samplers without increasing total-variation error.

The construction handles graphs beyond the bridge/cycle/clique-block family.
For example, a diamond (two triangles sharing an edge) has a single block that
is neither a clique nor a cycle, and is handled here. No novelty is claimed for
the elementary bridge, cycle, clique, or block-product special cases.

**Novelty is not established.** The elimination lemma is elementary and may be
folklore. In particular, the chordal case is already a consequence of the stated
bipolar-orientation sampling theorem of Bezáková–Sun (2022), through a universal
sink reduction explained below. Thus the contribution here is an independently
proved, implemented and exhaustively checked reduction, an explicit
parameterized/approximate transfer statement, and clarification of the scope of that literature. It is not a claimed new solution
of the general problem.

## 1. Definitions and an independent proof of the parking correspondence

Let G=(V,E) be finite, connected, undirected and simple; put n=|V|, m=|E|, and
fix q in V. A parking function has f(q)=-1, f(v)>=0 for v!=q, and for every
nonempty A subset V minus {q}, some v in A satisfies

    f(v) < |{vw in E : w not in A}|.

Maximal means maximal in coordinatewise order. Write A(G,q) for the acyclic
orientations of G having exactly one source, namely q. No restriction on sinks
is imposed. A one-vertex graph is allowed; its empty orientation and f(q)=-1
are the unique outputs.

For completeness, the familiar correspondence used below follows directly from
these definitions. Starting with q marked, repeatedly mark a vertex whose f
value is strictly smaller than its number of already marked neighbors. If the
process stopped early, the unmarked set would contradict the defining condition.
Thus every parking function admits a marking order. Orient every edge from
earlier to later in that order. Every nonroot vertex has a positive indegree,
and the resulting g(v)=indeg(v)-1 is at least f(v). Moreover,

    sum over v in V of g(v) = m-n.

Conversely, a topological ordering of any orientation in A(G,q), starting with
q, is a valid marking order for indegree minus one. To check the original subset
condition directly, the earliest vertex of a nonempty A in that ordering has
all its incoming neighbors outside A; it therefore has f(v)=indeg(v)-1 strictly
smaller than the exterior degree. This also shows nonnegativity away from q.
The marking-order argument bounds the sum of every parking function by m-n.
Thus every indegree-minus-one output is maximal, and every maximal parking
function must equal the g dominating it. In particular, maximal and
maximum-total-sum coincide here.

Finally, an acyclic orientation is determined by its indegree vector: vertices
of indegree zero have all incident edges pointing out; remove them, subtract
their contributions from remaining indegrees, and repeat. Every remaining
acyclic graph has a source, so this reconstruction is unique. We have proved the
bijection

    A(G,q) <--> maximal parking functions,  O |-> indeg_O - 1.       (1)

This is the correspondence as presented by Benson, Chakrabarty and Tetali,
proved here to make the sampling claims independent of unverified
implementation assumptions [2]. Their Remark 3.1 points to earlier antecedents;
no first-discovery attribution is made here.
The sum over nonroot coordinates is m-n+1, since f(q)=-1.

## 2. The constant-fiber simplicial deletion lemma

A vertex v is simplicial when its neighbor set is a clique.

**Lemma.** Suppose v!=q is simplicial, let C=N_G(v), d=|C|, and H=G-v. Then H
is connected, d>=1, and restriction of orientations induces a bijection

    A(G,q) <--> A(H,q) x C.                                      (2)

The C-coordinate is a vertex label, not an independently chosen total order.

**Proof.** Connectivity supplies d>=1. A path passing through v can replace a
segment a-v-b with the edge a-b, because C is a clique. Hence H is connected.

Let O be in A(G,q). The orientation of C union {v} is an acyclic tournament,
so it has a unique total order. The vertex v is not first, since it is not a
source. Its in-neighbors in C are a nonempty initial segment. Let p be the last
of these in-neighbors in the clique order; this is the C-coordinate in (2).

Deletion cannot introduce a directed cycle or give q positive indegree. If a
vertex w loses an incoming edge when v is deleted, then v->w. Since p->v and
C is ordered, also p->w. Thus w retains an incoming edge in H. No nonroot
source is introduced, and the restricted orientation belongs to A(H,q).

Conversely, take O_H in A(H,q) and p in C. Orient the edges incident to v by

    u -> v   if u=p or the edge u->p occurs in O_H;
    v -> u   otherwise.                                        (3)

The second case means p->u, because C is a clique. Formula (3) inserts v
immediately after p in the clique order. To see global acyclicity, take any
topological ordering of O_H and insert v immediately after p in that full
ordering. All members of C preceding p are then before v, and all other
members of C are after v. Every edge is oriented forward in this ordering.

The new vertex has an incoming edge p->v. No old incoming edge was removed.
If q belongs to C, it is first in the clique order, so q->v; otherwise q is
not adjacent to v. Thus q remains the unique source. The two constructions are
inverse: restriction recovers O_H and the last in-neighbor recovers p. QED.

The lemma really needs the simplicial hypothesis. On the 4-cycle with arcs
0->1->2->3 and 0->3, the root is 0. Deleting nonsimplicial vertex 1 creates a
second source at 2. Restriction is then not even a map to A(G-1,0).

## 3. Iteration: exact and approximate sampling

Choose a deterministic sequence of deletions v_1,...,v_k, never deleting q,
where v_i is simplicial in the graph then present. Let C_i be its surviving
neighbor set and d_i=|C_i|. Let H be the remaining induced graph, with h
vertices and b edges. The empty sequence is permitted. Iterating (2) gives

    A(G,q) <--> A(H,q) x product_i C_i,                          (4)
    |A(G,q)| = Z * product_i d_i,  Z=|A(H,q)|.                  (5)

All graphs along the sequence are connected. Each deleted edge belongs to
exactly one C_i incidence, so sum_i d_i = m-b.

**Exact sampler.** Draw O_H uniformly from A(H,q). Independently draw one
uniform vertex p_i from each fixed set C_i. Restore v_k,...,v_1 in reverse
order with (3), and output indegree minus one. By bijection (4), each output
has exactly probability

    1 / (Z * product_i d_i).

There is no rejection of whole orientations in this lifting step, no unknown
mixing time, and no bias from the number of topological orderings. Uniform
choices of p_i are sufficient even though their ranks in the clique order
depend on the already sampled orientation.

**Approximate transfer.** If the core sampler has law mu on A(H,q), use exactly
uniform independent p_i as above. Let L(mu) be the resulting law on maximal
parking functions, and U_H,U_G the respective uniform laws. Then

    TV(L(mu), U_G) = TV(mu, U_H).                               (6)

Indeed, each core state has the same D=product_i d_i extensions, each with
mass mu(O_H)/D. The half-sum of absolute differences is therefore
(1/2) sum_{O_H} D |mu(O_H)/D - 1/(ZD)|, which is exactly the right side.
Thus an epsilon-approximate core sampler yields an epsilon-approximate graph
sampler, with no dependence of the error bound on the number of deleted
vertices. Equation (6) assumes a valid core output and exactly uniform pivots;
it does not excuse failure probabilities or biased integer primitives.

### Algorithmic costs

Given the deletion certificate and O_H, reconstruction uses one test of an
already oriented pivot-neighbor edge per restored edge. It takes O(n+m) basic
operations with O(1) adjacency/direction lookup. A static adjacency matrix
prepared once provides this lookup, or sparse hash tables provide its expected
version. No global topological sorting or repeated sorting of clique neighbors
is needed. Computing indegrees is another O(n+m) pass.

Here is a completely specified polynomial preprocessing method. Maintain
M(u), the number of missing edges between pairs of surviving neighbors of u.
Initially compute all these numbers in O(n^3) adjacency queries. Repeatedly
delete the smallest-labelled nonroot vertex v with M(v)=0. For each surviving
neighbor u of v, subtract from M(u) the number of surviving w!=v adjacent to
u but not adjacent to v. These are exactly the disappearing missing pairs
{v,w}. Nonneighbors of v do not change their neighbor sets. An update uses
O(n^2) queries, so all updates and searches together cost O(n^3). The algorithm
may stop at any core; if run maximally, the remaining graph has no nonroot
simplicial vertex. The parameter b below refers to this actual computed core,
not an uncomputed optimal core.

The reviewed sampler implementation (omitted from this prose-only edition)
implements this preprocessing, the pivot reconstruction, and an exhaustive
core fallback. Its final orientation is sorted solely to give
reproducible output order; that formatting adds O(m log(m+1)) comparison work.
Its sparse direction sets use expected constant-time hashing. A deletion
certificate need not be recomputed for repeated draws.

### Low-level valid-plan contract

The reviewed lift and sample-from-plan helpers assume a plan produced by the
stated peeling procedure or independently verified as a valid root-preserving
simplicial-deletion certificate. They do not fully validate an arbitrary
externally supplied plan. The certificate is fixed independently of the sampled
orientations and randomness. This is a documentation clarification of the
reviewed interface, not an algorithm change.

### A general exact fixed-parameter fallback

For the core, enumerate the 2^b edge orientations, testing for acyclicity and
unique source q in O(h+b) graph operations. Count the valid orientations Z,
choose an exactly uniform integer in {0,...,Z-1}, and make a second enumeration
pass to select that valid orientation. No list of exponentially many
orientations is stored. Z>=1: ordering vertices by distance from q, breaking
ties deterministically, gives an acyclic orientation with every nonroot vertex
having an incoming edge from a nearer vertex.

The graph-operation cost of a fresh sample including preprocessing is

    O(n^3 + 2^b(h+b) + m log(m+1) + n),                         (7)

apart from arbitrary-precision arithmetic and fair-bit generation. Counts have
at most m+1 bits. A deliberately conservative additional bit-operation bound
for counting and optional product-count output is

    O((2^b+n)(m+1)^2).

Vertex-index manipulation is polynomial in log(n+1), too. Consequently this is
an exact fixed-parameter algorithm in b and is polynomial-time whenever
b=O(log(n+m+1)). In unrestricted graphs b can be m; (7) is then exponential.
There is no claim that b is always small or that this solves general efficient
sampling.

For exact random integers in {0,...,r-1}, draw ceil(log2 r) unbiased bits and
retry values >=r. A singleton uses no bits. Each call terminates almost surely,
uses fewer than two trials in expectation, and is exactly uniform. The core
choice uses at most 2b expected bits; all pivot choices together use at most
2 sum_i ceil(log2 d_i) <= 2(m-b). Thus the expected total is at most 2m fair
bits. The word-RAM graph-operation bound is deterministic except for these
integer retries; the sampler is Las Vegas with an almost-sure exact output,
not a bounded-time algorithm producing only an approximate law. The default
implementation uses Python's SystemRandom; the mathematical exactness theorem
is under the stated ideal independent-fair-bit interface. Seeded PRNG checks
verify code paths, not physical randomness.

## 4. Every chordal graph peels to the prescribed root

A graph is chordal if it has no induced cycle of length at least four. We include
the standard structural argument to avoid assuming that an arbitrary
elimination order happens to end at the desired root.

**Structural lemma.** Every connected noncomplete chordal graph has two
nonadjacent simplicial vertices.

**Proof by induction on the number of vertices.** Choose nonadjacent a,b and an
inclusion-minimal a-b vertex separator S contained in V minus {a,b}. Let A,B be the components of G-S
containing a,b. Every s in S has a neighbor in both A and B: a path from a to
b avoiding S minus {s}, which exists by minimality, proves this.

The set S is a clique. Otherwise choose nonadjacent x,y in S. A shortest
x-y path with internal vertices in A, and one with internal vertices in B,
exist. Each path is induced. There are no cross edges between A and B, and
shortestness rules out chords involving x or y within either path. Their
union is an induced cycle of length at least four, a contradiction.

The smaller induced chordal graph G[A union S] is connected. If complete, any
vertex in A is simplicial in G. If noncomplete, induction supplies two
nonadjacent simplicial vertices in it; since S is a clique, at least one lies
in A. That vertex has no neighbors outside A union S, and is simplicial in G.
Apply the same argument to B. The two chosen vertices are nonadjacent because
A and B are different components of G-S. QED.

In a complete graph every vertex is simplicial. Otherwise the lemma supplies
at least one simplicial vertex distinct from q. Deletion preserves chordality
and, by Section 2, connectivity. Thus greedy root-preserving peeling of a
connected chordal graph ends at {q}. In this case Z=1, b=0, and

    |MP(G,q)| = product_i d_i.                                 (8)

The algorithm above is an exact polynomial-time sampler for all such graphs,
with O(n^3) preprocessing and O(n+m) unsorted reconstruction per draw under
constant-time adjacency lookup. The reproducible Python output adds the stated
sorting and optional arbitrary-precision count costs. No claim is made here
that the supplied implementation has linear total preprocessing time.

## 5. A source-reading correction: adding a universal sink

For any rooted simple graph (G,q), add a new vertex t adjacent to every vertex
of G; call the resulting graph G^+. There is a bijection

    A(G,q) <--> bipolar (q,t)-orientations of G^+.              (9)

Extend O by directing every new edge v->t. This preserves acyclicity and all
old indegrees, makes t the only sink, and leaves q the only source. Conversely,
in every bipolar (q,t)-orientation all edges incident to t point into t.
Deleting t leaves old indegrees unchanged, so q remains the unique source and
acyclicity is preserved. These maps are inverse.

If G is chordal, so is G^+: an induced cycle of length at least four avoiding
t would already occur in G, while any such cycle containing t has a chord
from t to a nonconsecutive vertex. Moreover, G^+ is connected and q!=t.
The bipolar state space is nonempty by the root-distance construction above.

Bezáková–Sun's Theorem 3 states an exact uniform O(|E|) bipolar (s,t)-orientation
sampler on connected chordal graphs [3]. Applying its stated theorem to
G^+ and then (9),(1) gives the maximal-parking sampler in O(n+m) time in that
paper's sampling model. This is a direct implication of that theorem, rather
than a new chordal-sampling theorem. Its hypotheses are satisfied here.

**Inspection limit.** The retrieved complete 12-page proceedings PDF contains
the precise bipolar definition and Theorem 3 on printed/PDF page 11. It gives
a sketch, and Section 4 refers detailed proofs to an appendix that is not
present in these retrieved 12 pages. We have not audited that missing appendix
or implemented its claimed linear-time algorithm. Our self-contained
polynomial-time theorem and implementation above do not depend on that missing
proof. Also, a general statement about sampling a bipolar orientation requires
a nonempty state space; our cone construction explicitly guarantees one.

Although all-acyclic, bipolar, and fixed-source state spaces are different,
(9) allows an exact transfer. The chordal case is therefore not an unfilled
research gap or a novel result of this note. No conclusion about unrestricted graphs follows, because coning does
not turn a nonchordal graph into a chordal one.

## 6. Concrete tests and obstructions

The historical verification receipts record the checks summarized below.
Executable test programs and detailed receipts are omitted from this edition;
public verification metadata preserves the recorded counts and match results.
The reviewed test suite uses exhaustive parameter enumeration, not merely
sample frequencies.

* Every connected labelled graph on 1 through 5 vertices is tested at every
  possible root. Independent DFS enumeration supplies its rooted acyclic
  orientations. The complete core-orientation/pivot product is compared with
  that set, checking both equality of support and multiplicity exactly one.
* Independently, all candidate parking vectors within the singleton degree
  bounds are checked against **every nonempty subset** in the original parking
  definition. Coordinatewise maximal vectors are computed and compared with
  the orientation outputs. This does not assume the maximum-sum theorem.
* Every eligible one-step simplicial deletion in those graphs is checked for
  preservation of the unique root source and constant fiber size d, including
  simplicial roots being deliberately retained.
* Fifty deterministic pseudorandom connected 6-vertex graphs are checked at
  every root with exhaustive orientation/product enumeration, separately from
  the original-definition parking tests above.
* Universal-sink bijections are exhaustively checked for every connected
  labelled graph on at most 4 vertices and every root.
* The diamond rooted at a shared-edge endpoint has four target orientations.
  Uniformly permuting the three nonroot vertices produces fiber multiplicities
  1,1,2,2. Thus even conditioning the order to start with the root is biased
  (here the root is universal, so every such order is valid). The pivot sampler
  instead has four equally likely parameter choices.
* A 4-cycle 0-1-2-3-0 with a new vertex joined to both ends of edge 0-1 has
  a nonchordal 4-cycle core and one degree-two simplicial deletion. The core's
  three states lift to exactly six states. This is also a single block outside
  the previous bridge/cycle/clique-block class.
* Negative controls check failure of nonsimplicial deletion, rejection of loops,
  duplicate/parallel edges, disconnected inputs and invalid roots, and the
  out-of-range rejection branch of the exact integer primitive.

These finite checks are corroboration and regression tests; the proofs in
Sections 1–5 establish the general statements. The implementation never samples
an arbitrary spanning tree and silently declares its image maximal. Exact
counting difficulty alone is not an impossibility proof for exact sampling.

## 7. Remaining question and stopping point

The stated AIM problem [1] asks for uniform efficient sampling in general. The
method here may leave an arbitrary large irreducible core, and exhaustive core
sampling is exponential. No general exact polynomial-time sampler, FPAUS,
rapid-mixing bound, or unconditional impossibility theorem is established.
The bounded source search did not verify a general resolution; absence from
this search is not proof of absence in the literature. The result is a proved partial sampling theorem with unestablished novelty
and a literature-scope clarification, not a solution of the unrestricted
problem.

## Public references

[1] S. Hopkins, recorder, *Problems from the AIM chip-firing workshop* (2013),
Problem 5. The recorder identifies the entries as summaries rather than direct
quotations. [Author-hosted complete notes](https://www.samuelfhopkins.com/docs/aim_chip-firing_problems.pdf).

[2] B. Benson, D. Chakrabarty and P. Tetali, *G-parking functions, acyclic
orientations and spanning trees*, Discrete Mathematics 310 (2010), 1340–1353.
Theorem 3.1 and Corollary 3.2; concluding sampling discussion in Section 7.
[Primary preprint](https://arxiv.org/abs/0801.1114),
[complete PDF](https://arxiv.org/pdf/0801.1114).

[3] I. Bezáková and W. Sun, *Counting and Sampling Orientations on Chordal
Graphs*, WALCOM 2022, LNCS 13174, 352–364, Theorem 3.
[DOI](https://doi.org/10.1007/978-3-030-96731-4_29),
[NSF-hosted proceedings PDF](https://par.nsf.gov/servlets/purl/10355288).
