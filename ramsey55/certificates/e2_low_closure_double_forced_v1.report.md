# Two-forced-edge low-frontier experiment

Evidence category: **REPRODUCIBLE COMPUTATIONAL OBSERVATION**

This experiment is a constructive search, not a nonexistence proof. It
changes the previously exhausted one-forced-edge move architecture by forcing
a second edge that belongs to no current forbidden five-set before allowing
conflict-directed tabu repair.

## Frozen inputs and implementation

The production protocol was frozen in
`results/benchmark_plans/e2_low_closure_double_forced_v1.json` before the
search. Its SHA-256 is
`07a8f8a238775bbe70621c221446e250ba4852973f167d0313990b8784dbbb54`.

The 53 starts are the 9 `E=3` and 44 `E=4` representatives of the previously
audited 89,870-state low frontier. The search also loads all 22 known `E=2`
near misses, whose exact neutral cycles contain 1,892 labeled states.

Production source and executable SHA-256:

- `src/search43_e2_barrier_escape.cpp`:
  `18079f5b3f1a0018cd0d47ac7965091401aa9a9a9c59dcd492c26ec4d327dcca`
- `build/search43_e2_barrier_escape`:
  `578fd32bc5312b844e411789660e64eca05ea207cd2df8a1698bf2cfaa0d2214`

The source compiled without warnings under C++20 production flags. Its
dynamic check passed all 903 edge deltas on the base graph and 200 successive
random-flip delta checks. A separate ASan/UBSan smoke test passed.

The rollout now stops and exports an exact `E=1` graph. It also exact-recounts
the terminal graph after the last permitted move, so an `E=0`, `E=1`, or
new `E=2` state reached on the final move cannot be silently discarded.

## Exact forced schedules

The first schedule reproduced the prior complete 47,675-case schedule:

- 46,225 edges outside the seed conflict-edge union;
- 1,450 conflict-union edges whose exact post-flip objective exceeds four;
- 47,675/47,675 exact first-flip recounts passed;
- first heights range from 4 through 47, so ceiling 80 excludes none.

Across the once-forced graphs there are 39,511,631 eligible second edges.
An eligible second edge is neither the first edge nor an edge of any current
forbidden five-set. It therefore cannot remove a current conflict. For each
first graph, the run selected the lowest exact post-flip objective, breaking
ties lexicographically:

- every first graph had at least one eligible second edge;
- 47,675/47,675 exact second-flip recounts passed;
- 15,615 selected second moves were objective-neutral;
- 32,060 selected second moves worsened the objective by one;
- both forced edges were initially tabu during repair.

These schedule statements are exact finite enumerations. The subsequent
repair trajectory is heuristic.

An independently written C++ verifier sharing no production search code
reconstructed all 53 starts, the 22 neutral-cycle seeds, all 47,675 first
decisions, all 39,511,631 second candidates, and every selected twice-forced
graph. It reproduced every histogram and emitted schedule digest
`652fb5535ef09756`. Result SHA-256:
`3bd61319d912193b9efb18683653d66517560ceafa695ed791bca55f6c04007e`.

## Production outcome

The frozen run used random seed 20261322, one 256-step rollout per selected
second edge, tabu tenure 11, noise 90,000 per million choices, and objective
ceiling 80.

It executed:

- 47,675 rollouts;
- 2,720,135 repair steps;
- 2,767,810 exact objective recounts;
- 6,390,028 ceiling rejections;
- 147.696827 internal seconds.

There were zero `E=1` visits and zero `E=0` constructions. The run retained
1,878 distinct labeled `E=2` endpoints. Result and endpoint-stream SHA-256:

- `results/constructive/e2_low_closure_v2/double_forced.result.json`:
  `68a95613c09406cea836523f43ee39aa3345edf1023b883e20016b259e160071`
- `results/constructive/e2_low_closure_v2/double_forced_new_E2.g6`:
  `ad48e7eb76403abc050bd6200003720ff781840116c6c6651414cbc27b90b646`

## Independent endpoint audit

The endpoint classification was separately frozen, then run through the
existing independent recursive-bitset and nauty audit:

- all 1,878 graphs recount to exactly two forbidden five-sets;
- every pair has one color and four common vertices;
- dense and sparse nauty partitions agree for graphs and complements;
- the endpoints form four ordinary isomorphism classes;
- modulo complementation they form exactly two classes, of labeled sizes
  930 and 948;
- both classes occur in the supplied 22-near-miss corpus;
- novel labeled endpoints and novel complement classes are both zero.

Superseding v2 audit-plan and valid-result SHA-256:

- `results/benchmark_plans/e2_double_forced_discovery_audit_v2.json`:
  `a9948365b9938ce36ec40d8b168bc8fc2f53e05d26b6d5140964b8939fd6a348`
- `results/verification/e2_double_forced_discovery_audit_v2.json`:
  `6b853b060f8a8b603af62bc86036475258cd448b183e57e39bcfda37cbe8e9f7`

The v1 audit output revealed that only its prose claim boundary still
contained the prior run's hard-coded count 1,670. V2 explicitly supersedes
that presentation-bugged artifact: corpus sizes are derived from the audited
inputs, a focused regression test was added, and the complete classification
was rerun into distinct v2 outputs. V1 remains preserved. No graph-checking,
canonicalization, partition, or novelty logic changed.

## Interpretation and claim boundary

Forcing one non-repairing edge and forcing two non-repairing/out-of-closure
edges both return only to the same two known `E=2` complement classes under
their frozen repair trajectories. This is evidence that the basin is robust
to this edge-local move family.

It is not a global classification of low-conflict graphs. It does not prove
that a \((5,5;43)\)-graph does not exist, and it does not change
\(43\le R(5,5)\le46\). The next constructive experiment must change the
operator at vertex/block scale rather than merely increasing this rollout
budget.
