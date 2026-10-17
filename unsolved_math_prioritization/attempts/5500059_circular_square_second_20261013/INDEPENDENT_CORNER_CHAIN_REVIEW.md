# Independent review of the corner chain and bridge appendix

Problem: row 1757 / 5500059 / AMR0540059. Review date: 2026-10-13.

## Separate verdict and frozen input

Accepted within its expressly restricted scope. The appendix constructs compatible corner-and-side patches of arbitrary finite chain length, allows finite polygonal approximation with ratio at most G+epsilon for every epsilon>0, and proves an obstruction to connecting the prescribed reflected constant-angle chains with just one boundary cell. It does not cover the square: four middle side intervals and an interior region remain uncovered.

This is a separate acceptance binding the complete 9045-byte `CORNER_CHAIN_AND_BRIDGE_OBSTRUCTION.md`, SHA-256 `cd3f06710e3cebfee00e7e524b54a095a5cd99ebbb760e8f3aac98cd431d2595`. It neither broadens nor changes the separate acceptances of the full 100-cell construction and the quantitative finite-N lower gap. No literature priority claim is made.

## Canonical cell and exact corner attachment

With the stated rational functions of t, independent symbolic calculation verifies that both upper strip points lie on the outer circle of radius F(t), the parallel strip width is exactly two, and U=rL. The two indisk contact parameters are below L and U by exactly the positive differences shown in the appendix. Consequently the convex hull has precisely the stated support segments. The actual inradius is one because of the retained width-two strip, and its actual circumradius is F(t) on the accepted three-contact branch.

For the corner, the balancing identity gives G=(1+t)/sqrt(2); this identity is used only at the accepted root t=t0. The disk at (1,1) fits in the outer circle because t>1/sqrt(2). Both axis and exit half-planes contain it. The point q is the second intersection of the exit ray with the outer circle since the nonzero quadratic root is V=b(s-c)>0. Its signed distance expression for the other exit line equals 2bsc(c+s)>0, so it does not protrude across the other separator. The same holds for the reflected point q'.

The corner's inradius upper bound is valid for any disk center: add the two exit inequalities, then use x+y>=2z and c-s<0 to deduce z<=sb/(1+s-c)=1. This avoids assuming that the named indisk is the only candidate. The distance between p and p' is exactly 2G, proving the outer radius is optimal. The exact identity V-t=(3t^2-1)/(1+t^2)>0 places q beyond the corner's disk contact. Scaling the strip cell by rho=V/L makes its complete left support segment exactly [p,q]. The opposite containing half-planes prove disjoint interiors independently of indisk tangency.

Seventeen exact rational-function identities and the necessary rational interval bounds are checked in a fresh independent algebra checker, with results in [the exact independent chain algebra audit](INDEPENDENT_CHAIN_ALGEBRA.json). The balancing-circle relation is checked as an identity involving the accepted root polynomial rather than silently treating C(t)=F(t) at arbitrary t. Four algebra mutations are independently rejected.

## Finite chains and polygonal approximation

The formulas for x_j and sigma_j give consecutive baseline endpoints exactly, and U=rL matches the entire consecutive support segment, including its upper endpoint. The cells occupy consecutive parallel strips, so nonconsecutive cells cannot overlap. The corner is on the opposite side of the initial strip support and is separated from all later strips as well.

For any fixed finite number of cells, the claimed outer polygonal approximations can retain the specified separators and exact segment endpoints. At each upper endpoint the tangent to the known outer circle is a supporting line through that point, independent of the segment's supporting line because the segment ray meets the circle twice rather than tangentially. Retaining these two lines fixes the endpoint. Baseline endpoints are already fixed by a baseline and separator. Additional finitely many support lines yield arbitrarily close outer approximations, while every original indisk remains contained. The strip width, or the four corner constraints, fixes each true inradius.

The enclosing-radius increase can be made less than epsilon times the corresponding inradius. Because the patch is finite, all nonincident cells have positive separation and all strict geometric margins can be preserved at once. Incidence pairs stay on opposite separator sides. This justifies finite polygonal patches with the asserted ratios and segments; it is not an infinite approximation or a claim that a finite polygon has exact ratio G.

## Placement at all four square corners

The appendix supplies sufficient strict margins for every pair class. Its bounds on A, c, r, rho, L and U are verified by rational interval arithmetic on 0.82<t<0.83, using the known tighter t<0.823 bracket for G<1.29. In particular the height of each bottom chain is below 1.664<b, whereas any adjacent-side chain starts at sidewise coordinate b. Thus adjacent perpendicular chains cannot meet. The sidewise extent of an individual strip cell is less than 2.3 sigma_j, whereas its baseline origin is more than 4.7 sigma_j from the midpoint. Each chain stays in its own half-side, so reflected chains are disjoint.

Corner patches remain in boxes of side below 2.21, and S>10. This separates distinct corner boxes and far-side strips. The original exit separators handle each corner's own adjacent chains; remaining pair classes are covered by the height, midpoint, or opposite-side margins. These strict margins also permit the finite polygonal approximations to stay within the same square without introducing overlap.

Summing the baseline increments gives the stated uncovered middle length g_M=4A*rho*r^M/(1-r)>0 for each side and cell count 4+8M. The construction is therefore correctly identified as incomplete. The limiting midpoint notation does not assert a partition by infinitely many cells.

## Restricted one cell bridge obstruction

The bridge argument uses the two specific endpoint separator directions theta and pi-theta. Its support-distance inequalities force the symmetric feet with u=A+hC, h>=1, C=cot(theta)>0. Including the unit-disk point (0,1) gives the displayed isosceles triangle. Since u<h+1, that triangle is acute, so its minimum enclosing circle is its circumcircle rather than a two-point diameter circle.

Differentiation gives exactly R_triangle'=(1-v^2)/2+C v>0 with 0<v<1. Minimizing over h>=1 yields 1+1/(4t^2), which is greater than 1.36 and hence greater than G. The centered-at-(0,-1/(4t^2)) circle with radius 1+1/(4t^2) contains the relaxed unit disk and feet, proving sharpness for those relaxed local data. It does not produce an equality polygon or a square completion.

This obstruction does not apply to chains whose angles change before the gap, multiple bridge cells, or an unrelated global construction. The frozen appendix states those limits accurately. Its acceptance supplies a further local construction and a restricted completion obstruction, while the original global optimization problem remains unresolved.
