# Independent reconstruction of the binary matching gadget

Scope: this document proves an exact reduction, including its bit bounds. It
does **not** validate any external approximate-counting algorithm. No statement
in the prior triage notes was used as a certificate. The construction is the
one in the original project request, independently reconstructed here.

## Precise claim

Let `A` be a symmetric matrix of even order `n = 2m`, with nonnegative rational
off-diagonal entries given explicitly in binary. Its diagonal is ignored. There
is a deterministic polynomial-bit-time construction of a finite simple graph
`H` and a positive integer `D` such that

\[
 \#\operatorname{PM}(H)=D^m\operatorname{haf}(A).
\]

There is an explicitly computable projection from perfect matchings of `H` to
perfect matchings of the support graph of `A`. The fiber over a support matching
`M` has size

\[
 D^m\prod_{e\in M}A_e.
\]

Consequently, the projection of the uniform distribution on perfect matchings
of `H`, when this set is nonempty, is exactly the normalized rational-weighted
matching distribution. The empty graph has one perfect matching and the
order-zero hafnian is one.

## 1. A binary DAG with exactly W paths

Write the positive integer `W` in binary as `1 b_2 ... b_l`, where
`l = floor(log_2 W)+1`. Begin with distinct vertices `s,t` and the arc `s -> t`.
At a step with bit `b`, let `t_old` be the current sink. Add two fresh vertices
`a,z` and arcs

\[
 t_{\rm old}\to z,\qquad t_{\rm old}\to a,\qquad a\to z,
\]

and add `s -> z` exactly when `b=1`. Set the current sink to `z`.

Every arc points forward in the creation order, with the new vertex `a` placed
before the new vertex `z`. The digraph is therefore acyclic. Its source has no
incoming arcs and its final sink has no outgoing arcs. Arcs are distinct: `a,z`
are fresh, and `t_old != s`, so the optional arc `s -> z` differs from
`t_old -> z`. There are no loops.

Suppose the previous graph has `w` paths from `s` to `t_old`. Every old path
gives exactly two new paths to `z`, extending either directly or via `a`.
There is exactly one further path, the new single arc `s -> z`, when `b=1`.
These classes are exhaustive because the only arcs entering `z` are the ones
just specified, and `a` has only the incoming arc from `t_old`. Thus the number
of new paths is `2w+b`. Induction on the bits gives exactly `W` paths. This
includes `W=1`, for which there are no recurrence steps.

The DAG has `2l` vertices, `2l-2` internal vertices, and

\[
 1+3(l-1)+\sum_{r=2}^l b_r\le 4l-3
\]

arcs. In particular, its size depends on the binary length of `W`, not on `W`.

## 2. Split vertices and the full boundary signature

For each internal vertex `i`, introduce two distinct vertices `L_i,R_i` and an
identity edge `L_i R_i`. Introduce the terminal `L_s` and the terminal `R_t`.
There is no `R_s` and no `L_t`. For every directed arc `i -> j`, introduce the
edge `L_i R_j`. This is well-defined because no arc enters `s` or exits `t`.
Denote the resulting graph by `K_W`, and its terminals by `x=L_s,y=R_t`.

This graph is simple. Distinct arcs yield distinct edges, and no arc edge is an
identity edge because the DAG has no loops. The vertices have labels on two
disjoint sides, so reversing the orientation of an undirected edge cannot
identify different arc edges.

Consider a perfect matching of `K_W`. An internal vertex pair is either matched
by its identity edge or by two arc edges, one entering `R_i` and one exiting
`L_i`. In fact, if either member is matched to an arc edge, the identity edge
cannot be used; the other member must also use an arc edge. Therefore the
selected directed arcs have indegree and outdegree both one at every internal
vertex they visit, indegree zero and outdegree one at `s`, and indegree one and
outdegree zero at `t`.

Starting at `s`, following the selected outgoing arcs cannot repeat a vertex,
because the DAG is acyclic. It cannot stop at an internal vertex, because the
incoming selected arc forces an outgoing one there. Hence it ends at `t`.
There are no other selected arcs: any additional component with balanced
indegree and outdegree one would contain a directed cycle (follow outgoing
arcs in that finite component), contrary to acyclicity. This proves that a
perfect matching selects exactly one directed `s`-to-`t` path, with identity
edges on all internal vertices outside the path.

Conversely, select the arc edges on any directed `s`-to-`t` path and the identity
edges at every internal vertex outside that path. Every split vertex and each
terminal is covered exactly once. These two maps are inverse bijections, so
`K_W` has exactly `W` perfect matchings.

Now remove both terminals. Any selected arc component in a perfect matching
would have equal indegree and outdegree one at every visited vertex. Following
arcs would produce a directed cycle. Thus no arc edge is selected, and the
unique perfect matching consists of all identity edges. This proof also covers
the empty graph left when `W=1`.

Finally, removing exactly one terminal leaves an odd number of vertices, hence
no perfect matching. In the order `(both present, both removed, x removed,
y removed)`, the exact signature is therefore

\[
 (W,1,0,0).
\]

The gadget has exactly `4l-2` vertices, including the two terminals, and at most
`6l-5` edges (the arc edges plus `2l-2` identity edges). Its number of internal
vertices is `4l-4`, which is even.

## 3. Global gluing and the parity obligation

Let `G` be a simple graph on the `n` original vertices, with positive integer
weight `W_e` on each edge. Replace each edge `e={u,v}` by a fresh copy of
`K_{W_e}`, identifying its terminals with `u,v` in an arbitrary fixed order.
All gadget internal vertices are distinct. Retain all original vertices,
including isolated ones. The output `H` is simple: edges involving internal
vertices cannot collide across gadgets, and a gadget's direct terminal edge
(if present) is between its own unique original pair. There is at most one
original edge per original pair.

Let `P` be a perfect matching of `H`. For a gadget `e`, let `c_e` be the number
of its two original endpoints covered by matching edges belonging to that
gadget. All of its internal vertices are covered by edges in that gadget,
since they have no neighbors elsewhere. The restriction of `P` thus covers
`(4l_e-4)+c_e` vertices inside the gadget, an even number. Since its internal
count is even, `c_e` is either zero or two. This local parity argument is
necessary: sharing endpoints does not mean every gadget retains both terminals
in its matching restriction.

At each original vertex exactly one matching edge is selected, so exactly one
incident gadget uses that vertex. The gadgets with `c_e=2` consequently form a
perfect matching `M` of `G`. A gadget with `c_e=2` has exactly `W_e` possible
matching restrictions; a gadget with `c_e=0` has exactly one. Restrictions have
disjoint internal vertices, and their selected endpoint sets are disjoint
because `M` is a matching. They can therefore be combined independently.

More formally, the preceding projection gives a bijection

\[
 \operatorname{PM}(H)\ \longleftrightarrow\
 \bigsqcup_{M\in\operatorname{PM}(G)}
 \left(\prod_{e\in M}\operatorname{PM}(K_{W_e})\right)
 \times
 \left(\prod_{e\notin M}\operatorname{PM}(K_{W_e}-\{x_e,y_e\})\right).
\]

Each right-hand tuple specifies a unique union matching, and projection
recovers `M` and every tuple member. This is stronger than a numerical identity:
it identifies every fiber and the exact law of its projection. It yields

\[
 \#\operatorname{PM}(H)=\sum_{M\in\operatorname{PM}(G)}\prod_{e\in M}W_e.
\]

## 4. Rational scaling and polynomial bit size

Delete all zero-weight support edges. For each positive edge, write
`A_e=p_e/q_e`, where `p_e,q_e` are positive binary integers. Reduction to lowest
terms is optional mathematically; the implementation uses exact normalized
fractions. Define

\[
 D=\prod_{e:A_e>0}q_e,\qquad W_e=p_e(D/q_e).
\]

The empty denominator product is one. Each `W_e` is a positive integer. Every
perfect matching has exactly `m` edges, so its integer weight is exactly
`D^m` times its original rational weight. The identity and fiber sizes in the
claim now follow from Section 3.

Let `L` be the complete explicit binary input length, including all rational
entries and dimensions. Let `E` be the number of positive support edges.
The number of original vertices and `E` are at most a constant multiple of
`L` under an explicit matrix encoding. By the elementary product bit bound,

\[
 \operatorname{bits}(D)\le 1+\sum_{e:A_e>0}\operatorname{bits}(q_e)=O(L),
\]

and

\[
 l_e=\operatorname{bits}(W_e)
 \le \operatorname{bits}(p_e)+\operatorname{bits}(D)=O(L).
\]

In fact `sum_e l_e=O(L+EL)=O(L^2)`. The expansion therefore has

\[
 |V(H)|=n+\sum_e(4l_e-4)=O(L^2),\qquad
 |E(H)|\le\sum_e(6l_e-5)=O(L^2).
\]

Binary multiplication, exact division and optional gcd normalization take
polynomial bit time on these operands. Constructing the DAGs, split vertices,
and graph labels likewise takes polynomial bit time. The value `D^m` has
`O(mL)=O(L^2)` bits and is computable by polynomial-time integer arithmetic.
Thus scaling an explicitly represented rational approximation back by `D^m`
also takes polynomial bit time. There is no enumeration of `W_e` objects in
the construction.

## 5. Consequences and boundary cases

* `m=0`: return the empty graph, `D=1`, and hafnian one. There is one empty
  matching and its normalized law is a point mass.
* No perfect matching: the support graph and expanded graph are simultaneously
  without perfect matchings. Exact zero detection can be performed on the
  support graph by a correct polynomial-time general-graph matching decision
  algorithm. This statement is independent of any approximation dependency.
* Disconnected support: the gluing proof is local and needs no connectivity.
  An odd-order connected component forces zero; positive disconnected cases
  are handled by the same product and sum identities.
* Weights below one, very large denominators, and extremely small nonzero
  hafnians: no lower bound on their magnitude is assumed. Common-denominator
  scaling uses their binary lengths. Relative error is preserved by division
  by the positive factor `D^m`.
* Diagonal entries have no role. Signed or complex off-diagonal entries are
  outside the theorem. Zero edges must be deleted rather than supplied to a
  positive-integer gadget.

If an externally validated FPRAS counts perfect matchings of finite simple
graphs in polynomial **bit** time, calling it on `H` and dividing its answer
by `D^m` gives exactly the same relative-error and failure-probability guarantee
for `haf(A)`. Its size input is polynomial in `L`, so the resulting running
time is polynomial in `L`, `epsilon^{-1}`, and `log(delta^{-1})`. This is a
conditional transfer, not an audit of the external premise.

Likewise, if a sampler on `H` has output distribution `Q` within TV distance
`eta` of its uniform perfect-matching law `U`, the projection has distance at
most `eta` from the exact weighted law. Indeed for any event `B` of original
matchings, `|Q(pi^{-1}(B))-U(pi^{-1}(B))| <= eta`; take the supremum over `B`.
The projection scans a matching and gadget ownership in polynomial time. This
conditional transfer does not infer the existence of an efficient sampler
from the word FPRAS. A separate valid sampler or analyzed counting
self-reduction is still required.

## 6. Reproduced finite evidence and exact remaining scope

`code/gadget.py` implements the construction, exact rational hafnian recursion,
independent graph subset counting, matching enumeration, and certificate-
checking projection. The two exact counters have exponential worst-case
runtime and are reference verification routines, not approximation algorithms.

Run, from the project directory:

```text
python3 code/test_gadget.py
```

The script writes `data/gadget_verification.json`, including software version,
run time, source hashes and individual observed signatures. The reproduced
checks include all `W=1,...,64`; all 729 weight assignments from `{0,1,2}` to
the six edges on four vertices; 40 reproducibly seeded six-vertex weighted
instances; 12 boundary cases, including the denominator `2^512` (513 bits), a 257-bit
numerator, and different large denominators on disconnected edges; and all
fibers of one small weighted four-vertex graph. In the latter test the observed
fiber counts are separately compared with the products of edge weights.

All these checks passed in the recorded run. They are finite corroboration of
the proof, and do not replace the argument or certify an upstream FPRAS.
No full sampling-algorithm validation, priority claim, or unconditional
approximation theorem is established by this document.

## Checkpoint

2026-10-06 22:16 America/Los_Angeles (2026-10-07 05:16 UTC).

Independent exact-reduction reconstruction: complete. Best-guess completion
for this subtask is 100%; completion of the overall approximation/sampling
research and publication goal is not assessed here. The parent research log
must separately assess the unresolved external algorithm and publication
conditions. This checkpoint is an evidentiary status, not a proof premise.
