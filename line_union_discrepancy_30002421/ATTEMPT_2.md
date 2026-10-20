# Attempt 2: a rigorous counterexample for the axis-parallel interpretation

Date: 2026-10-20 UTC. Queue row 1825, ID 30002421.

## Result and exact limitation

For closed axis-parallel cubes, the proposed logarithmic lower bound is false. In fact, admissible finite unions of distinct, mutually parallel, full affine-line chords have discrepancy O(1/L), uniformly even over all closed axis-parallel rectangular boxes.

This does NOT disprove the question if its word “cubes” includes arbitrary rotations. The original source does not specify orientation, and the literature result used here does not provide the needed uniformity over changing orientations. This distinction is essential, not cosmetic.

## External theorem used

Bence Borda, *Bounded error uniformity of the linear flow on the torus*, Monatsh. Math. 189 (2019), 221–237; preprint arXiv:1803.06968v1 (2018), Corollary 2, printed preprint p. 4.

In the following paraphrase, R ranges over all axis-parallel boxes in [0,1]^d. If the coordinates of α are real algebraic and linearly independent over Q, there is a finite constant K_α such that, for all T > 0 and all starting points s,

    sup_R | integral_0^T 1_R({s+tα}) dt − T |R| | <= K_α.

The theorem's bound is uniform over boxes, not merely a bound for each fixed box. This exact quantifier was checked in the PDF page image and HTML.

Primary sources:
- https://arxiv.org/abs/1803.06968
- https://arxiv.org/html/1803.06968
- https://real.mtak.hu/98617/2/180306968v1.pdf
- Journal DOI recorded in bibliographic search: https://doi.org/10.1007/s00605-018-1211-x

The arXiv record supplies the journal reference above. The DOI webpage was not accessible through the research tool; no claim is made to have inspected the typeset journal article. The inspected author preprint has one listed arXiv version.

## Explicit admissible line unions

Let

    C = [0,1]^3,   α = (sqrt(2), sqrt(3), 1),   v = ||α||_2 = sqrt(6).

The three coordinates are algebraic and Q-linearly independent. For each integer n >= 1, consider the lifted straight path t ↦ tα, 0 <= t <= n. Break it at every time that one coordinate is an integer. There are finitely many such times. On each open interval between consecutive breaks, the integer vector k = floor(tα) is constant.

Let K_n be the collection of these k, and define

    ell_k = Rα − k,
    A_n = C ∩ (union_{k∈K_n} ell_k).

### Full chords, not truncated segments

For a fixed k∈K_n, the full preimage of C on the supporting line is

    I_k = { t∈R : 0 <= tα_j − k_j <= 1 for j=1,2,3 }.

Because all α_j are positive, I_k is a closed interval. Its interior is precisely the interval during which the path lies in the interior of k+C. At either endpoint at least one coordinate is on a face, so I_k maps onto the entire chord ell_k∩C.

There is no truncation of the first interval: t=0 is the origin, and negative t leaves C immediately. There is no truncation of the final interval: the third coordinate is t, so t=n is exactly an exit through the upper z face of the last visited cell. Thus every chord used is full without adding endpoint extensions.

### Set measure and distinctness

If ell_k = ell_l, then k−l = rα for a real r. The third coordinate gives r∈Z, while the first coordinate gives r sqrt(2)∈Z. Hence r=0 and k=l. The supporting lines are parallel and distinct, so they do not intersect at all. In particular arclength on their union is the sum of their lengths, with no multiplicity issue.

The intervals I_k partition [0,n] except for shared endpoints in parameter space. Their chord lengths are v|I_k|. Consequently

    L_n = H^1(A_n) = v n = sqrt(6) n.

For completeness, positive crossing times of distinct coordinate families cannot coincide, because every ratio of two coordinates of α is irrational. The number of positive-length chords is therefore

    N_n = floor(n sqrt(2)) + floor(n sqrt(3)) + n.

This formula is not needed for the discrepancy conclusion; the controlling parameter remains the exactly computed L_n.

### Boundary convention

On every chord all three coordinate derivatives are nonzero. A coordinate face of any axis-parallel test box therefore meets that chord in at most one point. A finite union of such face intersections has arclength zero.

At a wrap time, the torus representative uses coordinate 0 whereas the closed exit endpoint of the previous chord may have coordinate 1. These discrepancies occur only at finitely many points and have zero arclength and zero dt measure. Hence for every closed axis-parallel box R⊆C,

    H^1(A_n∩R) = v integral_0^n 1_R({tα}) dt.

Dividing by L_n = vn gives the exact normalized identity

    mu_{A_n}(R) = (1/n) integral_0^n 1_R({tα}) dt.

## Contradiction to the proposed rate in this test class

Borda's corollary gives

    sup_R |mu_{A_n}(R) − |R|| <= K_α/n = vK_α/L_n.

Axis-parallel cubes are a subclass of these boxes, so

    D_axis(A_n) <= vK_α/L_n.

Therefore

    D_axis(A_n) / ((log L_n)/L_n) <= vK_α/log L_n → 0.

For every proposed universal c>0, some sufficiently large n violates D_axis(A_n) >= c log(L_n)/L_n. The finite constant K_α need not be explicitly computed for this asymptotic counterexample.

## Optional completion lemma for general stopping times

The integer stopping construction above avoids all corrections. More generally, take any finite irrational torus orbit of speed v and duration T. Distinct wraps again have distinct supporting lines when Rα∩Z^3={0}. Only the initial and terminal pieces can be partial chords; complete those pieces. The added arclength e is at most 2 sqrt(3), and the full union has L=vT+e.

If the original orbit has unnormalized time discrepancy at most K on a test class, the completed union satisfies

    |H^1(A∩Q) − L|Q||
       <= vK + |added_length_in_Q − e|Q||
       <= vK + e.

Thus its normalized discrepancy is at most (vK+2 sqrt(3))/L. This completion argument is independent of the orientations of the test sets; the limitation comes from which uniform discrepancy theorem is available for the original flow.

## Why this does not settle arbitrary rotations

Borda's more general Theorem 1 permits polytope facets with algebraic normal vectors ν satisfying ν·α != 0. Its constant is allowed to depend on the facet normals. It does not bound the supremum over all rotating cubes. Cube orientations with a face parallel to α have ν·α=0 and fail a stated hypothesis. Constants also cannot be assumed uniform as normals approach those excluded directions.

No manipulation of “each fixed admissible orientation has a finite constant” into “all orientations share one finite constant” is valid. A rotation-dependent family of cubes could still have logarithmic or larger discrepancy on A_n.

## Source-status check

The entire inspected preprint, including introduction and references, was searched for Steinerberger and the original line problem. Neither appears. Borda instead explicitly explains that his result disproves a continuous-curve conjecture of Drmota. Thus it supplies the theorem needed for the axis-parallel counterexample, but does not itself resolve the orientation intended by Steinerberger's 2013 statement.

## Source retrieval verification

The author preprint PDF was retrieved from the institutional repository URL above, text-extracted, and p. 4 rendered and visually checked. It is 222149 bytes; SHA-256 fddef4d3a9f17befc11ab06e9d65c86e7db1bd18a7ba8893ed5da400065ad1b9. The source PDF, extracted text, and rendered page image are not included in this package. This file contains the authored reduction and public bibliographic metadata, not copied source text.
