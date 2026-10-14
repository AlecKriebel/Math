# Independent second audit of the nonlinear two-move terminal results

Scope: mathematical audit within shared PASS3. No new construction pass and no full-game conclusion.

Audited files:

- `../pass3_invariant/TWO_MOVE_DEFICIT_RESERVE.md`, SHA256 `853a0f8b7e8ab9ea9179c6177e1a496c8d26397f7b383fd3d024559fbdcef2ea`.
- `../pass3_invariant/FIVE_HALVES_TERMINAL_CAPACITY.md`, SHA256 `1642e3f1286e5df69403eba81121399fb184fbeda0b4c65c4e3bd919252ae8c2`.

## Result

No mathematical defect found. Both results are valid for the stated terminal-only weighted game. Neither result protects intermediate lethal times or asserts an unrestricted Time-Bomb strategy.

## Checks

1. The four side-three neighborhoods centered at the four diagonal king neighbors cover the entire side-five reachable square. Summing their nonnegative deficits gives at least the full-square deficit. A total greater than four times the update budget therefore gives one neighborhood whose deficit exceeds that budget.
2. The first move reaches the selected center legally. An adaptive update cannot fill all its deficits, and the final move is chosen only after observing that update. Strictness is preserved.
3. In the fractional sharpness example, every legal side-three successor neighborhood contains exactly four sites with both coordinates nonzero. Their total deficit is exactly beta. Values remain nonnegative for the stated range zero through four.
4. The unit point-bomb example with all twenty-five positions except the four corners preloaded has twenty-one bombs. Every legal first center sees at most one remaining unbombed neighbor. Reserving a boundary fill of an additional omitted noncorner gives the stated twenty-bomb pre-boundary example. These are correctly scoped as arbitrary preloaded local states, not forced histories from the empty board.
5. The side-five endpoint recursion has four disjoint children, cardinality twenty-five times four to the k, and radius three times two to the k minus one. The legal traversal length three times two to the k-minus-one leaves precisely the child's remaining-time budget.
6. The maximal initial wait is three times the dyadic scale minus one. The traversal sum is six twenty-fifths times one minus the reciprocal scale, multiplied by the update budget.
7. The final two-move reserve contributes four twenty-fifths of the update budget. Combining it with the wait and traversal charges yields the stated coefficient two-fifths minus three over twenty-five times the scale minus one over twenty-five times its square. Its product with five-halves is strictly below one.
8. All waiting and block updates end at time T-minus-two. The sole update in the terminal primitive occurs after move T-minus-one, and no update after the terminal move is used retroactively.

The results are accepted within these explicit restrictions. No novelty claim is supplied.
