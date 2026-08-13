# Adversarial review: theta-2 five-port signature gate

Verdict: **VERIFIED within the stated scope**.

The replay closes the previously unresolved upstream algebraic-completeness
check for the five-port theta-2 minimum support.  It does not rely on the old
atlas compiler, graph canonicalizer, Fourier engine, invariant evaluator, or
relation IDs.  The primitive arcs and repairs are written explicitly; the
only project files read are inert coefficient/core data and the frozen root
records used as comparison inputs.

The most important correction is that the three common signature hashes are
not themselves treated as proof.  Expansion gives 192 raw survivors.  The
intrinsic omitted-role test and an independent standard mixed-graph
canonicalizer prove the exact partition:

```text
18 direct labelled isomorphisms
42 nonretaining selected-incoming root-presentation duplicates
132 nonretaining marginalized-incoming restoration roots
```

The 132 regenerated marginalized roots equal the frozen 132-root inventory
as a canonical decorated-relation multiset, and all presentation transports
are explicit.  The 42 additional selected-incoming descriptions map to
already represented frozen classes; they are not silently dropped by count.

The audit deliberately preserves three fail-closed artifacts:

- the first mutation run, where a nominal wrong-width mutation was not
  rejected;
- the first 192-versus-132 provenance comparison, which correctly failed;
- the second mutation run, showing that five-wide complement-before-
  projection is mathematically vacuous on zero-sum quartets.

The active replay corrects these issues and all active mutations pass.

Residual scope: this directory verifies only the five-port theta-2 signature
filter and its binding to the frozen restoration-root inventory.  It does not
verify the downstream 2,106-state restoration hard cover, the three-outgoing
core gate, probe coherence, arbitrary subdivisions, bridge arguments, or the
global JC theorem.  Those claims require their own certificates.

