# Source log (retrieved in this session, 2026-09-13 US Pacific)

1. Erich Friedman, Problem of the Month, February 2007.
   https://erich-friedman.github.io/mathmagic/0207.html
   Text specifies each A attacks exactly n B's and no A's, and each B exactly m A's and no B's.
   Knights and Rooks table: column N=4, row R=2 is '?'.
   Source example N1R1.gif independently retrieved with GitHub.fetch_file;
   blob SHA c5a73fb1608603107683f8c176b06111a08b2771 reproduced from bytes.
   Image inspected: 4 columns, 2 rows; top . . K R, bottom R K . . .
   N1R1 coordinates and direct-check report are included.
2. https://puzzling.stackexchange.com/questions/128060/where-should-the-chess-pieces-be-placed-in-4x4-6x6-and-9x9-chessboards
   Question dated 2024-08-26, last edit 2025-05-29. Its Puzzle 2 is N=4,R=1, NOT the target.
   A comment correctly warns that ratios inferred from reciprocal attacks need not apply.
3. https://erich-friedman.github.io/puzzle/chessattack/
   Nearby published puzzles include N=2,R=3, not the target.
4. Initial queries: 'Friedman knights rooks four two February 2007 math magic';
   '"knights and rooks" "four" "two"'; '"mathmagic/0207.html" knights';
   '"Friedman" "knights" "rooks" "attacks"';
   '"knights" "rooks" "each" "four" "exactly two"'.
   No exact-target later solution found. Search non-discovery is not a proof of open status.

Operational notes: direct container requests and pip failed due unavailable DNS.
Web tool could not render the source GIF (unsupported content-type). GitHub base64
read succeeded; decoded bytes' git hash was checked and the image rendered locally.

## Second illustrated source calibration

N4R1.gif was retrieved using GitHub.fetch_file at
https://github.com/erich-friedman/erich-friedman.github.io/blob/master/mathmagic/0207/N4R1.gif
Its blob SHA 34035bef1f04e6e53fed5371998111e70ad0422a was reproduced from the
2940 decoded bytes. The 6x6 image was visually inspected: two knights at
(2,3),(3,2) and eight rooks listed in data/source_N4R1.json. Both independent
checkers confirm knight outdegree 4 and rook outdegree 1. It is not a target
N4R2 solution. The solver independently recovered this exact placement.

## Final source/status recheck, after the boundary proof was found

The primary page was opened again; its target cell remains '?'. Queries:
- '"knight" "four rooks" "two knights"'
- '"knights and rooks" "impossible"'
- '"knights" "rooks" "rightmost"'
- '"N4R2" "chess"'

No earlier proof or counterexample for the exact target was located. Results
about legal chess moves, FEN strings, and solo-chess complexity were not
solutions to the stated placement problem. Neither these searches nor the
archival question mark establish historical priority. No contact or
publication was made. The mathematical conclusion rests on the supplied
proof, not on a claim that the problem remained open.

A final delivery-stage recheck reopened the primary source and the later
Puzzling post and repeated searches for '"knights" "four rooks" "two knights"',
'"Friedman" "knights" "rooks" "impossible"', and '"N4R2" chess'.
The target cell and the limited historical-status conclusion were unchanged.
