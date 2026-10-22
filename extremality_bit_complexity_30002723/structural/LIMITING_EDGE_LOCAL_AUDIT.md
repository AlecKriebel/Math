# Local audit: a zero limiting edge forces interior jumps and spikes to vanish

20 October 2026. This note assumes a perturbation h is already known to be affine on every open q-grid cell, so that point values and one-sided limits at every grid point exist. It uses the usual inherited limiting-additivity requirement: if the limiting slack of pi is zero along a coarse-face boundary, every corresponding approach has limiting slack zero for h.

Write J(u)=h(u+)-h(u-) and P(u)=h(u)-(h(u+)+h(u-))/2.

## Vertical edge

Let the limiting zero edge be x=t, with a coarse 2-face F lying locally to its right. Let (t,u) be an interior point of that edge, where u and z=t+u are q-grid points. Because u and z lie in open nonfixed coarse projections, pi is continuous at both of them; they are not original breakpoints.

Set A=h(t+), Y^e=h(u^e), and Z^e=h(z^e), with e in {-,0,+}. The following approaches lie in relint(F) for sufficiently small positive epsilon:

- x=t+epsilon, y=u-2epsilon gives A+Y^- - Z^-=0.
- x=t+epsilon, y=u+epsilon gives A+Y^+ - Z^+=0.
- x=t+2epsilon, y=u-epsilon gives A+Y^- - Z^+=0.

Subtracting yields J(u)=J(z)=0.

Two further approaches are essential for excluding isolated spikes:

- y=u exactly, x=t+epsilon gives A+Y^0-Z^+=0.
- x+y=z exactly, x=t+epsilon gives A+Y^- -Z^0=0.

They show Y^0=Y^-=Y^+ and Z^0=Z^-=Z^+, hence P(u)=P(z)=0. These are valid approaches within the original coarse 2-face: keeping a coordinate at an artificial q-grid point does not leave relint(F), because that point is interior to its original coarse projection.

For a left-side coarse face, reverse the appropriate signs. Horizontal edges follow by exchanging x and y. Diagonal edges follow by using x and x+y as local coordinates. In every case, all jumps and spikes at interior grid points of both nonfixed projections vanish separately, not merely in a linear combination.

## Actual additive edge versus a limiting edge

For an actual translation relation h(t)+h(y)=h(t+y), limits and point values at an interior pair give equal jumps and equal spikes.

For an actual reflection relation h(x)+h(t-x)=h(t), limits give

h(x-)+h((t-x)+)=h(t),
h(x+)+h((t-x)-)=h(t),

so J(x)=J(t-x). Taking the average of these equations and subtracting the pointwise equation gives P(x)=-P(t-x). Slopes are equal in both translation and reflection cases.

Thus the proposed local relation signs are correct: jumps are unsigned for either geometric orientation; spikes change sign exactly for reflections. The cell reflection is k -> qt-k-1, whereas the point reflection is k -> qt-k; these must not be confused in an implementation.

## Scope of this audit

This validates the local continuity assertion and signs. It does not alone prove that all remaining fine-grid active equations are captured by coarse zero-vertex sector equations. In that global reduction, sectors with one of delta x, delta y or delta(x+y) equal to zero must be retained. Considering only open two-dimensional sectors would incorrectly discard possible spikes.

## Global finite-system factorization: audit outline

Let N be any common multiple of the input breakpoint denominators, and work in the space of functions h affine on each open N-grid cell, with arbitrary point values at grid points. This is a finite-dimensional vector space. The following is the proposed exact factorization of its active-equality system; the arguments below find no extra mixed jump/slope constraint.

1. **Full zero coarse 2-face:** impose common slopes across all three open projections, and J=P=0 at all grid points in the open projections. One boundary sector equation sets the remaining constant Delta h to zero.
2. **Actual zero coarse 1-face:** impose paired slopes, paired unsigned J, and paired P with translation sign + and reflection sign -. These make Delta h constant at every point and one-sided limit on the open edge; one endpoint sector equation fixes this constant.
3. **Zero limiting edge of a coarse 2-face:** impose paired slopes and J=P=0 separately in both nonfixed open projections, as proved above. These make the limiting Delta h constant along the whole open edge; one endpoint sector equation fixes it.
4. **Zero coarse vertex sectors:** retain every feasible direction type whose corresponding limiting slack of pi is zero, including the exact point itself when its slack is zero. These supply all constants just mentioned and all isolated zero constraints.

For item 2, on successive fine-grid edge segments Delta h has derivative zero. At an interior grid point, its right-minus-left jump is J_y-J_z for a translation, or J_x-J_y for a reflection. Its point value minus the average of the limits is P_y-P_z for a translation, or P_x+P_y for a reflection. The proposed pairings therefore make the same constant persist across every interior grid point. There is no leftover independent intercept at each fine cell.

For item 1, necessity of common affine behavior follows directly from the bounded interval lemma. Conversely, common slope and zero J/P throughout the open projections make h affine on each entire open projection. Delta h is then constant over the full coarse face. For item 3, zero J/P removes all possible singular changes in the nonfixed projections, and paired slopes give zero derivative of the boundary limit.

For completeness, classify each fine-grid active equality by the coarse face containing its base point. If the base point lies in the interior of a coarse 2-face, its slack can vanish only if that coarse face is fully additive: a nonnegative affine slack cannot have an interior zero without vanishing identically. If it lies inside a coarse 1-face, the relevant actual or limiting slack is affine and nonnegative on that edge; an interior zero forces it to vanish along the whole edge. These are items 2 or 3, or the boundary of item 1. Otherwise the base point is a coarse vertex and item 4 applies directly. This exhausts all active fine-grid faces and their limit constraints.

The direction lines delta x=0, delta y=0 and delta x+delta y=0 divide a neighborhood into six open cones and six rays, plus the exact base point. Representatives of the six open cones can be chosen as (1,1), (2,-1), (1,-2), (-1,-1), (-2,1), (-1,2). The six rays can be represented by (1,0), (1,-1), (0,-1), (-1,0), (-1,1), (0,1). Using only directions with both coordinates in {-1,0,1} would miss some mixed-sign open cones. A sector relation uses the actual value for a zero directional coordinate and the corresponding one-sided limit otherwise.

If this factorization is used with N=4q, BHK Part I Theorem 4.11 supplies equivalence between uniqueness in this finite system and extremality against unrestricted competitors, including two-sided discontinuous input. This bypasses any need to infer global regularity of arbitrary perturbations. The factorization is the substantive authored lemma; BHK does not state the compressed algorithm.
