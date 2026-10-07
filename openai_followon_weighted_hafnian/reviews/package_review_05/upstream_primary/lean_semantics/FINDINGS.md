# Independent pinned Lean source findings

Pin: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Source-only findings; no kernel build performed.

Actual base FPRAS interface: `OAI.MatchingFPRAS.thm_main : MainStatement` in `lean/OAI/Combinatorics/MatchingCount/Main.lean`. The model is in its sibling `Model.lean`. `PerfectMatching/Main.lean` is an entropy theorem source.

At the interface, `GraphInput` represents finite simple undirected graphs by a finite set of increasing ordered pairs; `Perfect` is the standard exactly-one-incident selected-edge predicate; `Z` is the card of a powerset filter, including the empty graph. `MainStatement` quantifies a single fixed finite-table randomized tape machine and a fixed polynomial time bound, valid for every graph and positive rational epsilon < 1, delta < 1/2; requires all tapes halt with nonnegative rational output, exact zero on zero graphs, and fair finite-tape success fraction >= 1-delta. This interface accurately encodes a semantic unweighted FPRAS. Implementation dependency review remains in progress.
