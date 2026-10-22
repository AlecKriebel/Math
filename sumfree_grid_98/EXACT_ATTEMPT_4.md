# Exact finite-grid attempt 4: shell recurrence and completed slices

Date: 2026-10-20. This strengthens attempt 3 at the full boundary-error scale. No general exact upper theorem is claimed.

## Exact outer-shell identity

Put Q=[N−1]^d and T=[N]^d\Q. Every point of T has a coordinate N and cannot be a summand in a grid-internal relation. Once a sum-free F⊆Q has been chosen, every point in T\(F+F) may be added, simultaneously and safely. Every point of (F+F)∩T must be excluded. Hence

f_d(N)=N^d−(N−1)^d+max_(F sum-free in Q) [|F|−|(F+F)∩T|].

This is an exact profile recurrence, not a scalar recurrence in f_d(N−1): the shape of F+F on the shell matters, not just |F|.

## A two-sided boundary completion

For integer t≥d let S_t={x∈[N]^d:t≤Σx_i≤2t−1}. Define

B_t=S_t ∪ {x:max_i x_i=N, Σx_i<t} ∪ {x:min_i x_i=1, Σx_i≥2t}.

This is sum-free:

- Added low points cannot be summands because they have a coordinate N; they cannot be targets of two slice points because their rank is below t.
- Added high points cannot be targets because they have a coordinate 1. As summands with slice points or other high points their sum rank exceeds 2t−1, so the result is not in the slice; it cannot be any high target, and cannot be any low target.
- Any relation using a low added point as a summand leaves the cube.

No new-new relation has been omitted in this reasoning.

Its exact cardinality simplifies to

|B_t|=N^d−(N−1)^d+H_{d,N−1}(2t−1−d)−H_{d,N−1}(t−1).

Indeed, first add the missing low top-shell count H_{d,N}(t−1)−H_{d,N−1}(t−1). Then add the high bottom-face count N^d−(N−1)^d−H_{d,N}(2t−1)+H_{d,N−1}(2t−1−d). The three pieces are disjoint.

This formula happens to equal the outer boundary count plus a rank-slice count on a translated smaller cube. That is only a counting identity; it is not a general invariance of sum-freeness under translation.

## Strictly better than isolated completion

Exact integer evaluation gives:

| grid | best isolated-completed slice | constructed B_t | t |
|---|---:|---:|---:|
| [29]^3 | 17,420 | 17,423 | 34 |
| [30]^3 | 19,272 | 19,275 | 35 |
| [50]^3 | 88,228 | 88,246 | 57 |
| [100]^3 | 699,658 | 699,788 | 113 |
| [11]^4 | 11,902 | 11,906 | 18 |
| [9]^5 | 51,514 | 51,519 | 18 |
| [8]^6 | 238,842 | 238,848 | 19 |

The code `boundary_completion.py` and `BOUNDARY_COMPLETION_RESULTS.json` use only exact integer formulas. Thus the proposed repair “take an optimal slice and add all isolated points” is itself false as a general finite solution.

## Boundary-scale asymptotic improvement

Attempt 3 proves that every largest plain slice has t/N≥1+δ_d for all sufficiently large N when d≥3. Choose ε>0 small enough that (d−1)ε<δ_d/2 and ε<1/2. Fix x_1=N and choose every other coordinate in {2,…,floor(εN)}. These Ω_d(N^(d−1)) points have rank below t for large N and can all be added to the slice. They are not isolated because none of their coordinates is 1.

Consequently the largest B_t exceeds the best plain slice by Ω_d(N^(d−1)). Since all isolated points together number only O_d(N^(d−2)), it also exceeds every isolated-completed slice for sufficiently large N. This remains fully compatible with an asymptotic theorem whose error is O_d(N^(d−1)).

## Inclusion-maximality in a central threshold range

Under all three conditions

d≤t, 2t≤dN+1, and dN≤4t−2,

B_t is inclusion-maximal (not necessarily maximum-cardinality).

Proof: an omitted low point w has rank r<t and all coordinates at most N−1. The coordinate box 1≤y_i≤N−w_i realizes every integer rank from d to dN−r. Since d≤t and dN−r≥dN−(t−1)≥t, choose y with rank t. Then y and w+y both lie in S_t, so adding w violates sum-freeness.

An omitted high point w has rank r≥2t and every coordinate at least 2. Split w=y+z coordinatewise with 1≤y_i≤w_i−1. All ranks from d to r−d can be attained. Because d≤t and 2t≤r≤4t−2, there exists a split with both ranks between t and 2t−1. Thus y,z∈S_t, and adding w again violates sum-freeness. Equal y,z are allowed, as required.

The extra condition 2t≤dN+1 is necessary for the stated proof and must not be dropped: d=1,N=3,t=3 would otherwise give the non-maximal singleton {3}.

## Next gap

The shell identity yields a genuine exact objective but no matching universal upper bound for B_t. Attempt 5 investigates improving B_t by changes involving non-shell points, and records any obstruction to a scalar or compression-based upper proof.
