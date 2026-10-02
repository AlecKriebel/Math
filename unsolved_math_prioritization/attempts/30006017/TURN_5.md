# Turn 5: a flat-disk area-continuity obstruction and the final transfer gap

**Fifth and final substantive author turn. Original centered random-area question unresolved.** This last attempt tests whether the source's conjectural developed-boundary limit could be enough to transfer the continuum theorem. It cannot be used that way without additional area control. The construction below lies in the actual geometric class of flat translation disks, can be made generic, and even has bounded normalized quadratic side energy. It is not a counterexample to the source's conditional-uniform Gaussian ensemble.

## 1. A polygonal annular-cover disk

Fix 0<a<1. Let q_j be the counterclockwise successive corners of the square [-1,1]^2, with q_0=(1,1) and q_(j+4)=q_j. For j=0,...,4N−1 take a separate copy of the quadrilateral with developed vertices

    q_j, q_(j+1), a q_(j+1), a q_j.

Glue successive quadrilaterals along their matching radial edges, preserving the developed coordinates, but do not identify the last radial edge with the first. The resulting chain is a topological disk D_(N,a). Each quadrilateral has area 1−a², so the intrinsic area is

    Area(D_(N,a))=4N(1−a²).                                 (1)

The developing map winds N times around the square annulus, with multiplicity N on its interior. Its planar union has only area 4(1−a²); using that union would therefore be the wrong area convention.

To verify that this is a translation disk without interior singularities, split each quadrilateral along a diagonal. Its two consistently oriented triangles have doubled areas 2(1−a) and 2a(1−a), both strictly positive. Consecutive quadrilaterals are glued along a full boundary edge in a chain, so induction proves that the union is a disk. All vertices stay on its boundary. Thus there are no interior vertices at which a cone singularity could appear; along an interior edge the two developed triangles occupy opposite sides and give an ordinary flat neighborhood.

The boundary has 8N+2 sides: 4N outer sides traversed counterclockwise, one inward radial side, 4N inner sides traversed clockwise, and one outward radial side. Repeated developed vertices are distinct intrinsic boundary vertices. The boundary signed-area formula agrees with (1), as required by Turn 1. This geometric example is nongeneric initially, because many side vectors repeat; genericity will be restored below.

## 2. Exact quadratic-energy normalization

Let Q_(N,a) be the sum of squared side lengths of this unscaled boundary. There are 4N outer sides of length 2, 4N inner sides of length 2a, and two radial sides of length sqrt(2)(1−a). Hence

    Q_(N,a)=16N(1+a²)+4(1−a)².                              (2)

Scale every developed coordinate by

    r_(N,a)=sqrt(2/Q_(N,a)).

The scaled disk has total quadratic side energy exactly 2, which is the limiting mean quadratic energy of the standard planar Brownian-bridge increments. Its area is

    A_(N,a)=8N(1−a²)/[16N(1+a²)+4(1−a)²]
                -> A(a):=(1−a²)/[2(1+a²)].                 (3)

For a=1/2, A(a)=3/10; for a=1/3, A(a)=2/5. Thus two families with the same side count n=8N+2 and the same energy normalization have different positive area limits.

They also match the limiting quadratic covariance normalization. For the unscaled side vectors v_i,

    sum_i v_i v_i^T
      =8N(1+a²) I + 2(1−a)² [[1,1],[1,1]].                 (4)

After scaling by r², both diagonal entries are exactly one and the off-diagonal entry is 4(1−a)²/Q_(N,a), tending to zero. Consequently the quadratic matrix tends to I. Every individual scaled side is O(N^(-1/2)).

Nevertheless the entire developed image lies in [-r,r]^2. After translating the starting vertex to zero, the developed boundary curves converge uniformly to the constant zero curve, regardless of their continuous parametrizations. Their areas tend to the distinct positive numbers in (3). The extra quadratic-increment normalization therefore does not restore continuity of area under uniform developed-boundary convergence.

## 3. Generic perturbations remain genuine flat disks

The degeneracy of the initial repeated side set is not essential. Use the fixed abstract triangulated disk just constructed. It has n=8N+2 boundary vertices, all free as developed coordinates modulo translation, and no interior vertices. Strict positivity of its finitely many triangle orientations is an open condition on these coordinates. Every sufficiently small perturbation of all boundary coordinates therefore yields another flat translation disk with the same abstract triangulation. Interior edge neighborhoods remain flat for the same two-sided reason as above.

The generic side-set condition is dense in this open parameter set. To see this explicitly, boundary coordinates modulo translation are linearly equivalent to ordered zero-sum side vectors (v_1,...,v_n). For disjoint nonempty U,V with U union V not all indices, the forbidden equation is the polynomial

    det(sum_(i in U) v_i, sum_(j in V) v_j)=0.

It is not identically zero on the zero-sum vector space: choose one index from U, one from V and one outside their union, give their vectors respectively (1,0), (0,1), and (−1,−1), and set the other vectors to zero. The determinant is then one. This witness only proves that the polynomial is nonzero; it is not asserted to be a valid polygon itself.

There are finitely many forbidden polynomial zero sets. Their union has empty interior, so every sufficiently small open perturbation neighborhood contains generic side vectors. Rational coordinates can also be chosen because rational points are dense in the open complement. Genericity in particular excludes zero and repeated side vectors here.

For each N choose such a perturbation with every unscaled vertex displaced by at most delta_N, where delta_N decreases sufficiently fast, for instance below N^(-2) and below a fixed orientation-preservation margin for the chosen a. The original triangle areas and edge lengths have N-independent positive/finite bounds at this fixed a, so such a margin is available. The boundary shoelace area and quadratic energy change by O(N delta_N): there are O(N) terms and all unscaled developed coordinates are uniformly bounded. Rescale the perturbed disk once more to make its energy exactly 2.

Since Q_(N,a) is of order N, these changes do not alter the limits in (3)–(4), the O(N^(-1/2)) bound on the maximal side, or uniform collapse of the developed boundary. We have therefore constructed **generic** flat disks with all the advertised properties. Genericity is not being discarded to obtain the discontinuity example.

## 4. What the example refutes and what it does not

The construction refutes the following proposed proof step: a developed-boundary scaling limit, plus Brownian-order quadratic side energy and vanishing maximal side, automatically determines the O(1) intrinsic-area limit. Even inside generic translation disks, identical uniform boundary limits and identical limiting quadratic matrices can coexist with different positive areas. Microscopic multiplicity can survive while the developed boundary becomes uniformly small.

It does not refute the source's random-area conjecture. These are deliberately selected disks, not disks chosen uniformly conditional on standard Gaussian bridge increment sets. For a generic fixed set a singled-out filling has only its specified share of the finite uniform ensemble; constructing one filling says nothing about the typical conditional-uniform disk. The quadratic-matrix conditions in (4) are not a replacement for the source's Gaussian law. No claim that the example has that law, or that it controls its probabilities, is made.

Likewise, this is not a contradiction to the continuum limit of Turn 4. That theorem controls a precisely defined excursion-layer functional and a prescribed shrinking cutoff, whereas the construction here tests a much weaker boundary-continuity inference. An actual finite disk identity or a quantitative area approximation can contain information that plain boundary convergence loses.

## 5. Final mathematical position

After five attempts, the retained results are:
1. Exact multiplicity tilting, affine covariance, and independent Gaussian radial factorization of the actual source ensemble. The radial factor is negligible at the centered fluctuation scale, using the credited mean theorem.
2. A complete conditionally centered Gaussian width construction on excursion layers, with deterministic small-component variance control.
3. A credited critical-tree construction of the Abel-renormalized continuum area, plus a general obstruction to automatic Abel/sharp-cutoff equivalence.
4. A complete sharp-cutoff continuum L2 limit, with O(epsilon^(1/4)) error, using the credited uniform tree variance estimate.
5. A generic flat-disk counterexample to the boundary-area continuity route, even under normalized quadratic side statistics.

The central finite-model bridge remains unproved: no verified representation identifies the source's uniform flat-disk area with the continuum width cutoff plus a controlled random or deterministic error. The available report/slides state the finite bijection and conjectural boundary picture but do not provide a complete area-preserving approximation theorem. Recovering that theorem, or replacing it with a direct tightness and limit-law analysis of the exact filling-multiplicity tilt, is still necessary.

The source expectation constant alone does not identify the limiting distribution or the random error. The work therefore does not assert that the original centered area converges to U+C, and does not claim a counterexample for the original ensemble. The general phrase 'fixed generic side set' in the imported short statement is not used to manufacture a rescaling counterexample to the intended Brownian model.

**Final original disposition: unresolved, five substantive author turns completed out of five.** No sixth author search is undertaken. Independent review must audit the source scope, credited theorem transfers and all scoped proofs before publication. Historical novelty remains unverified.
