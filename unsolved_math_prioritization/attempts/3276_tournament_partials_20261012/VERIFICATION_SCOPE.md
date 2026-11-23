# Verification scope and stopping boundary

## Finite tournament lane

The two candidate engines both give zero obstruction-cycle completions at every order from three through eight. Orders one and two are handled directly. The canonical-word / DFS-state / dead-state counts are respectively:

- Order 3: 3 / 0 / 0
- Order 4: 6 / 4 / 4
- Order 5: 9 / 35 / 16
- Order 6: 26 / 1,307 / 495
- Order 7: 53 / 83,761 / 32,160
- Order 8: 146 / 14,944,184 / 5,728,965

Only cyclic vertex rotation and a global color permutation are quotiented. Every chord retains all six oriented-color choices. No all-three-color incidence, interval reachability, or new structural pruning theorem is assumed.

The periodic three-distinct-color word is excluded at lengths three, six and nine. At length six the state/dead counts are 74/26; at length nine, 353,866/106,035. General order nine is unsearched. Periodic length 12 is unsearched. The accepted minimum periodic-counterexample order is at least 12.

The independent audit exhaustively enumerates 46,879 labeled tournaments through order four, and 1,892,511 literal fixed-cycle completions through order five. Its 24 count scopes include satisfying cases with a constraint removed, which reject an always-zero search. The independent BFS harness checks 746,070 insertion proposals in 9,600 partial-state trials, with 581,193 accepted and 164,877 rejected proposals. It checks positive-length diagonal reachability and rejection without state mutation.

Literal symmetry checks cover 29,511 raw words of lengths three through nine; the length-nine orbit count of 369 is not a tournament search. There are 78 transformed hostile fixtures. Six mutated candidate programs, four corrupted raw-result controls, the candidate's eight result mutations and eight invalid command-line scopes, and integrity mutations are rejected within the original audited checks. The author's full replay ran in all three Python modes; the independent auditor separately ran full higher-order replay in normal mode and its behavioral audits in all three modes.

## Structural lane

The author's exact word theorem was checked on all 88,560 labeled words of lengths three through ten, with no symmetry quotient, and sharpness examples through length 101. These are word-level checks, not exhaustive tournament completions. The independent structural recovery audit checks all 29,511 ternary words through length nine and all 43,688 binary words at odd lengths through fifteen. Its through-ten coverage is replay of the inspected author checker. The complete audit records every hostile control and boundary.

The author's incidence-deletion tests cover 111 fixtures, all permitted deletion schedules and exhaustive stable-subset unions. The independent reviewer uses three schedules against exhaustive stable-subset unions in 801 deterministically sampled tournaments of orders one through nine, plus explicit hostile cases. Those fixtures can contain cyclic rainbow triangles; no target claim is inferred from their mere inclusion.

## Edition gate

The preparation gate checks all accepted original byte dependencies, every full reversible source transformation, exact public inventory, scholarly-versus-operational identity classification, concrete illustrative examples, and the complete external preparation seal. The independent edition reviewer must inspect the complete text and transformation boundaries rather than equating hash consistency with mathematical validity.

All preparation checks and hostile controls are required under normal Python, -O and -OO, with explicit exception gates. A correct-byte check is not a fresh search replay. This edition distributes no program, raw output, external source document or formal certificate. The finite result remains computer-assisted; the unrestricted problem remains unsolved.
