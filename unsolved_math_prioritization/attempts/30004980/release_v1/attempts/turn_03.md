# Attempt 3: Cyclic obstruction to scheduling arbitrary near-twin pairs

Timestamp: 2026-10-03 13:55 UTC. Budget: 3/5. Exact-target completion estimate: 5%.

Tested strengthening: any partition into pairs whose initial disagreement sizes are at most D=floor((n-1)/2) can be ordered so that pair-first contractions stay within D.

This strengthening is false. Let the graph have vertices 0,...,5 and edges

03, 13, 25, 35, 14, 15.

It is a triangle on {1,3,5} with one pendant leaf at each triangle vertex. Choose the pairs P0={0,1}, P1={2,3}, P2={4,5}. Each pair has original disagreement size 2. The pair-update matrix w from Attempt 2 is

[0, +1, -1]
[-1, 0, +1]
[+1, -1, 0].

After any first pair, red degree is 2. For any choice of the second pair, one active pair has red degree 3 and the other 1: the two relevant off-diagonal entries are +1 and -1. Thus all six possible orders of this matching have widths 2,3,2 over their three pair contractions. Scheduling alone cannot repair this matching.

The graph itself has twin-width exactly 2. Its minimum first-pair disagreement is 2, giving the lower bound. For the upper bound use pairs {0,1}, {2,4}, {3,5} in this order, then finish arbitrarily on three parts. Direct quotient checking gives red degree at most 2. The artifact checks/cyclic_pair_obstruction.json records the graph, matrices, all six bad-order profiles, an alternative pair schedule, and an exact dynamic-programming result.

Outcome: an explicit, fully checkable counterexample to a plausible stronger scheduling lemma, not a counterexample to the twin-width conjecture. The obstruction survives having all matched pairs individually optimal first moves. A proof must choose the matching jointly with its order, carry extra slack, or allow more general part sizes. No claim that this elementary obstruction is new to the literature is made.
