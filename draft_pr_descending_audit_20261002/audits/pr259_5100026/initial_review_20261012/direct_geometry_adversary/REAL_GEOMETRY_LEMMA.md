# Independent real construction lemma

Derived 2026-10-12 11:51:17 UTC in the direct Cartesian family, after reading
the submitted proof; this is a separate Euclidean proof of real finiteness,
not part of the pre-proof independence freeze. Audit estimate 80% complete.

Let E be a nondegenerate ellipse, and take three consecutive distinct
vertices P0,P1,P2 of an actual billiard orbit tangent to a strict nested
elliptical caustic. Let R be the intersection of the tangents to E at P0,P1,
and S the intersection of the tangents at P1,P2. If M is strictly inside E,
the lines at R and S perpendicular to R-M and S-M have a finite unique
intersection. In particular, either original focus is allowed. No parity
hypothesis is needed for this finiteness assertion.

Proof. Consecutive vertices cannot be antipodal: their chord would pass
through the center, which lies inside the caustic and therefore cannot lie
on any tangent to that caustic. Distinct ellipse tangents are parallel only
at antipodal tangency points. Thus R,S are finite.

Also P0 cannot equal P2: a two-bounce return requires a chord normal to the
boundary at both endpoints, which for an ellipse is an axis diameter; that
again passes through the caustic interior. The three tangent points are
therefore distinct. R cannot equal S, since at most two tangents to a real
strictly convex conic can pass through an exterior point (equivalently,
restrict the dual conic to the pencil of lines through that point; it is a
quadratic). Otherwise three distinct tangents would be concurrent at R.

Both R and S lie on the tangent at P1. If their normal vectors R-M,S-M
were dependent, then R,S,M would be collinear. Their line is the tangent
at P1, which contains no strictly interior point of E. Contradiction.
The two antipedal normal equations therefore have nonzero determinant.

More explicitly, let H be the outward unit normal, T=JH the unit tangent,
and write R=P1+rT,S=P1+sT. Then

det(R-M,S-M)=(s-r)(P1-M) dot H.

Here r!=s and (P1-M) dot H>0 by strict interiority. For an original focus,
the support identity h_E(H)^2-(M dot H)^2=b^2>0 also verifies the latter.

This proof supports the submitted real-domain conclusion even without the
Jacobi determinant formula. It does not prove phase invariance.
