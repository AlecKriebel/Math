# Independent derivation checkpoint

Recorded 2026-10-15 04:08:39 UTC. Review search01, PR 570, problem 30006605,
frozen head 417ca52e83cf06b07c388d89c756cfd86473d5b0.

This checkpoint precedes access to the frozen packet's old `audit/` conclusions.
Read so far: bundle/PROOF.md, controls.py, SOURCE_STATUS.md; official MFO/DROPS
landing-page metadata. No other reviewer's findings have been requested or read.
The assignment is verification of candidate 1/5, not an additional discovery
attempt. Progress estimate: 20% of this algorithm/reduction audit.

## Independently derived claims

For a finite connected unit-edge graph, D=n-1 bounds all distances. At threshold
R>=0, let b(u) be the largest k in [0,D] with k w(u)<=R. Nonnegativity makes the
successful k values an initial interval, including zero; w(u)=0 gives b(u)=D.
Thus w(u)d(x,u)<=R iff d(x,u)<=b(u), and subtracting b(u) from D converts the
conjunction to max_u(d(x,u)+D-b(u))<=D. No median-graph property is used here.
There is no needed floor/division primitive: binary search on integer k suffices.

The optimum is an attained maximum k w(u) at a minimizing vertex, hence occurs
in n sorted rows [0,w(u),...,Dw(u)]. A feasible incumbent B exists at D max w.
Maintaining either B=rho or an active copy of rho suffices, so equal-to-pivot
entries may safely be discarded on either answer, provided feasible pivots are
saved. A weighted median of row midpoints with each midpoint assigned its row
length gives at least M/2 row length on each weak side. The lower midpoint has
at least L/2 row entries on each weak side, including even L and L=1. Consequently
pruning <=q on an infeasible answer, or >=q on a feasible answer, removes >=M/4.
Ties and all-zero rows strengthen this removal rather than obstructing it.

This establishes O(log n) oracle calls and O(n log^2 n) comparison/search overhead.
The claimed O(n log^5 n) theorem follows if the imported additive oracle applies
to adjacency-list input on all finite median graphs, takes nonnegative integer
labels <=D, and runs deterministically in O(n log^4 n). This review does not yet
certify that imported theorem's proof. Final all-centers recovery is a final
threshold call at rho; a saved witness is valid even if its initial upper bound
was not its actual radius.

## Adversarial checks still required

- Independently compare complete feasible sets and all centers with brute force.
- Check row-pruning invariants, weighted-median quantiles, contraction and query
  count on synthetic sorted rows as well as graph profiles.
- Cover n=1, all zero, one positive, optimum zero, asymmetric rational profiles,
  equal midpoints, singleton active rows, and extreme rational magnitudes.
- Reproduce full author JSON from a scratch copy; compare recorded output and
  verify packet seals without executing writing code in frozen originals.
- Confirm original finite vertex-center/real-profile/unit-edge question in the
  primary OWR source; distinguish the ESA prior search mechanism from this proof.
- Audit arithmetic counts, input-size assumptions, edge-read bound, and scope of
  reference controls (which do not implement the fast median-graph oracle).
