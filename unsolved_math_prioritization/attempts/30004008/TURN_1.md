# Turn 1: localization to the common source component

Status: a proved reduction and sufficient condition, not a solution of the arbitrary-root conjecture. No novelty claim.

## 1. Unique source component

Let A_1,...,A_q be spanning out-arborescences on V, q≥1, with roots r_i, and let D be their colored union. Every r_i reaches every vertex in D, and any two roots reach one another. Let S be their common strongly connected component. No arc enters S: if x outside S had an arc into S, a root could reach x and x could return to the root, a contradiction. Since a root reaches every component, S is the unique source component of the condensation digraph.

For each i, A_i[S] is a spanning out-arborescence on S with the same root. Indeed, the A_i path from r_i to a vertex of S cannot leave S and return, since no arc enters S. Its restrictions therefore reach every vertex of S, preserve indegrees, and are acyclic. This assertion includes the singleton case, where the restricted trees are empty.

## 2. Exact rainbow localization for q=n-1

**Theorem.** Put s=|S|. The original instance has a rainbow spanning arborescence if and only if there is a set J of s-1 colors for which the restricted trees (A_i[S]:i∈J) have a rainbow spanning arborescence on S. For s=1, J is empty and the one-vertex tree is the local witness.

For the forward direction, any spanning out-arborescence B of D has its root in S: otherwise it could not reach S without an entering arc. Its paths to S stay in S, so B[S] is a tree with s-1 arcs and thus uses s-1 distinct colors.

For the converse, start with a local witness B on S. Process all unused colors in any order. Its color root r_i lies in S and hence in the current vertex set X. If X is proper, the A_i path to any vertex outside X has a first arc leaving X. Add that arc and its new head. This extends the out-arborescence and preserves distinct colors. There are exactly n-s unused colors, so after those steps all n vertices are reached. Every color is used exactly once. The argument uses actual colored arcs; parallel endpoint pairs cause no identification.

In particular, if the full conjecture holds on s vertices then it holds for this instance, since *any* s-1 restricted colors may be chosen. A vertex-minimal counterexample must have a strongly connected union. This reduction alone gives no answer when S=V.

## 3. A quantitative sufficient condition from credited multi-root theory

Let R be the number of distinct input roots and let a≥b≥0 be the two largest root multiplicities, padding with zero if R=1. The maximum number of colors selectable while allowing at most two vertices to have multiplicity ≥2 is

M = R + (a-1)_+ + (b-1)_+.

To prove this, keep at most one color from every root except at most two chosen roots; the two largest excesses maximize the capacity. Conversely, keeping all colors of those two roots and one from every other root realizes M. Deleting colors preserves the property, so every size from 0 through M is achievable.

Therefore, if s-1≤M, choose s-1 colors of that kind and apply the credited at-most-two-multi-roots theorem, Theorem4.5 of [the primary paper](https://arxiv.org/abs/2412.15457v2), on S. Then extend by Section2. The s=1 case requires no imported theorem. When R≥2, the condition reads s≤R+a+b-1. A failed condition is only an obstruction to this sufficient criterion, never evidence of a counterexample.

For example, source size4 and six colors with root multiplicities(2,2,2) satisfy M=5≥3, despite having three multi-roots globally. Three colors suffice on the source, and the other three extend to a seven-vertex ambient instance. This example illustrates the reduction; small-order existence is already known.

## 4. Credited implications and precise gap

The paper's theorem for n≤6 yields a theorem for arbitrary ambient n whenever s≤6. Its reported finite verification n≤8 likewise transfers to s≤8, conditional on that published computation, which this packet does not independently reproduce. Neither statement is new small-order verification.

The hard part remains strongly connected source instances beyond the proved/verified small orders with sufficiently distributed repeated roots. The localization establishes an exact subinstance criterion, not a method that always solves the local instance. The finite tests below validate implementation and boundary cases; the proof above establishes the unbounded reduction.

## 5. Reproducibility

Run `python verify_turn1.py`; compare stdout with TURN_1_CHECKS.json. Controls enumerate all color multisets of rooted labeled trees on up to four vertices, verify every restricted color subset, lift witnesses, and separately check the multiplicity capacity formula. Additional deterministic larger constructed instances exercise proper source components. No external libraries or third-party search code are used.
