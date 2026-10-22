# Independent adversarial audit of the concentration-profile repair

## Accepted artifacts

- `pass2_invariant/CONCENTRATION_PROFILE_LEMMA.md`
  SHA-256 `f06ef58652911b266679144bba9f853dcdd6892042707c0f0937823621a8cea6`
- `pass2_invariant/THREE_DEADLINES_13_17_21.md`
  SHA-256 `1c4d6f28e989bff3739e328e5bf15525172edf9ddc228dbaa104d6c0b5674b96`

Outcome: accepted under the exact Time-Bomb contract. No required correction was identified. These are restricted-deadline results, not a solution of the unrestricted game.

## Checks

1. **Traversal/update count.** With side L and wait w, the nested-square traversal lengths sum to (L−3)/2, so the number of charged updates is w+(L−3)/2=r−1. The last Angel move sees the announcement from the previous round and no later one. No update after the terminal move is incorrectly charged or observed.
2. **Concentration bound.** For any chosen side-q square, any allowed translated kernel adds average at most c(q). The chosen square can depend on earlier announcements; the concentration supremum is over all translates and therefore remains valid under adaptive choices. The least-average-child choice does not increase the inherited average.
3. **Boundary announcement.** The profile reduction reserves L²c(L) for the announcement immediately after the earlier terminal move. Its denominator D=L²[1−A_r(c)−c(L)] is sufficient because the preboundary local mass is strictly below D. The downstream terminal value stays strictly below one.
4. **Real rather than integer hazards.** The middle phase uses real g-mass. It needs a strict inequality, not an integrality step. The time-21 final phase can use the integer bomb-count refinement, as written.
5. **Kernel update accounting.** A new time-13 bomb increases f by a translate of delta; a new time-17 bomb by U/D_2; a new time-21 bomb by (U*U)/2025. Duplicates have smaller increments. All coefficients are nonnegative.
6. **Arithmetic.** With |Q|=81, beta=81/53 and D_2=81−28beta=2025/53, the three mass/peak pairs are (1,1), (53/25,53/2025), and (81/25,1/25). The convolution peak is 81/2025 because an overlap of two side-nine squares contains at most 81 cells.
7. **First phase.** At time 13, L=27 and w=0. The side-nine contribution is at most 9/25 and the side-three contribution at most 1/3. Their sum is 52/75<1.
8. **Middle phase.** The boundary announcement contributes at most beta to local g-mass; the three traversal rounds add average at most beta/3. The final bound is strictly below (D_2+beta)/81+beta/3=1.
9. **Last phase.** If g(a_17)<1, the preboundary count of time-21 targets in its side-nine square is at most 52. The round-17 announcement makes it at most 53, strictly below C=54. The robust terminal lemma applies.
10. **Intermediate safety and quantifiers.** No lethal allowed time lies strictly inside a phase. All chosen regions and moves depend only on already observed announcements. The argument covers arbitrary adaptive Devil choices at the three allowed timestamps; it never uses a completed future schedule.

## What the audit does not establish

The same recurrence need not succeed for arbitrary finite deadline sets. Its local terminal moves cannot be used across unprotected intervening deadlines. The old estimate's failure at {13,17,21} was not a losing instance; this accepted repair now gives an actual online winning strategy for that set.
