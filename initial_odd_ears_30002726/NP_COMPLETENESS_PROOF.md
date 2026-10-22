# NP-completeness of maximizing an initial odd-ear prefix

Prepared 20 October 2026. This is an authored proof for independent mathematical
review, not a claim of external peer review or a certified literature-novelty
claim. No third-party source text is reproduced here.

## The exact decision problem

The input is a finite undirected loopless 2-vertex-connected graph G with at
least three vertices, and an integer t. Parallel edges are permitted in the
general problem. An open ear decomposition starts with a circuit and continues
with paths whose distinct endpoints are already present and whose internal
vertices are new. The ears partition E(G). The initial circuit counts as one
ear, as does an ear consisting of a single edge. An ear is odd when its number
of edges is odd.

Let beta(G) be the maximum number of consecutive odd ears at the start of such
a decomposition. The question is whether beta(G) >= t. Odd ears after the
first even ear do not count.

## Theorem

The decision problem beta(G) >= t is NP-complete. NP-hardness holds even when
G is simple and has a universal vertex z such that G-z is bipartite and
connected. In particular, computing beta exactly in polynomial time would
imply P=NP.

The proof uses a polynomial-size many-one reduction from Set Cover. It uses
neither succinct edge weights nor parallel edges.

## 1. Factor-critical formulation

A graph H is factor-critical if H-v has a perfect matching for every vertex v.
For the precise open-ear convention above, the established characterization is

  beta(G) = max ( |E(H)| - |V(H)| + 1 ),

where H ranges over 2-vertex-connected factor-critical subgraphs of G. If no
such H exists the maximum is zero. See Benchetrit and Sebo, Section 3.1,
Theorem 3.2 and the paragraph defining beta:
https://arxiv.org/abs/1509.05586.

For clarity, this correspondence uses both directions. An all-odd prefix has
a 2-connected factor-critical union, and each ear increases the cyclomatic
number by one. Conversely a 2-connected factor-critical H has an all-odd open
ear decomposition. Its decomposition can be extended to G, since a
2-connected subgraph of a 2-connected graph can be extended by open ears;
unused edges with both endpoints already present are one-edge ears.

It is harmless, and optimal for a fixed vertex set, to make H induced.
Adding edges preserves factor-criticality and 2-vertex-connectivity and only
increases the objective. Thus the characterization also equals the maximum
over induced 2-connected factor-critical subgraphs.

## 2. Cone lemma

Let B be a connected bipartite graph with at least two vertices, and obtain G
by adding a new vertex z adjacent once to each vertex of B. Then

  beta(G) = max { |E(B[S])| : S is nonempty,
                    B[S] is connected and has a perfect matching }.

Proof. A factor-critical graph on at least three vertices cannot be bipartite.
Indeed its order is odd; in a connected bipartite graph of odd order, deleting
a vertex from the smaller class leaves unequal class sizes and therefore no
perfect matching. Consequently every eligible H in G contains z. Replace it
by the induced graph on its vertex set and write that set as S union {z}.

The cone over B[S] is 2-vertex-connected precisely when B[S] is connected:
deleting z leaves B[S], and deleting any other vertex leaves connectivity
through z. Its factor-criticality is equivalent to the existence of a perfect
matching M of B[S]. Necessity follows by deleting z. Conversely, after
deleting u in S, remove its M-edge uv and add zv; after deleting z use M.

There are |S|+1 vertices and |E(B[S])|+|S| edges in this cone. Its cyclomatic
number is therefore |E(B[S])|. This proves both inequalities in the identity.
Also G itself is 2-vertex-connected because B is connected. QED.

## 3. Set Cover input and preprocessing

A Set Cover instance consists of a universe U={1,...,m}, a family
A_1,...,A_n of subsets of U, and a budget s. The question is whether at most
s of the A_j cover U. Set Cover is NP-complete; a primary classical source is
Richard M. Karp, *Reducibility among Combinatorial Problems*, 1972:
https://doi.org/10.1007/978-1-4684-2001-2_9.

We may restrict to m>=1, n>=1, 1<=s<=n, and union_j A_j=U. Cases excluded by
these conditions are immediately decidable and can be mapped to fixed yes/no
instances. For example, a triangle has beta=1 and a four-cycle has beta=0;
threshold 1 supplies fixed yes and no outputs. Thus this restriction retains
NP-hardness. Empty sets in the family cause no difficulty.

Put

  T = sum_j (1 + |A_j|),
  k = T+n+3,
  M = (m+1)k^2,
  F = M-ks.

The letter k is a construction parameter, not the decision threshold. The
output threshold is F. Notice that k>T, k>s, and k^2>ks+T. In fact
k-s>=T+3, so k(k-s)>T. Also F>0.

## 4. Constructing the bipartite base

Take m+1 pairwise vertex-disjoint copies Q_0,Q_1,...,Q_m of K_(k,k).
Q_0 is the root block; Q_i corresponds to element i for i>=1.
Write the left and right classes in Q_i as L_i and R_i, each of size k.
Choose one distinguished right vertex q_i in each R_i.

For each set A_j, add one new left vertex c_j, called its connector. Join c_j
to q_0 and to q_i for each i in A_j. There are no other edges involving
connectors, and no edges between different blocks.

Call the resulting graph B. Its bipartition is

  left:  all L_i and all c_j;
  right: all R_i.

B is simple. It is connected: all connectors meet q_0, and each element block
has a connector neighbor because the union of the sets is U. It has

  |V(B)| = 2k(m+1)+n,
  |E(B)| = M+T.

Finally output the simple cone G over B and threshold t=F. Because k is
linear in n plus the explicitly listed set incidences, both G's vertex and
edge lists have polynomial size in the Set Cover input. The graph G is
2-vertex-connected and deleting its universal vertex leaves bipartite B.

## 5. A small cover yields beta(G)>=F

Suppose the input has a cover of size at most s. Delete redundant sets until
the chosen cover J is inclusion-minimal, and let r=|J|<=s. Each chosen set
A_j has a private element p(j), meaning p(j) is in no other chosen set. These
private elements are distinct. If a chosen set had no private element it
would be redundant, contradicting inclusion-minimality.

Form S from all block vertices and the r chosen connectors, with one left
vertex omitted from L_(p(j)) for each j in J. No right vertex is omitted, and
the root block is untouched. There is at most one omission in any block.

B[S] has a perfect matching. Match each c_j to q_(p(j)). In that assigned
block, after the omitted left vertex and externally matched right vertex are
removed, match the remaining K_(k-1,k-1). Match every other block internally
as K_(k,k). These edges are disjoint and cover every vertex of S.

B[S] is connected. Every retained block is connected, since k>=2; each
chosen connector meets the root block; and each element block meets at least
one chosen connector because J covers U.

Exactly r left block vertices, in distinct blocks, were omitted. This loses
exactly kr internal block edges. No connector incidence from a chosen
connector is lost, because all right vertices remain. Hence

  |E(B[S])| = M-kr + sum_(j in J)(1+|A_j|)
             >= M-ks = F.

The cone lemma gives beta(G)>=F.

## 6. beta(G)>=F yields a small cover

Suppose beta(G)>=F. By the cone lemma choose S such that B[S] is connected,
has a perfect matching, and has at least F edges. Let r be the number of
selected connector vertices. For each block Q_i let

  a_i = |L_i \ S|,   b_i = |R_i \ S|.

Thus 0<=a_i,b_i<=k. The number of retained internal edges in Q_i is
(k-a_i)(k-b_i), and its lost internal edge count is

  d_i = k(a_i+b_i)-a_i b_i.

First, every block retains at least one internal edge. If one retained none,
there would be at most M-k^2 internal block edges and at most T connector
edges in total. Consequently

  |E(B[S])| <= M-k^2+T < M-ks = F,

contradicting the choice of S.

Second, the perfect matching of the bipartite graph B[S] forces equality of
its left and right class sizes. Counting selected vertices gives

  sum_i (k-a_i) + r = sum_i (k-b_i),
  hence sum_i (a_i-b_i) = r.

For each i,

  d_i - k(a_i-b_i) = b_i(2k-a_i) >= 0.

Summing yields sum_i d_i >= kr. Since B has only T connector edges,

  |E(B[S])| <= M-kr+T.

Together with |E(B[S])|>=M-ks this implies k(r-s)<=T. The quantities r,s are
integers and k>T, so r<=s.

Finally, the sets whose connectors belong to S cover U. Fix an element i.
Its block has a retained internal edge, as does the root block. Because
B[S] is connected and different blocks have no direct edges, there must be
a retained edge from Q_i to a selected connector c_j. By construction this
is possible only when i belongs to A_j. Thus every element belongs to one
of the r selected sets, giving a cover of size r<=s.

This establishes the exact many-one equivalence

  Set Cover instance is yes  iff  beta(G)>=F.

## 7. Membership in NP and scope

A certificate for beta(G)>=t can specify a 2-connected factor-critical
subgraph H, and a perfect matching of H-v for each v in V(H). Its length is
polynomial in the graph size. One checks the edge and vertex sets, verifies
connectivity after every vertex deletion, verifies each supplied matching,
and checks |E(H)|-|V(H)|+1>=t. All these operations are polynomial. Threshold
t<=0 can be accepted directly. Thus the decision problem is in NP.

Combining membership with the reduction proves the theorem. The result is
consistent with fixed-parameter tractability in the target threshold and
with polynomial recognition of beta<=1. It does not claim NP-hardness for a
fixed value of t. It does not concern Frank's polynomially computable
maximum TOTAL number of odd ears.

## 8. Verification limits

This proof is self-contained apart from two established inputs: Set Cover
NP-completeness and the stated odd-ear/factor-critical characterization.
Finite exact computations are supporting debugging checks, not a substitute
for the reduction. Independent mathematical audit is recorded separately.
The bounded source search did not locate a prior resolution of the exact
target, but that does not certify novelty or exclude later publications.
