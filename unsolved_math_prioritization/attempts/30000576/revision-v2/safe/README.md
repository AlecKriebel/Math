# Rank 658: literature attribution with a scalar-field bridge

Problem 30000576 / OWR-1323-013. Revision 2, 4 October 2026.

The first audit correctly held the original attribution-only packet because
the inspected sources did not explicitly identify the scalar field of the
no-chaotic-time-map example. That packet and its audit remain unchanged.

PROOF.md now proves a general bridge: every chaotic real C0-semigroup on a
separable Banach space has a chaotic complexification, and a nonchaotic
individual time map stays nonchaotic after complexification. It explicitly
establishes dense tuples sharing a common real period, diagonal
hypercyclicity, the complex Banach structure, strong continuity, and
descent of discrete chaos by real-part projection.

Thus either possible scalar field in the published example leads to the
complex-space target. The negative resolution remains attributed to
Bayart–Bermúdez, [*Semigroups of chaotic operators* (2009)](https://doi.org/10.1112/blms/bdp055).
Its full counterexample proof remains unavailable. This is a published-result
application plus a proved scope bridge, not a new counterexample or an
independent audit of that paper.

The exact target retains both questions: does every positive-time map have
to be chaotic, and must at least one positive-time map be chaotic? A semigroup
with no chaotic positive-time map answers both negatively.

Proposed status: prior-literature `already_solved`, subject to fresh
independent review of the new bridge and its binding to the cited result.
One substantive mathematical approach was completed; the complete bridge
is an early-stop candidate. No five-approach completion is claimed.

Run `python3 tests/verify_bridge.py` for exact finite algebra controls and
`python3 tests/verify_packet.py` for file and scope integrity. Finite checks
do not prove the infinite-dimensional theorem; PROOF.md is the proof.
