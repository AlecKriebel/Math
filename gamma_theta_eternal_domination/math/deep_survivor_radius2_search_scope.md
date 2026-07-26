# Radius-two robustness probe around `Kun_w{vRrblV`

Status: **OBSERVED** bounded computation.

The fixed labeled graph is the canonical order-12, size-40 Graph6 record
`Kun_w{vRrblV`.  It was singled out by the transition-kernel experiment
because its forced maximum-independent states survive unusually many deletion
rounds.  That fact motivates this local probe but is not used as a correctness
assumption.

## Exact search universe

Order the 66 unordered pairs of vertices as
`combinations(range(12), 2)`.  For every subset of pair indices of cardinality
zero, one, or two, toggle exactly those adjacencies in the fixed labeled graph.
The raw universe therefore has

\[
  \binom{66}{0}+\binom{66}{1}+\binom{66}{2}
  =1+66+2145=2212
\]

labeled origins.  No isomorphism pruning occurs before these origins are
formed.  The pinned nauty 2.9.3 `labelg -q -g` canonicalizes all 2,212 records
in origin order.  Canonical multiplicities are retained, so their sum must
remain 2,212.

Each distinct canonical graph is then evaluated exactly by both campaign
stacks:

- stack A uses bitsets, exhaustive subset invariants, subset dynamic
  programming for clique cover, and greatest-fixed-point deletion for the
  one-guard game;
- stack B uses frozenset graphs, independent exhaustive subset routines,
  complement DSATUR coloring, and an explicit colored configuration digraph.

Both stacks must agree on
\(\gamma,i,\alpha,\gamma^\infty,\theta\), on every eternal decision from
\(\gamma\) through the first successful guard count, and on the winning
greatest eternal family after representation normalization.

## Interpretation and limit

The computation asks whether a conjecture counterexample occurs within two
edge toggles of this one graph.  A negative answer is local robustness
evidence only.  It does not cover all order-12 graphs, any graph beyond edit
distance two, or the full `n=12,k=3` slice.  The same program forms the
universe and checks its coverage, and the exact coloring conclusions do not
carry proof logs in this artifact.  Consequently the result is labeled
`OBSERVED`, not `CERTIFIED-FINITE`.
