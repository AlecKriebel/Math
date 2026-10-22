# A single adaptive schedule rules out sub-square-root deviations from linear motion

This is a restricted-path obstruction under the same two-dimensional Time-Bomb contract. It is not a Devil win against an unrestricted Angel.

## Explicit strategy

For each integer j≥1 define

    n_j = 4^j,
    R_j = 2^(j−1)−1,
    K_j = (2R_j+1)² = (2^j−1)².

After observing the Angel's move a_(n_j), the Devil lists every integer cell in

    2a_(n_j) + {−R_j,…,R_j}².

There are K_j such cells. In rounds n_j through n_j+K_j−1, it announces one listed cell per round, every time with detonation time 2n_j. All other rounds receive irrelevant current/past-time announcements.

This is legal. One has K_j≤n_j, so every listed bomb is announced by round 2n_j−1. The next stage starts at n_(j+1)=4n_j>2n_j; hence no two stages demand the same announcement round. At the start of a stage its entire target list is determined by the position just observed. No future Angel move is used.

## Exact consequence for every surviving play

If the Angel survives through move 2n_j, then

    ||a_(2n_j)−2a_(n_j)||_∞ > R_j.

Otherwise that endpoint is one of the cells announced during stage j and the move is lethal. In particular every infinite surviving play must satisfy this inequality for every j≥1.

## Corollary: no sub-square-root deviation from a line

The same single Devil strategy defeats every legal path for which there exists a vector v in R² such that

    a_n = n v + o(sqrt(n))

in maximum-coordinate norm as n tends to infinity. The vector need not be known to the Devil, need not be selected before play, and the path can otherwise respond adaptively to the bombs.

Indeed, writing e_n=a_n−nv gives

    a_(2n_j)−2a_(n_j) = e_(2n_j)−2e_(n_j) = o(sqrt(n_j)).

But R_j/sqrt(n_j)=1/2−2^(−j) tends to 1/2, contradicting the exact inequality above for all sufficiently large j. Therefore that path must be killed at some finite stage.

This includes every path staying within a finite bounded distance of any constant-velocity line. No common deviation bound is required: a single prescribed sequence of stages handles all finite bounds. It also includes paths with an arbitrary fixed spatial intercept, since such an intercept is o(sqrt(n)).

## Quantitative corollary

For every infinite surviving play and every vector v in R²,

    limsup_(n→∞) ||a_n−nv||_∞ / sqrt(n) ≥ 1/[2(2+sqrt(2))].

To see this, suppose the limsup is L smaller than the displayed constant. For every sufficiently small positive ε and all sufficiently large n, the normalized error is at most L+ε. Then

    ||a_(2n_j)−2a_(n_j)||_∞ / sqrt(n_j)
        ≤ (sqrt(2)+2)(L+ε) < 1/2,

with a fixed gap from 1/2. This contradicts the exact lower bound R_j/sqrt(n_j)→1/2. The constant is approximately 0.1464466094.

## Scope warning

A legal Angel can respond to these announcements by changing direction enough to violate the displayed approximation to a line. Nothing here prevents that. The result gives a necessary fluctuation property for a surviving play against this specific Devil; it does not establish that such fluctuations are impossible.
