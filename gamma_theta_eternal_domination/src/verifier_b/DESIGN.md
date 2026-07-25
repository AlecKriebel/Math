# Verifier B design and trust boundary

Verifier B is an independent, exact implementation for small graphs (the
campaign target is currently \(n\leq 12\)).  Its purpose is differential
checking, not maximum throughput.

## Representation

- A graph is a tuple of `frozenset` neighborhoods on vertices
  `0, ..., n-1`.
- Vertex subsets and guard configurations are `frozenset` objects.
- Algorithms use ordinary set membership, `itertools.combinations`, explicit
  dictionaries, and recursive color assignments.  There are no packed graph
  integers, bit masks, SAT calls, NetworkX calls, or imports from verifier A.

This is intentionally structurally unlike verifier A's bitset core.  A common
representation or transition routine would make a differential agreement much
less informative.

## One-guard eternal domination

For a requested guard count \(k\), `build_colored_configuration_digraph`
enumerates every dominating \(k\)-subset.  For each such source \(D\) and each
unoccupied attack \(r\notin D\), it explicitly records one arc for every guard
\(u\in D\cap N(r)\) for which

\[
    D'=(D-\{u\})\cup\{r\}
\]

is another dominating \(k\)-configuration.  An arc stores all four pieces of
data: source, attack color, moved guard, and target.  Thus an arc represents
exactly one guard traversing exactly one graph edge.  Occupied vertices are not
attack colors.

Starting with all digraph vertices, `greatest_closed_family` simultaneously
deletes any configuration having an attack color with no arc into the current
set.  At termination, a nonempty remainder is precisely a family closed under
every legal attack.  This is a direct greatest-fixed-point computation on the
explicit colored digraph.

For decisive positive checks, `verify_eternal_family` does **not** call the
digraph builder or its transition tables.  It checks domination and every
source/attack response directly from the definition.  Explicit response
certificates receive an additional field-by-field check.

The empty graph is assigned the conventional value
\(\gamma^\infty(\varnothing)=0\).  For every nonempty graph, zero guards are
rejected and attacks are only at unoccupied vertices, exactly as in the
campaign model.

## Other exact parameters

- `gamma`: increasing exhaustive search over dominating subsets.
- `i`: increasing exhaustive search over independent dominating subsets,
  equivalently maximal independent sets.
- `alpha`: decreasing exhaustive search over independent subsets.
- `theta`: complete DSATUR-style backtracking coloring of the **complement**.
  Color names are introduced consecutively; this only quotients permutations
  of color names.
- graph6: a local parser/writer using the graph6 upper-triangle ordering,
  including strict payload and padding validation.

All search orders are deterministic.  At order 12 the largest subset layer has
924 configurations, so the implementation remains suitable for independent
candidate checking on the campaign laptop.  It is not intended for blind
enumeration of all order-12 graphs.

## Tests and model traps

`tests/test_verifier_b.py` includes hand examples, all labeled graphs through
order four against small transparent brute-force oracles, graph6 round trips,
certificate tampering, and explicit traps for:

- allowing attacks at occupied vertices;
- allowing simultaneous movement of all guards (`C5` with two guards);
- accepting a one-round defense whose resulting configurations do not
  dominate (`P3` with one guard);
- confusing clique cover with coloring the original graph; and
- admitting arcs that move more than one guard or do not traverse an edge.

No claim should rely solely on this stack.  Its value is as an implementation
and representation independent of the generator and verifier A.
