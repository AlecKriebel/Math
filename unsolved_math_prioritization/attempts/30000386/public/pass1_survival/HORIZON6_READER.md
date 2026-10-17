# A complete one-dimensional six-round Devil strategy

This is a restricted one-dimensional analogue, not a counterexample to the two-dimensional conjecture. The Angel may move by −1, 0, or 1. Every bomb below explodes at time 6.

After observing the first move a₁, announce the bomb at a₁. Thereafter translate the current Angel position to zero. Reflect the coordinate if needed to make the sorted bomb list lexicographically minimal. Discard bomb positions farther than h from zero when h moves remain, since they cannot be reached in time.

The following table specifies every later response. A response q is a bomb position relative to the new Angel position, in the coordinate orientation used for that row. After announcing it, translate, prune, and reflect again as above to obtain the stated child. No information about future Angel moves is used.

| Moves left h | Current terminal bombs B | Angel move | New bomb q | Child h:B |
|---:|---|---:|---:|---|
| 5 | [0] | -1 | 0 | 4:-1,0 |
| 5 | [0] | 0 | -1 | 4:-1,0 |
| 5 | [0] | 1 | 0 | 4:-1,0 |
| 4 | [-1, 0] | -1 | -1 | 3:-1,0,1 |
| 4 | [-1, 0] | 0 | 1 | 3:-1,0,1 |
| 4 | [-1, 0] | 1 | 1 | 3:-2,-1,1 |
| 3 | [-1, 0, 1] | -1 | -1 | 2:-2,-1,0,1 |
| 3 | [-1, 0, 1] | 0 | 0 | 2:-1,0,1 |
| 3 | [-1, 0, 1] | 1 | 1 | 2:-2,-1,0,1 |
| 2 | [-2, -1, 0, 1] | -1 | 0 | 1:-1,0,1 |
| 2 | [-2, -1, 0, 1] | 0 | 0 | 1:-1,0,1 |
| 2 | [-2, -1, 0, 1] | 1 | 1 | 1:-1,0,1 |
| 2 | [-1, 0, 1] | -1 | -1 | 1:-1,0,1 |
| 2 | [-1, 0, 1] | 0 | 0 | 1:-1,0,1 |
| 2 | [-1, 0, 1] | 1 | 1 | 1:-1,0,1 |
| 3 | [-2, -1, 1] | -1 | 0 | 2:-2,0,1 |
| 3 | [-2, -1, 1] | 0 | 0 | 2:-2,-1,0,1 |
| 3 | [-2, -1, 1] | 1 | 1 | 2:-2,0,1 |
| 2 | [-2, 0, 1] | -1 | 0 | 1:-1,0,1 |
| 2 | [-2, 0, 1] | 0 | -1 | 1:-1,0,1 |
| 2 | [-2, 0, 1] | 1 | 1 | 1:-1,0,1 |

The only terminal row is h=1 with B={−1,0,1}; all three last moves are bombed. Every nonterminal row lists all three Angel choices. The table therefore proves a legal adaptive Devil strategy by finite backward induction. There is one announcement after each of moves 1 through 5, exactly the permitted budget. Repeated bomb positions are allowed.

The JSON certificate and a separate recursive checker reproduce this table. The checker does not call the minimax solver.
