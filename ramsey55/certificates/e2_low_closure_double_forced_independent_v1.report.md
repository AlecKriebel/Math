# Independent audit of the two-forced-edge low-frontier experiment

Evidence category: **REPRODUCIBLE COMPUTATIONAL OBSERVATION**

This is a fail-closed audit of the frozen constructive experiment in
`results/benchmark_plans/e2_low_closure_double_forced_v1.json`. It verifies
the two exact forced-edge schedules and reproduces the later heuristic search
outcome. It is not a Ramsey nonexistence proof.

## Frozen audit

The independent audit protocol was frozen before the retained full audit:

- plan:
  `results/benchmark_plans/e2_double_forced_search_independent_check_v1.json`
- plan SHA-256:
  `67a508dc4c42360f6dc07837ffe2b3f12d6ef82b23ef15e130d2c9fa1b6193b7`
- Python fail-closed orchestrator SHA-256:
  `2e8cddb5971a246d0c3b502c0c687badac3e7abedb20338cf357710be491802d`
- independent C++ schedule checker SHA-256:
  `fd133602a1057e49470e514325af066d951f1aca395a2dcf6b047c71d417b9ec`
- focused-test source SHA-256:
  `1eeb40e11549de68bd699a25d6378e56479470a0582c32ef60ec8e99f7515d62`

Seven focused tests passed both before the plan freeze and after the retained
audit. The checker rejects duplicate JSON keys, hash drift, schedule-count
drift, E1-handling drift, malformed graph6, invalid endpoint geometry, and
aggregate-identity failures.

## Exact schedule reconstruction

The independent schedule implementation shares no code with the production
search. It decoded and exact-recounted all 53 supplied representatives and
independently reconstructed the 22 known labeled neutral cycles:

- 9 representatives have objective 3;
- 44 representatives have objective 4;
- all 22 known E=2 starts generate disjoint 86-state neutral cycles;
- the known labeled-state union therefore has exactly 1,892 states.

It then exhaustively reconstructed the complete first schedule:

- 47,675 eligible first barriers;
- 46,225 outside the seed conflict-edge union;
- 1,450 in the conflict-edge union with post-flip objective greater than 4;
- 47,675 exact post-first-flip recounts;
- every published first-height count matched.

From every once-forced graph, it independently enumerated every edge other
than the first edge and excluded the current conflict-edge union. This was a
full enumeration, not a sample:

- 39,511,631 eligible second candidates;
- every first graph had at least one candidate;
- the minimum-height, lexicographically first candidate was selected for all
  47,675 first graphs;
- 47,675 exact post-second-flip recounts;
- 15,615 selected moves had delta 0;
- 32,060 selected moves had delta +1;
- every published second-height count matched.

The independently derived selected-schedule FNV-1a digest is
`652fb5535ef09756`.

## E1 stop/export semantics

The production plan, result, source, executable, inputs, and output stream
all matched their frozen SHA-256 bindings. Because the source hash is fixed,
the audit also checked its control flow:

- objective 1 stops immediately both inside the rollout loop and after the
  terminal-step recount;
- both sites increment `E1_visits` and return the E1 graph;
- double-forced mode exact-recounts the returned graph to one conflict;
- it writes the graph to the frozen near-construction path and exits 11;
- both forced edges are initially tabu;
- the graph after the final permitted move is exact-recounted.

The recorded run reports zero E1 visits and its frozen E1 output path does not
exist.

## Independent endpoint quotient

All 1,878 retained graph6 records were independently decoded, round-tripped,
and recursively enumerated for K5 and I5:

- all 1,878 are distinct;
- 938 have two K5 conflicts and no I5 conflict;
- 940 have two I5 conflicts and no K5 conflict;
- every conflict pair has the same color and overlaps in four vertices.

The audit used the Traces engine through `shortg -t`, rather than the
dense/sparse `labelg` route used by the endpoint audit. It explicitly supplied
every endpoint, every complement, all 22 known inputs, both published V2
representatives, and all of their complements. It independently recovered:

- four ordinary isomorphism classes;
- two complement-isomorphism classes;
- labeled complement-class sizes 930 and 948;
- both classes represented in the supplied 22-seed corpus;
- zero novel labeled endpoints and zero novel complement classes;
- exact one-for-one coverage by the two published V2 representatives.

The endpoint complement-partition SHA-256 is
`22f54e5a5c7d16d7b77f47b9a5f56cc5bac52385106db0cc6a7b151d48e834b5`.

The V1 audit plan/result were preserved byte-for-byte. Its plan continues to
record the historical inherited-prose defect and metadata-only amendment.
The separately named V2 plan/result were also preserved and contain the
correct 1,878/22 corpus sizes. The V1 and V2 representative streams are
byte-identical. No audit generation was overwritten by this check.

## Deterministic frozen-binary replay

Finally, the SHA-bound production executable was rerun with all frozen
inputs and parameters in a temporary directory:

- exit code: 0;
- every non-runtime result field matched;
- E1 visits: 0;
- E1 output created: no;
- E0 found: no;
- reproduced E2 lines: 1,878;
- reproduced E2 SHA-256:
  `ad48e7eb76403abc050bd6200003720ff781840116c6c6651414cbc27b90b646`;
- reproduced and frozen E2 streams: byte-identical.

This replay provides direct evidence that the retained result did not merely
omit a reached E1 state from its JSON: under the frozen executable and
parameters, the run again reached neither E1 nor E0 and left no E1 artifact.

## Result and boundary

The retained independent audit is:

- `results/verification/e2_double_forced_search_independent_v1.json`
- SHA-256:
  `38bebb3adf501ab4df75b3fd16777f018535e47e8170c70be341f4a5d2c5cb3d`
- status:
  `VALID_EXACT_FORCED_SCHEDULE_AND_REPRODUCIBLE_HEURISTIC_OUTCOME`

The 47,675 first choices and 39,511,631 eligible second choices are exact
finite enumerations only relative to the 53 supplied representatives and the
frozen edge rules. The subsequent 256-step tabu repairs are heuristic.
Reproducing zero E0/E1 outcomes proves no global nonexistence statement and
does not change the bound
\[
43 \le R(5,5) \le 46.
\]
