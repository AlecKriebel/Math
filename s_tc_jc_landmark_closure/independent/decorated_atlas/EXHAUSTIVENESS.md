# Exhaustiveness certificate for the primitive universe

Status: **EXACTLY COMPUTED / PROVED for the bounded primitive universe**.

This note concerns only simple, binary, nonroot, fully reduced ported blobs
under `docs/DEFINITIONS_LOCK.md`. It does not promote the bounded universe to
arbitrary subdivisions and does not classify stochastic containment.

## 1. Core grammar

Delete the boundary leaves of a primitive ported blob but remember their
attachment vertices. Let `n2` and `n3` be the numbers of vertices of degree
two and three in the remaining biconnected core, and let `E` be its number of
edges. Binary reduction implies that every core vertex has degree two or
three. Hence

```text
2E = 2 n2 + 3 n3.
```

For cyclomatic number `beta = E-(n2+n3)+1`, substitution gives

```text
beta = n3/2 + 1.
```

Thus a rank-one core has `n3=0` and is a cycle. A rank-two core has exactly
two cubic vertices. Biconnectivity then decomposes it into three internally
vertex-disjoint paths between those vertices: a theta core. In a simple graph
at most one path may have no internal vertex, since two such paths would be
parallel edges. Conversely every cycle and every such theta is simple and
biconnected.

Every degree-two core vertex has exactly one boundary port, because it must
have degree three in the binary standard topology. A cubic pole has no port.
An unported degree-two vertex would have been suppressed by the locked
standard reduction. Consequently the implemented cycle words and weak
three-part theta compositions enumerate every fully reduced primitive core.

## 2. Reticulations and orientations

For each core the generator chooses the required reticulation vertices
directly: one for a cycle and two for a theta. It distinguishes one incoming
boundary. That boundary cannot meet a reticulation, because the reticulation
already requires two incoming core arcs. For each placement, every core edge
is assigned one of its two possible directions by a complete recursive
enumeration. The recursion prunes only when the remaining incident edges
cannot meet the prescribed binary indegree/outdegree quotas, so no feasible
orientation is removed.

At a completed orientation the generator independently checks:

- binary bidegrees;
- directed acyclicity;
- reachability from the incoming boundary;
- rooted tree-childness;
- the locked local arrow-tail condition;
- simplicity and level at most two.

The mixed graph is then subjected to a second admissible-rooting census. In
particular, `S_TC` is nonvacuous: at least one admissible rooting must exist,
and every admissible rooting must be tree-child.

## 3. Quotients and transports

Canonicalization refines the full vertex-colour partition and then
individualizes every unresolved cell. It therefore examines every
colour-preserving vertex permutation. The lexicographically least mixed
adjacency code is a complete isomorphism invariant, and the winning
permutation supplies the raw-to-canonical vertex map. Edge, port,
reticulation, and inheritance-parent transports are derived from that map,
not from an external topology identifier.

A decorated directed relation is canonicalized as one coloured disjoint
union. Source and target vertices have different side colours, and one
explicit `MATCH` edge encodes each element of the complete port bijection.
Therefore a common target graph cannot merge relations having different
sources, source embeddings, directions, or port correspondences.

## 4. Exact bounded counts

| ports | accepted raw presentations | role classes | labelled primitives | raw-to-labelled transports | decorated ordinary-T relations | displayed-signature collisions |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 72 | 7 | 39 | 42 | 18 | 0 |
| 5 | 326 | 29 | 660 | 696 | 192 | 0 |
| 6 | 972 | 83 | 9,720 | 9,960 | 1,800 | 0 |
| 7 | 2,307 | 198 | 138,060 | 142,560 | 17,280 | 0 |

For seven ports, the raw orientation audit has 6,342 bidegree-complete
orientations: 2,307 accepted, 2,268 rejected for a directed cycle, and 1,767
rejected by rooted tree-childness. The cycle/theta accepted split is
`42 + 2,265`.

## 5. Exact algebra compiler and claim boundary

For every labelled primitive, the compiler enumerates all reticulation
switchings, verifies that each is an arborescence, computes every edge's
descendant-port mask, and constructs any zero-sum JC Fourier coordinate as an
exact sparse integer polynomial in edge multipliers and inheritance
parameters. Complete tensor hashes are stored through five ports. For six and
seven ports, all switchings and masks are stored and the complete compiler is
replayable, while bounded tensor-probe hashes avoid materializing hundreds of
millions of redundant coordinate objects.

The displayed-parameter signature is only a sufficient equality certificate.
All 148,479 labelled records for four through seven ports have distinct such
signatures. Therefore no nonisomorphic/non-`T` *equal-signature candidate*
survives this test. This is not a proof that unequal signatures imply distinct
JC varieties, stochastic separation, or absence of one-sided containment.

The selected-completion universe is audited separately in
`SELECTED_STRENGTH_CORRECTION.md`. In particular, dummy repair leaves belong
to a full completion and are not themselves a failure-of-core-retention
certificate. The audited predicate only decides retention of the original
primitive core as a strong factor. It does not decide intrinsic selected
`S_TC` membership after arbitrary `red_*`; a cycle sink omission can reduce to
a strong tree.
