# Verifier A design

Verifier A represents vertices and vertex sets by integer bit masks. It does
not use NetworkX or a solver.

For fixed `k`, it enumerates every dominating `k`-configuration. Starting with
all of them, it repeatedly deletes a configuration if some unoccupied attack
has no surviving successor obtained by moving exactly one adjacent guard to
the attacked vertex. The terminal set is the greatest fixed point. It is
nonempty exactly when a size-`k` eternal family exists.

The other parameters use exhaustive subset enumeration. Clique cover uses the
exact recurrence

`f(S) = 1 + min(f(S \ C))`,

where `C` ranges over cliques in `S` containing a fixed pivot. The pivot makes
every clique partition appear in exactly one branch at that recurrence level.

Verifier B is required to use set-valued configurations, an explicit colored
configuration digraph, and an independently written coloring solver. It must
not import this package.
