# Structural review of one-point staircase rerooting

Shared PASS3, 14 October 2026. Reviewed `pass3_concentration_audit/REROOTING_ONE_POINT_BOUND.md`, 10256 bytes, SHA-256 `41336ca4027b4c0c40928e3df4df0e70ec107043d78f64f799d404017c8870b5`.

## Verdict

**Accepted for the exact one-point rerooting map and both finite counting inequalities.** In the notation of the proof, the number of marked pairs with i >= 2, c_i >= m and c_(i-1) <= p_0 <= n/2 is bounded by

`(n+1) binom(n,p_0) B_(n+1)(m)`.

For fixed original cell sizes a,b, the corresponding count is bounded by

`(n+1) binom(a+b,b) B_(n+1)(a)`.

The independent concentration review owns the first-cell input and analytic corollaries. My review finds the geometric and counting hypotheses those corollaries need are established. The result still requires the predecessor-size restriction; it is not an unconditional largest-cell estimate.

## Inflation and incoming-edge lift

Inflating the first entry of a 213 avoider by 12 preserves avoidance. An occurrence using at most one twin collapses to an old occurrence. Both twins cannot form the first two entries of 213 because they increase, cannot form the last two because nothing in the state precedes them, and cannot form its first and last entries because they are adjacent in position.

Anti-diagonal reflection converts this first-entry inflation into inflation of the maximum of the lower state S(A). The two lower twins are consecutive in position and value in the incoming two-cell shuffle. A new cross-cell 1324 would require lower–upper–lower–upper order, impossible using both adjacent twins. An occurrence using only one twin was already excluded. The cell classes remain correct, and the new lower maximum lies in the same upper gap as the old maximum, preserving the forward witness.

The lift is injective. Its inverse identifies the top two consecutive lower values and removes the specified twin. This argument is about the encoded incoming edge; it does not require these twins to remain globally adjacent after the entire rotated staircase is reconstructed.

## Deterministic bridge

For a target lower state B=S(A), write B=L,M,R around its maximum. Av(132) implies every value in L exceeds every value in R. Given any ascent in the upper state U, put the entire block L,M in its gap and put R after all upper entries.

An increasing lower pair cannot cross from L,M to R. Inside L,M no upper point lies between the pair; inside R no upper point follows it. Hence no lower–upper–lower–upper occurrence is possible. The maximum M is bracketed by the chosen upper ascent, so the edge is greedy. The rule remains valid when L or R is empty. The first two entries of the inflated terminal state supply a fixed ascent, making the bridge choice deterministic.

## Rotation, parity, and recovery

Cut the incoming edge of the marked noninitial state, inflate the original final state, rotate the normalized path, and insert the deterministic bridge back to the original first state. All retained edges are unchanged except the injective lift into the old final state, if that edge was not cut. The case i=r needs no incoming lift.

Because the exact kernel is homogeneous in normalized states, rotating them causes no additional parity restriction or transpose. The exact canonical transfer theorem gives one valid full-class avoider of size n+1. Its first cell is at least the size of the marked original cell, including the extra point when i=r.

Given an output and a proposed bridge edge index, the state immediately before that edge is the old final state after inflation. Deflating its first-entry block and undoing the incoming lift, when present, determines every old state and retained edge shuffle. Rotating back from the state after the bridge fixes the original marked index as well. The only unknown is the old cut shuffle. Invalid proposed bridge indices may be rejected and do not enlarge the fiber bound.

There are at most n+1 bridge choices. A cut edge between original states of sizes a,b has at most binom(a+b,b) interleavings. This proves the exact-size bound without any extra factor for internal patterns, cell boundaries, or point allocations. For b <= p_0 <= n/2, monotonicity gives `binom(a+b,b) <= binom(n,b) <= binom(n,p_0)`, proving the threshold version. Multiple marked indices of one input are included in the same fiber argument.

## Diagnostics and remaining scope

The independent script `check_rotation_local_maps.py` checks all 625 first-entry state inflations through size seven, 510 deterministic bridge constructions of total size at most seven, and every one of the 2533 greedy incoming shuffles of total size at most seven. It verifies state formulas, avoidance, witnesses, and inverse recovery. All checks pass; `ROTATION_LOCAL_MAP_CHECKS.json` records them. The global all-size inverse argument, rather than these finite tests, establishes the counting inequalities.

The older three-point connector construction is superseded and receives no new acceptance pin here. A large cell can still have predecessors of successively smaller macroscopic sizes with finite total mass. The one-point encoding does not eliminate that possibility.
