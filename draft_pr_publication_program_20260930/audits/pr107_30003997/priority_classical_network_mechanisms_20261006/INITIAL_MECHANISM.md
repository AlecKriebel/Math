# Independent initial mechanism comparison

Timestamp: 2026-10-06 04:19 UTC. Prepared before reading any other priority-audit family. Completion estimate for this priority audit: 5%.

## Exact target and success test

One fixed-root directed spanning out-arborescence T must serve every destination v. The objective is sum_v sum_{e in P_T(r,v)} c^v_e, with an arbitrary explicitly encoded destination-by-arc cost table. The repaired candidate proves NP-completeness of threshold zero with binary costs on a root-reachable simple four-consecutive-layer DAG of depth three and nonroot indegree at most three. It also proves the {1,2} version by a constant total-depth offset, and an exact minimum-unsatisfied-clauses identity. This audit assumes neither priority nor novelty from those correctness claims.

## Distinct classical mechanism families to test

1. Communication/requirement/routing spanning trees: classical pair demands and common edge lengths produce sum_{u,v} q_{uv} d_T(u,v). With demands supported only on a fixed root this becomes a polynomial shortest-path-tree problem for nonnegative common lengths. Arbitrary c^v_e is strictly more flexible. A prior theorem must supply genuinely commodity-specific edge costs or an exact construction transferring its hardness; word similarity is insufficient.
2. Confluent single-sink multicommodity routing: reversing every arc turns a rooted out-arborescence into routes that merge and cannot split. Each terminal sends one unit with a commodity-specific arc price. This is the most promising exact model equivalence, provided prior hardness includes arbitrary commodity prices and a spanning, uncapacitated setting. Ordinary confluent flow with a common scalar price is polynomial without capacities and does not imply this claim.
3. Simultaneous/constrained shortest-path trees: at zero threshold with nonnegative costs, each destination requires its root path to use a destination-specific allowed edge set. Feasibility means selecting one arborescence consistent with all those sets. A theorem about simultaneous paths is relevant only if paths share parents after merging, not merely independently chosen paths or merely disjoint paths.
4. Hierarchical/network labeling or consistent path selection: candidate variable-parent choices create global labels read by terminal paths. Prior hierarchy hardness could subsume this if node labels and terminal-specific permitted ancestry are represented without stronger constraints or cost transformations.
5. Multiobjective arborescences: multiple scalar arc objectives ordinarily evaluate every selected arc in every objective, whereas this target evaluates only the root-to-that-objective's-destination path. A direct corollary needs destination-specific incidence/path gating. Minimax and budget constraints alone do not establish the sum objective.

## Initial risk assessment

The SAT consistency gadget is standard enough that its shape does not itself justify discovery language. The confluent-flow and simultaneous allowed-path formulations may expose an exact earlier theorem. Depth-three binary restrictions may remain a new strengthening even if broad hardness is prior, but this must be checked against full reductions. No earlier theorem is currently established. No proof search is being added; the assigned work is source/priority verification.
