# Attempt 1: an unconditional baseline and the parallel-lift identity

Date: 2026-10-20 UTC. Queue row 1825, ID 30002421.

## Scope and result

The target remains unresolved by this attempt. The objects are finite unions of full affine-line chords of C = [0,1]^3, measured as sets, with total arclength L > 0. The tests below are closed axis-parallel cubes contained in C. Hence every lower bound below also holds if arbitrary cube rotations are permitted. No assertion for arbitrary rectangular boxes is substituted for this test class.

This attempt proves, with no dependence on line count,

    D_axis(A) >= 1 / (8 max(1,L)^(3/2)).

It also checks the exact lift from planar points. The planar square-versus-rectangle gap has an established remedy, but a further side-length factor appears when squares are lifted to cubes. It must not be silently discarded.

## 1. Direct proof of the baseline

Put K = [1/4,3/4]^3. If A ∩ K is empty, the closed cube K has discrepancy 1/8.

Otherwise choose x ∈ A ∩ K, and choose one of the full affine lines defining A through x. Set

    r = 1 / (4 sqrt(max(1,L))),   Q = x + [-r,r]^3.

Then Q ⊆ C. Parametrize that line by x + tv with ||v||_2 = 1. For |t| <= r, every coordinate of tv has modulus at most r, so this entire segment belongs to A ∩ Q. In particular H^1(A ∩ Q) >= 2r, including when the chosen point belongs to an intersection of several lines. Set union, not multiplicity, is enough for this inequality.

For L >= 1,

    mu_A(Q) - |Q| >= 2r/L - 8r^3
                         = 3/(8 L^(3/2)).

For 0 < L < 1, the same expression is 1/(2L) - 1/8 >= 3/8. Combining this with the empty-core case proves the displayed universal bound. The apparent impossibility of a core-intersecting chord when L is very small causes no issue: that branch simply cannot occur.

No number-of-lines estimate was used. Infinitely many possible choices of very short grazing chords do not affect the argument. Repeated lines, point intersections, and chords contained in boundary faces also cause no problem. The cube Q is a valid positive-side closed cube and its arclength includes any face-supported portions.

The optimized single-line choice, where permitted by the distance to ∂C, is r = (12L)^(-1/2), giving (2/(3 sqrt(3))) L^(-3/2). This optimizes the same one-line calculation, not the target order.

## 2. Why the full-chord hypothesis matters

The local segment of length 2r is available because the defining objects are full lines intersected with C. It is not available for an arbitrary finite union of truncated interior segments.

For illustration, take m^3 centers of the regular m × m × m grid, and around each put a short parallel segment of length L/m^3, for a fixed L > 0 and large m. Their total length is L. The normalized measure is the average of equal-mass segments, each at distance O(L/m^3) from its grid center. For cubes, the discrepancy tends to zero as m grows: only grid cells meeting a cube boundary contribute to the cell-count error, O(m^2) cells out of m^3, and the short-segment perturbation has the same vanishing boundary-cell control. This is not an admissible counterexample, since these are truncated segments rather than full chords. It explains exactly why an argument that treats arbitrary rectifiable support of length L cannot prove the intended result.

## 3. The parallel-lift calculation

Let P be a set of N distinct points in [0,1]^2, and put

    A_P = union_{p in P} ({p} × [0,1]).

Then L = N. For a closed axis-parallel cube Q = S × I of side s, with S a square in [0,1]^2 and I an interval in [0,1],

    H^1(A_P ∩ Q) = s #(P ∩ S),
    |Q| = s^3,
    |mu_A(Q) - |Q|| = s |#(P ∩ S)/N - s^2|.

Consequently

    D_axis(A_P) = sup_{S subset [0,1]^2 square} side(S) |#(P ∩ S)/N - |S||.

This is a side-length-weighted square discrepancy, not exactly the ordinary planar rectangle or square discrepancy. Since s <= 1, a small planar rectangle discrepancy does give the source's stated upper-bound implication. The reverse lower-bound transfer requires an additional argument that produces a suitably large square or otherwise controls the weight.

## 4. Square/rectangle literature check

The original Steinerberger statement and its following parallel-line motivation were inspected at printed page 2891 in the recovered official report. It explicitly says cubes; orientation and boundary conventions are not specified.

Ruzsa, *The discrepancy of rectangles and squares*, in the 1993 Graz proceedings, pp. 135–140, gives the planar comparison. A full elementary presentation is in Jiří Matoušek, *Geometric Discrepancy: An Illustrated Guide*, §6.3, Theorem 6.3, printed pp. 180–182. It proves an unnormalized Ω(log N) lower bound for axis-parallel squares completely contained in the unit square, by a constant-factor comparison with rectangle discrepancy. The accompanying attribution identifies the earlier square bound as Halász's unpublished argument, reproduced in Beck–Chen, and the elementary reduction as Ruzsa's.

This inspected presentation also explicitly warns that the analogous direct comparison between cubes and rectangular boxes in higher dimensions is not supplied. The planar theorem alone does not eliminate the factor side(S) in the preceding lift identity. No current-status claim is being based on a historical remark in the book.

Public references:

- Original report: https://ems.press/journals/owr/articles/12723
- Official report PDF: https://ems.press/content/serial-article-files/46480?nt=1
- Inspected mathematical proof and bibliography: https://people.fjfi.cvut.cz/vybirja2/TUM-IBC/Matousek_Geometric_Discrepancy.pdf

## 5. What is not proved

The lower bound L^(-3/2) is smaller than the required (log L)/L by a factor of order sqrt(L) log L. It does not settle the problem. A tube-volume estimate with a naked N r^3 endpoint term would not be a valid length-only proof without first controlling the relevant chords; the direct argument above avoids that issue. No universal c/L estimate, logarithmic estimate, or admissible counterexample is claimed.
