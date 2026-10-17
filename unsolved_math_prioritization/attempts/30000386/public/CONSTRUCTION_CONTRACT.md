# Public game rules version 1

This is a newly authored public restatement dated 14 October 2026. It is the
package-root rules reference for proofs that mention `CONSTRUCTION_CONTRACT.md`.
It is not a byte-preserved copy of their historical research contract.

Some preserved proofs record the historical contract SHA-256
`1be42b4f13460a91a71948fc532c135b7453f56811566ed5c3f918f8976c5c4c`.
That hash identifies the earlier document and does **not** authenticate this
replacement. The current public document has its own identity in
[MANIFEST.json](MANIFEST.json). The independent
[source and acceptance contract](TIME_BOMB_ACCEPTANCE_CONTRACT.md) supplies
the source-based normalization.

## Exact game

The initial Angel position is a_0=(0,0), at time zero, with no announcements.
In round n>=1 the Angel first selects a_n in Z^2 with
||a_n-a_(n-1)||_infinity<=1. The nine moves include diagonals and staying.
This move loses exactly if some earlier round r<n announced the pair (a_n,n).
If play survives, the Devil observes that move and announces one pair (p_n,t_n),
where p_n is an arbitrary lattice site and t_n is a positive integer.

The announcement may depend on the complete observed history. Sites, target
times, and identical pairs may repeat. A current or past target time has no
retroactive effect. Several earlier announcements can target different sites
at the same future time. The budget is one announcement after each surviving
move, with no stored credits or batch announcements.

An effective announcement made after round r has lead t-r>=1. A maximum-lead-H
restriction bounds this number by H; it is an additional restriction, not a
rule of the full game.

## Full target and acceptance

An affirmative resolution needs one nonanticipating Angel strategy that
survives every round against every legal adaptive Devil. A negative resolution
needs a legal adaptive Devil strategy forcing a finite loss against every
Angel strategy. Neither statement is established in this package.

An offline path selected after the whole schedule, a theorem for restricted
timestamps or leads, a defeat of one policy class, a legally realizable losing
preload, and finitely many successful tests do not by themselves resolve the
target. Finite-horizon online wins for every horizon do suffice when combined
with the proved finite-Angel-action extraction.

Proofs must preserve every intermediate lethal-time test, the announcement
following each boundary move, the two spatial coordinates, speed one, and the
empty initial state. No effective computability or uniform memory bound is
part of the existence target.
