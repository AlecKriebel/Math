# Research log

## 2026-07-24 00:20 PDT

- Defined two qualitatively different construction targets: the exact
  centered quarter-grid \(X=12,Y=-51\) pseudomarginal profile and the best
  stored unrestricted binary64 configurations for \(N=41,\ldots,44\).
- Implemented a Riemannian-Adam population search with a differentiable
  maximum-inner-product objective, a soft seven-bin profile, sorted row
  energy matching, and centering.  Profile-guided schedules explicitly set
  all auxiliary weights to zero for the final two phases.
- Added asymmetric Gaussian starts, tangent perturbations, six-temperature
  replica exchange, and an explicit delete/reinsert topology change using
  4,000 asymmetric candidate points.
- Ran deterministic seeds 2026072400 through 2026072701.  The eight
  populations made 776 replica-exchange attempts and accepted 500.
- No point set had maximum inner product at most \(1/2\).  The best
  \(N=41,42,43\) values remained the inherited numerical benchmarks.
- The profile-guided \(N=41\) branch temporarily reached a much closer
  shadow descriptor but maximum \(0.56838\).  After penalty release and
  direct minimax polish it returned to the known 35+6 active-core basin at
  \(0.5149946525121685\).  This is evidence against, not a proof against,
  an X=12-induced competitive basin.
- Direct minimax polishing produced a new numerical \(N=44\) record
  \(0.5274577123235293\), an improvement of about \(1.3480\cdot10^{-5}\).
  The best descendant came from the unrestricted control, slightly ahead
  of the profile-guided descendant \(0.5274590715832641\).
- Added independent binary64 and 90-digit Decimal recomputation.  The new
  \(N=44\) coordinate hash is
  `d862f8be8e94cbb9fb6923f5f3fe2e9518dadcd87375741de270116f25627612`.
  Five baseline/tamper tests pass.  All claims remain numerical only.

## 2026-07-24 00:30 PDT

- Extracted the \(5\cdot10^{-4}\)-near-maximum graph and numerical
  nonnegative tangent stress from each best \(N=41,\ldots,44\) source.
- Exact bitset searches found maximum independent-set sizes
  \(15,15,15,16\), hence minimum tight-edge vertex-cover sizes
  \(26,27,28,28\).  A separate Bron--Kerbosch implementation reproduced all
  four optima and was checked against brute force on 270 small random graphs.
- For every cardinality and four deterministic seeds, removed the complete
  minimum cover, reinserted all removed points sequentially from distinct
  asymmetric random caps, optimized the whole block against a frozen
  independent complement for 1,300 iterations, released all vertices for
  1,300 iterations, and ran direct epigraph polish.
- No restart beat its source at \(10^{-12}\), and no restart reached
  maximum inner product \(1/2\).
- Exact finite-graph checks on the binary64-defined tight graphs found 14 of
  16 retained graphs nonisomorphic to their source; all 14 have different
  edge counts, so the negative isomorphism decisions need no numerical
  spectral comparison.  Stored isomorphism mappings verify the other two.
- Three \(N=42\) runs returned to the source objective within
  \(1.3\cdot10^{-15}\) but with nonisomorphic 176- or 177-edge tight graphs
  instead of 175 edges.  This is numerical evidence for multiple/flexible
  basins at the same observed objective, not a kissing configuration.
- The best \(N=44\) run recovered the record orbit: after an exact graph
  relabeling its Gram matrix differs from the source by at most
  \(8.44\cdot10^{-15}\).  It supplied no further improvement.
- Added a pinned independent verifier.  It ignores solver-success status,
  recomputes all retained coordinate claims, exact cover optimality, graph
  certificates, and stress residuals, and rejects five targeted corruptions.
  The geometric status remains **NUMERICAL EVIDENCE ONLY**.

## 2026-07-24 00:58 PDT

- Implemented a global topology escape based on the low singular modes of
  the source tight-edge rigidity matrix.  This move deletes no points:
  every point moves coherently along a nonrotational tangent direction.
- Removed all ten infinitesimal rotation directions before choosing 28
  low-singular modes.  Ran RMS geodesic kick amplitudes
  \(0.08,0.16,0.28,0.45\), temporarily penalized the old tight edges for
  900 iterations, then released the penalty exactly to zero for 1,400
  iterations and applied direct minimax polish.
- An independent eigenspace-based tangent calculation reproduced the
  numerical nonrotational rank/nullity pairs at threshold \(10^{-9}\):
  \(130/24,150/8,162/0,166/0\) for \(N=41,42,43,44\).
- Recorded a strong scale separation: the smallest \(N=43\) singular value
  is only \(4.23\cdot10^{-8}\), whereas the smallest \(N=44\) value is
  \(1.986\cdot10^{-2}\).  These remain numerical diagnostics, not exact
  ranks.
- No restart beat its source and none reached \(1/2\).  Nine of sixteen
  retained tight graphs are nonisomorphic to their source, all with
  edge-count witnesses.  Small kicks returned to the original objective
  basin at \(N=41,43,44\); large topology changes were worse.
- Added pinned coordinate, topology, and alternate-rigidity verification.
  Seven regression/tamper tests pass, including a check that optimizer
  success status is not trusted.

## Status

No exact construction.  The X=12 shadow did not produce a new competitive
41-point basin.  Whole-cover reinsertion changed most tight-graph topologies
but found no better objective.  Global rigidity-mode escape likewise found
no improvement and numerically returned small kicks to the known basins.
The numerical \(N=44\) benchmark improved in the first round and is
preserved for subsequent construction searches.
