# Results and precise limits

## Exact setting

The base field is C. Two fixed rank-three linear pinhole cameras P3 rationally map to P2 and have distinct centers. Image and world curves are reduced, integral, closed, projective curves. Both camera maps are generically defined on the world curve, and each image closure equals its prescribed image curve. Singular images, epipoles, epipolar-line images, world-center incidence, and baseline intersections are allowed.

Unknown cameras, other camera models, real visibility, positive characteristic, nonintegral-input conventions, and all interpretations of the informal broad AIM problem are outside the result. This is an established-tools synthesis without a novelty or exhaustive literature-priority claim.

## Exhaustive classification

1. If exactly one image is epipolar, or the two epipolar lines do not correspond, no lift exists.
2. For corresponding epipolar lines, all lifts are integral curves in the common epipolar plane other than lines through either center. A world degree d and projection degrees r1,r2 occur exactly when d>=1, 1<=r_i<=d, and r1+r2>=d. Smooth lifts occur for d=1,r1=r2=1, or d>=2 and independently r_i in {d-1,d}. This branch is an infinite family, not a finite candidate list.
3. If neither image is epipolar, at least one lift exists. All lifts are exactly the nonbaseline reduced support components of the intersection of the two explicit cones, giving a finite input-derived candidate list. Every genuine component has scheme coefficient one. Compute degrees and embedded smoothness on the selected reduced primes.

## Degree and smoothness corrections

On a normalized fiber-product component T, write k for the epipolar-map degree and D_i for pulled-back image-epipole base divisors. Then world degree is k+deg max(D1,D2). Center multiplicities are deg(D2-D1)_+ and deg(D1-D2)_+, and degree(C)=r_i degree(C_i)+mult_ci(C). The baseline scheme coefficient is m1*m2+sum_T deg min(D1,D2), with m_i the image-epipole multiplicities. It is not always m1*m2: two smooth conic epipoles can give a doubled baseline.

Embedded smoothness is equivalent to injectivity and immersion of the actual normalization-to-world map, or to emptiness of the selected reduced prime's projective Jacobian singular locus. Smooth abstract normalization alone is insufficient. The local criterion compares center/baseline collisions globally within each selected component. Saturating by the baseline ideal removes its component, while retaining points of surviving curves on the baseline. All these claims and the exceptional-family sufficiency are proved in full in the linked reports.

## Effectivity and implementation

The geometric results hold over C. Literal terminating computation requires an effective exact coefficient presentation and certified absolute decomposition, such as algebraic-number coefficients considered over their algebraic closure. Approximate floating-point samples or unspecified arbitrary complex constants are not promised exact decisions. No efficiency bound is asserted.

The implemented programs are exactly 13 finite exact fixture groups and a 430-tuple monomial check (degrees 1 through 12). No general-purpose reconstruction, arbitrary-input primary-decomposition, normalization, or smoothness solver was implemented. Written proofs establish generality; the programs check the disclosed finite examples.

## Acceptance

The independent mathematical review accepted the adopted scope with no remaining mathematical obligations inside that contract. The disposition is scoped_resolved1/5. The original acceptance-manifest SHA-256 is 713520104c62adf26b0a6437b1ce1f2a1540e1489d4ec71b8eb15c9f0564a3af. Public-edition hashes and provenance are in audit/ACCEPTANCE.json; the portable package manifest is separate. A changed proof requires renewed review.
