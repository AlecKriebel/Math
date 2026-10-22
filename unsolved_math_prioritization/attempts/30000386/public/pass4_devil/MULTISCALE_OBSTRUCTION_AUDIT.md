# Independent audit of the multiscale obstruction

Accepted artifact: `pass4_multiscale/REPORT.md`, SHA256
`52044362abf69c83eb23e51061ec0951d35de7bca8e4d4ec9b0af5fa98772d89`.

This audit accepts Sections 2–4 and 6. Sections 1 and 5 have separate independent review by the main audit lane.

## Tracking radius

The common-time carpet uses exactly Q=(2R+1)^2 announcement rounds, targets Q+1, and has maximal lead Q. Thus a controller claiming uniform distance R from a stationary reference against all streams of lead at most H must have Q>H. The statement is a tracker obstruction; an unrestricted Angel may leave the carpet.

## Equal-block certificate

The revised statement explicitly uses announcement rounds [S_j,S_j+L) and reference moves (S_j,S_j+L]. Therefore the earliest announcement can have a target strictly before the following block endpoint with lead 2L−1. If a bootstrap seeks a new lead bound J>H, covering its entire short class requires H≥min(J,2L−1), hence H≥2L−1 and J≥2L. The latter inequality also makes all L proposed long announcements with target S_j+2L legal.

Consequently Q≥2L. With M≤L/4 and L≥2, (2M+1)^2≤L^2, and the proposed union certificate is at least min(L,2), hence cannot be below one. For L=1 the integer displacement radius is zero and the certificate equals one. The argument concerns the numerical upper-bound certificate only. It does not convert that upper bound into an actual loss probability or rule out more precise history-dependent certificates.

The earlier version left the announcement-block timing implicit. The accepted revision resolves that ambiguity by stating the half-open convention and distinguishes the primitive lead bound H from the proposed larger bound J.

## Time dilation

Spreading an arbitrary virtual diagonal king step over K physical rounds requires K v≥sqrt(2) under a Euclidean speed-v constraint. The K physical rounds retain K announcement opportunities; a shared class budget can redistribute them but cannot change their total to one. Interior physical targets also remain legal lethal events. No invalid reduction to a one-announcement macro-game is made.

## Two-class preload

The sixteen displayed announcements have respective leads 17 through 10 and 8 through one. Their target times exceed every setup move, so the specified stay-put history is legal. At move 17 the current batch forces the origin; at move 18 the next batch plus the intervening origin announcement fills its neighborhood. Each class alone fails to provide the common admissible move needed by the combined guard. The report correctly identifies existential reachability under a cooperating path, rather than strategic forceability from the empty board.

No required corrections remain in the accepted revision. No arbitrary-H or unrestricted winning or losing theorem follows from these certificate obstructions.
