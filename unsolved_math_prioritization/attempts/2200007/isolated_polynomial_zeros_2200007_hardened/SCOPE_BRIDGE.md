# Exact scope and the credited counterexample

## Target

On page 2 of [Shapiro's arXiv version](https://arxiv.org/pdf/1503.05295),
Problem 3 defines the maximum over real nonnegative polynomials of degree 2k
in l variables expressible as sums of squares of real polynomials of degree
at most k. Conjecture 4 asserts that this maximum equals k^l for every l.
Isolation concerns the real zero set. The statement adds no complex-finiteness
hypothesis, no genericity hypothesis, and no restriction to homogeneous forms.

The complete page was visually inspected on 6 October 2026. The shorthand in
the exact-ID catalog is therefore interpreted through its preceding definition.
The source's asymptotic discussion of the different non-SOS extremal function
is not an additional hypothesis of Conjecture 4.

## Verification of prior work

The construction below belongs to DannyExperiments' [designated manuscript](https://github.com/DannyExperiments/ottaviani-shapiro-sos-counterexample/blob/41e3d18a8c536e5a859201afd5faefe2b0ecd315/paper/manuscript.tex),
Theorem 1.1. This is a fresh explanation of its applicability, not a new result.

In coordinates (t,x_0,...,x_8), set

    q_0 = x_0^2 + t(t-8),
    q_i = x_i^2 - (t-i+1)(t-i),  1 <= i <= 8,
    P = sum_{i=0}^8 q_i^2.

The coefficient of x_0^4 is 1, so P has degree exactly four. It is nonnegative
and its summands are quadratic. For real inputs, P vanishes precisely when
all q_i vanish. Their equations require t(8-t) and each (t-i+1)(t-i) to be
nonnegative. The former restricts t to [0,8]; the latter exclude all eight
open unit intervals. Thus t is one of 0,...,8. Every such value is feasible.

For an interior integer j, the vanishing radicands have indices j and j+1.
At 0 the indices are 0,1; at 8 they are 0,8. Each remaining radicand is
positive. Each slice therefore has seven independent sign choices, giving
128 distinct points. There are nine slices, hence 1,152 points in total.
The zero set is finite, so every point is isolated. Therefore the extremal
value at (k,l)=(2,10) is at least 1,152, exceeding 1,024. Conjecture 4 is false.

The arithmetic checker corroborates the degree, signs, slices, and count.
The explanation above, not a finite sample, excludes every other real t.

## Relation to the adjacent problem

[PR 825](https://github.com/AlecKriebel/Math/pull/825), pinned at
848693c9e6e3b4d9449b4a672bb63be026c65511, concerns ID 2200006, the request for
the exact extremal function. Its authored Section 5 and separate audit already
verify the same credited counterexample. Its unresolved exact-maximum status
does not make the universal equality in ID 2200007 unresolved. Conversely,
refuting that equality does not solve ID 2200006. No work on its upper bound
or general families is repeated here.

## Limits and stopping point

The prior disproof supplies a terminal answer to this conjecture. Zero new
research approaches were undertaken, and no further proof search is needed.
The exact maximum, minimal counterexample dimension, general families, and
absolute priority are outside this verification. Source audit labels are not
substitutes for checking the elementary certificate. No human specialist review
or kernel-checked formalization is asserted.
