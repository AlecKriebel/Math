# Optional quadratic-tangency strengthening

Problem 30003527, shared pass 4, 13 October 2026. Authored supplement to REGULAR_RADIUS_COUNTEREXAMPLE.md, whose frozen bytes remain unchanged. This does not resolve existential good radii or the full invariant-enlargement problem.

## Construction and exact bad core

Keep the same Q_0,Q_1,T and sheets C_-=Q_0×{-2}, C_+=Q_1×{2}. Replace the flat wall by

W_δ={(x,δz²,z): -1≤x≤1, -2≤z≤2}, δ=1/100.

Set C'=C_-∪C_+∪W_δ. These are disjoint compacta, each homeomorphic to a planar compactum. Hence C' is movable. Its bounded globally Lipschitz vertical-slowing field defines a full flow as before.

The wall projection has 0≤y≤4δ=1/25 and is disjoint from the sheet projections, which have y≥9/10. Its full vertical hull is

H_δ={ (x,y,z): -1≤x≤1, δz²≤y≤4δ }.

It is convex. Every vertical wall gap is contained in the unit neighborhood of W_δ: a point (x,y,z) in H_δ has the wall point (x,δz²,z) at distance y-δz²≤4δ<1. Thus the entire wall hull is selected at radius 1.

For a sheet-overlap base (x,y), we have 0≤x≤1/10 and 1≤y≤11/10. At its gap midpoint, the squared distance to a wall point with vertical coordinate s is

(y-δs²)²+s²
= y²+(1-2δy)s²+δ²s⁴≥y²,

with equality at s=0. The x-coordinate can be matched on W_δ, so the midpoint's distance to W_δ is exactly y. Its distance to each sheet is at least 2. Consequently no sheet gap with y>1 is selected at radius 1.

If y=1, every point of the closed sheet gap has distance at most 1-δz²≤1 to the same-height wall point. Exactly the binding gaps therefore fill. With the same nonmovable D as in the main report,

M_1(C')=H_δ disjoint union D.

Thus M_1(C') is nonmovable.

For completeness, all 0<r<1 are still good. The sheet gaps remain absent by the midpoint test. A wall gap at a fixed 0≤y≤4δ has maximum distance exactly y: its midpoint has distance y by the same squared-distance calculation, and each other point has distance at most y to a same-height wall point. Hence

M_r(C')=C_-∪C_+∪E_r,
E_r=W_δ∪{(x,y,z)∈H_δ:y≤r}.

The homotopy replacing y by (1-t)y+tδz² on E_r fixes W_δ and stays in E_r. It is a strong deformation retraction to W_δ. Thus E_r, and the finite disjoint union M_r(C'), are movable by shape invariance.

## Radius 1 is still ambient regular

In fact no Clarke critical value occurs at distance ρ≥3/5. It suffices, by the elementary implication proved in the main report, to exclude a∈conv Π_{C'}(a) at those distances.

Suppose such a=(x,y,z) exists. Convex-hull containment gives

-1≤x≤1, 0≤y≤11/10, -2≤z≤2.

The same-height wall point gives ρ≤|y-δz²|. Since δz²≤1/25<3/5≤ρ, the negative alternative is impossible. Therefore

y≥ρ+δz² and 3/5≤ρ≤11/10.

Both sheets cannot contain nearest points, since their separation is 4>2ρ. At least one sheet must have positive weight in a convex representation of a, because every wall point has y≤1/25 while a has y≥3/5. Assume first that the participating sheet is at height 2. Its being nearest implies |z-2|≤ρ≤11/10, hence z≥9/10>0.

Every nearest wall point has x-coordinate x. Its vertical coordinate s minimizes

f(s)=(y-δs²)²+(z-s)², -2≤s≤2.

A negative s cannot minimize when z>0: replacing it by -s preserves the first term and strictly reduces the second. For 0≤s<z,

f'(s)=2(s-z)-4δs(y-δs²)<0,

because y-δs²≥3/5-1/25>0. Hence every minimizing s satisfies s≥z. All nearest wall points therefore have vertical coordinate at least z; the participating upper sheet has height 2. A convex combination of those points can have vertical coordinate z only if z=2. The lower-sheet case is symmetric and forces z=-2.

The x-coordinate equation, since nearest wall points have x-coordinate x and all sheet points have x-coordinate in [0,1/10], forces x∈[0,1/10]. Choose any point c in the participating sheet. As before,

|x-c_x|≤1/10, |y-c_y|≤1/2, z=c_z,

so ρ≤sqrt(26)/10<3/5, a contradiction. Thus the same global regular-value exclusion is valid for C'.

## The bad boundary contacts are strictly quadratic

Fix a binding point (x,1)∈T. At a=(x,1,0), the unique nearest point of C' is (x,0,0)∈W_δ; the two sheets are at distance at least 2. The nearest-point minimization on the parabolic wall has a strictly positive second derivative there, and, in a neighborhood, gives a smooth distance function and smooth unit distance surface. One can see its local geometry directly from the unit normal offset of the parabola:

y(s)=δs²+1/sqrt(1+4δ²s²),
z(s)=s-2δs/sqrt(1+4δ²s²).

At s=0, z'(0)=1-2δ>0. Writing this boundary as y=h(z), its expansion is

h(z)=1+[δ/(1-2δ)]z²+O(z⁴).

Thus the vertical orbit through the binding gap is quadratically tangent to the smooth boundary at its midpoint. Both adjacent portions lie strictly inside the unit neighborhood: at y=1 and z≠0 their distance to the same-height wall point is 1-δz²<1. There is no boundary orbit segment near the contact, in contrast to the flat-wall version.

This defeats a repair that merely forbids orbit segments contained in the boundary, or merely asks for nondegenerate quadratic contacts. The contacts here are internal, so this is still not an isolating block. No statement about genuine isolating blocks is contradicted.

All extra arguments are elementary and use the main report's already identified movability and regular-level inputs. This optional strengthening is unaccepted until independently audited. No remote mutations or new source searches were performed for it.
