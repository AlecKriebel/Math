# Exact finite-grid attempt 3: completing the isolated boundary

Date: 2026-10-20. This is a genuine improvement of the finite lower target, not a proof of the general maximum.

## Exact isolated points

For N≥2, x∈[N]^d is isolated from all internal sum relations if and only if min_i x_i=1 and max_i x_i=N. Sufficiency: a coordinate N prevents x being a summand; a coordinate 1 prevents x being a sum. Necessity: if max_i x_i≤N−1, then x+1⃗ lies in the grid, so x occurs as a summand. If min_i x_i≥2, then x=1⃗+(x−1⃗), so x occurs as a target. Repeated summands are permitted in both arguments.

Their number is I_d(N)=N^d−2(N−1)^d+(N−2)^d, by inclusion-exclusion. Every maximum sum-free set contains all isolated points, since adding one creates no forbidden relation.

## Exact improved lower formula

Let H_{d,n}(s) be the cumulative positive-grid rank count from attempt 1, with H_{d,0}(s)=0. The cumulative count of isolated points is

J(s)=H_{d,N}(s)−H_{d,N−1}(s)−H_{d,N−1}(s−d)+H_{d,N−2}(s−d).

This follows by excluding points with no coordinate N and points with no coordinate 1, accounting for the translation of the latter cube. It is a counting identity, not a translation of sum-freeness.

Completing a slice S_t by all isolated vertices gives the rigorous bound

f_d(N)≥max_t [H_{d,N}(2t−1)−H_{d,N}(t−1)+I_d(N)−J(2t−1)+J(t−1)].

All entries are explicit finite binomial sums. `isolated_completion.py` calculates them using integers only.

## A dimension-three counterexample

For [11]^3, every ordinary coordinate-sum slice has at most 991 points. The slice with 14≤x+y+z≤27 has 989 points. Add the three permutations of (11,1,1). They have sum 13 and are isolated, so the result has 992 points and is sum-free.

Thus exact plain-slice extremality fails already in dimension 3, not only in dimension 6. This is a lower-bound counterexample, not an exact evaluation of f_3(11).

Other exact comparisons (plain slice maximum; isolated-completed lower bound):

- [5]^4: 540; 544.
- [4]^5: 947; 952.
- [3]^6: 700; 706 (the latter was separately proved optimal in attempt 2).
- [15]^3: 2475; 2478.
- [20]^3: 5780; 5786.
- [30]^3: 19257; 19272.
- [50]^3: 88201; 88228.
- [100]^3: 699601; 699658.

A finite check for d=3 and 2≤N≤10 found no strict gain from this completion, while N=11 does improve. This does not claim there are no other constructions beating slices earlier.

## Infinite obstruction at every fixed d≥3

Let V_d(u)=Vol{x∈[0,1]^d:u≤Σx_i<2u}, with density h_d for the sum of d independent uniform variables. Then V'_d(u)=2h_d(2u)−h_d(u).

For 0<u≤1/2, V'_d(u)=(2^d−1)u^(d−1)/(d−1)!>0. For 1/2≤u≤1, the exact truncated-power density formula gives

(d−1)! V'_d(u)=(2^d−1)u^(d−1)−2d(2u−1)^(d−1)
≥(2^d−1−2d)u^(d−1)>0

when d≥3. In particular V'_d(1)>0, so V_d(1) is strictly below the maximum, and all maximizers have u>1. Continuity gives a fixed positive gap separating the maximizers from [0,1].

Uniform lattice counting for the finitely described slice polytopes gives |S_t|=N^d V_d(t/N)+O_d(N^(d−1)), uniformly over t. This can alternatively be obtained directly from the exact binomial formula. Hence for sufficiently large N, every maximizing integer threshold t satisfies t/N>1+ε_d for some ε_d>0. In particular t>N+d−1.

The d permutations of (N,1,…,1) have sum N+d−1 and are isolated. They are omitted by every largest plain slice and may be added. Therefore, for every fixed d≥3, plain coordinate-sum slices fail to attain f_d(N) for all sufficiently large N.

No contradiction with the asymptotic theorem arises: the total isolated boundary is O_d(N^(d−2)), smaller than its O_d(N^(d−1)) error allowance. This argument proves failure of an exact construction, not a new leading constant.

## Remaining gap

It remains unknown from this attempt whether isolated-completed slices are optimal. The next attempt tests this stronger finite candidate and whether an exact outer-shell recurrence can produce a sharp upper bound.

A strengthening: by fixing two coordinates N and 1 and allowing the remaining d−2 coordinates to range independently over a small positive fraction of [N], the omitted isolated count is Ω_d(N^(d−2)), not merely d. Attempt 4 improves this further by adding non-isolated top-shell points, reaching Ω_d(N^(d−1)).
