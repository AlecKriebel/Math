# 30000991: graph case of persistence-pairing realization

[GRAPH_CASE.md](GRAPH_CASE.md) proves Knudson's Conjecture 3 for every finite graph by a component-postponement construction and an explicit descending integer function. The original question for higher-dimensional simplicial complexes remains unresolved.

- Status: unsolved, 2/5 substantive approaches
- Separate adversarial AI review: passed; see [the report](independent_review/REVIEW.md). The proof retains its original pending-review header for exact snapshot matching
- No novelty claim; adjacent prior problem 30000990 is explicitly distinguished and credited
- Run `python verify.py` here: 8,852 exact assertions on 467 graph filtrations, using only the standard library
- `construct_graph.py` implements the actual graph function construction
- `exploration/` records an earlier, weaker finite order-feasibility diagnostic, not higher-dimensional realizations
