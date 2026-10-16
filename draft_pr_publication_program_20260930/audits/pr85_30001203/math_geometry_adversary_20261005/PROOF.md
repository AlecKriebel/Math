# Independently checkable geometric derivation

This document was derived without reading the submitted prior review. It checks
the geometry and exact observation metric of the supplied construction. It is
not a proof of the imported Nash theorem, nor a claim of historical novelty.

## Precise tested statement

For a fixed `T>0`, define the history map

\[
\mathcal H_T(x)(t)=h(\varphi_t(x)),\qquad 0\leq t<T.
\]

Its local Gramian is the bilinear form

\[
P_{T,x}(v,w)=\int_0^T
\langle d(h\circ\varphi_t)_x v,d(h\circ\varphi_t)_x w\rangle\,dt.
\]

The target is a connected, closed, smooth 2-manifold, a globally defined smooth
complete vector field, and a smooth observation into finite dimensional Euclidean
space for which this exact Gramian is complete and uniformly negatively curved,
has uniform positive bounds relative to a fixed smooth background metric and in
one fixed finite atlas, and the history map is locally injective but globally
has two preimages for every attained history. The distinguished interval `T=1`
is enough; the derivation below also treats every other fixed positive `T`.

## 1. The hyperbolic polygon does yield a smooth closed surface

Work in the curvature `-1` hyperbolic plane. A regular geodesic octagon of interior
angle `alpha=pi/4` exists. One direct specification uses the right triangle from
the polygon center `O` to a vertex `V` and its adjacent side midpoint `W`.
The angles at `O`, `V`, and `W` are respectively `pi/8`, `pi/8`, and `pi/2`.
The hyperbolic cosine law for angles gives

\[
\cosh d(O,V)=\cot(\pi/8)^2=3+2\sqrt2.
\]

In the Poincare disk this means the vertex radius is

\[
r=\tanh(d(O,V)/2)=2^{-1/4}<1.
\]

The vertices `r exp(i k pi/4)`, `k=0,...,7`, with geodesic arcs between successive
vertices define the required compact polygon. Reflection symmetry of the triangle
gives the stated angles. This is an existence calculation in the ordinary
hyperbolic plane, not an assumption of the conclusion for a quotient surface.

The angle can be crosschecked without invoking the triangle law. At `(r,0)`
the two adjacent geodesic circles, orthogonal to the unit disk boundary, have
centers `(a,+/-b)`, where `a=(1+r^2)/(2r)` and `b=a tan(pi/8)`. Put
`c=a-r=(1-r^2)/(2r)`. Their inward tangent vectors are `(-b,+/-c)`.
For `r^2=sqrt(2)/2`, one obtains `b/c=1+sqrt(2)` and hence

\[
\cos\alpha=\frac{b^2-c^2}{b^2+c^2}=\frac{\sqrt2}{2}.
\]

The interior angle lies in `(0,pi)`, so it equals `pi/4`. The independent checker
verifies these equalities exactly in the quadratic field `Q(sqrt(2))`.

Number corners `v_i` cyclically modulo 8 and sides `e_i=[v_i,v_{i+1}]`.
Identify each `e_i` with `e_{i+4}` by an orientation preserving hyperbolic
isometry that reverses their boundary orientations. Equal geodesic side lengths
permit this identification.
Specifically, for `i=0,1,2,3`, identify

\[
v_i\sim v_{i+5},\qquad v_{i+1}\sim v_{i+4}.
\]

Interior points are unchanged hyperbolic disk neighborhoods. A nonvertex point
on a glued edge has two hyperbolic half disks: develop one across the geodesic
using the side isometry. Their union is a disk with the smooth hyperbolic metric.
The original metric is therefore not merely a piecewise smooth metric at edges.

At corner `i`, call the incident rays along `e_{i-1}` and `e_i` the previous and
next ray. The next ray at `i` is glued to the previous ray at `i+5`. Thus the
vertex link cycle is

\[
0\to5\to2\to7\to4\to1\to6\to3\to0.
\]

It contains all eight corners, once each. In particular, there is one vertex and
one circular link, rather than multiple link components meeting at a point.
Develop its eight sectors successively into the hyperbolic plane. Their total
angle is `8(pi/4)=2pi`. The final transition is an orientation preserving
hyperbolic isometry fixing the developed vertex whose derivative is the rotation
by `2pi`; hence its derivative is the identity. An isometry fixing a point and
its tangent frame is the identity (apply it to geodesics from that point).
Therefore there is no residual holonomy at the seam. The developed neighborhood
is an ordinary smooth hyperbolic disk, with no cone angle singularity.

The quotient is connected and compact. All boundary edges are paired and every
point has a disk neighborhood, so it has no boundary. Reversed boundary
orientations give a consistent orientation. It has one vertex, four edges, and
one face, hence Euler characteristic `1-4+1=-2`; this is the closed orientable
genus-two surface `S`. The local hyperbolic charts constructed above make its
metric `g` smooth (indeed real analytic), positive definite, and curvature `-1`.
This derivation makes the otherwise implicit side pairing concrete.

## 2. A connected smooth unramified double cover exists

The usual genus-two surface presentation is

\[
\pi_1(S)=\langle a_1,b_1,a_2,b_2\mid[a_1,b_1][a_2,b_2]=1\rangle.
\]

Hatcher gives the surface presentation on printed p. 51. Map `a_1` to 1 in
`Z/2` and each other generator to 0. Every commutator maps to 0 in an abelian
group, so the relation holds; the map is surjective. Its kernel `H` has index 2.
These are abstract generators in the standard surface presentation; they need
not coincide with the four paired-side letters of the opposite-side octagon.

The surface is path connected and locally path connected, and small disk
neighborhoods are simply connected. It thus satisfies the semilocal simple
connectivity assumption as well. Hatcher's Proposition 1.36 and Theorem 1.38
produce a **path connected** covering associated to `H`; Proposition 1.32 says
the sheet number equals the subgroup index. Consequently

\[
\pi:M\longrightarrow S
\]

is a connected, everywhere two-sheeted, unramified cover. This is not the
disconnected union of two copies of `S`. Equivalently the generator images act
on two sheets by one transposition and three identities; the action is transitive
and the surface relator acts trivially. The independent checker verifies this
explicit monodromy data.

Give `M` the chart structures pulled back from evenly covered disk neighborhoods
of `S`. The chart transition functions are the base's smooth transitions; thus
`M` is smooth and `pi` is a smooth local diffeomorphism. Hausdorffness follows by
separating distinct base images using base neighborhoods and separating points
in one fiber by disjoint sheets over an evenly covered neighborhood. A countable
atlas on `S` lifts to two sheets over each chart, so `M` is second countable.
The base orientation pulls back to an orientation on `M`.

A finite-sheeted cover of this compact surface is compact: choose finitely many
compact subsets `K_i` of evenly covered neighborhoods whose interiors cover `S`
(shrink a finite disk cover). Each `pi^{-1}(K_i)` is the union of two compact
copies of `K_i`, and these inverse images cover `M`. A finite triangulation of
`S` lifts with exactly two copies of each cell, so

\[
\chi(M)=2\chi(S)=-4,\qquad 2-2\operatorname{genus}(M)=-4.
\]

Hence `M` has genus three. Set `g_tilde=pi^*g`. It is smooth and positive definite
because `d pi` is invertible in every tangent space, and `pi` is a local isometry.

## 3. Nash applies with smoothness and the stated dimension

Nash's original Theorem 2, printed p. 59, states the compact result for a `C^k`
positive metric, with the same differentiability for the isometric embedding,
including every `3<=k<=infinity`; the ambient dimension is `(n/2)(3n+11)`.
The base `S` is compact, smooth, without boundary and its metric is `C^infinity`
positive definite. Taking `n=2`, `k=infinity` gives

\[
e:S\hookrightarrow\mathbb R^{17},\qquad
e^*\langle\ ,\ \rangle=g.
\]

The theorem gives an embedding, so it is injective, not just an immersion.
The theorem's `k=infinity` case supplies the required smoothness. No inference
from Nash's separate `C^1` result is made. The theorem statement and nearby
explanation were read directly in the original paper; its iterative proof is
an explicitly imported classical theorem, not reproduced by this review.

Let `h=e circ pi` and `f=0`. Both are globally defined and smooth. The zero field
has the global flow `varphi_t(x)=x` for every `t` in the entire real line; it is
complete independently of any metric completeness argument.

## 4. The Gramian is exactly the pulled back metric

For a constant state trajectory, a fixed local chart works for all times.
In that chart `Df=0`, so the variational system has fundamental matrix `Phi=I`;
its output matrix is the fixed Jacobian `H=Dh(x)`. Thus

\[
P_T(x)=\int_0^T (Dh(x))^T Dh(x)\,dt=T(Dh(x))^T Dh(x).
\]

Independently and intrinsically, the history differential is the constant
function with value `dh_x v`. Therefore

\[
\begin{aligned}
P_{T,x}(v,w)
&=T\langle de_{\pi(x)}d\pi_xv,de_{\pi(x)}d\pi_xw\rangle\\
&=Tg_{\pi(x)}(d\pi_xv,d\pi_xw)\\
&=T\widetilde g_x(v,w).
\end{aligned}
\]

This verifies the original observability integral, not an arbitrary metric
selected independently of the measured map. Integration over `[0,T)` or `[0,T]`
has the same value here. Since `T>0` and `g_tilde` is positive definite, the
Gramian is a positive definite smooth Riemannian metric.

## 5. Bounds have valid intrinsic and fixed-atlas forms

Fix any smooth Riemannian metric `q` on compact `M`. The `q`-unit tangent bundle
is compact. On it `g_tilde(v,v)` is a continuous, strictly positive function, so
it has a minimum `c>0` and a finite maximum `C`. Hence, for each fixed `T>0`,

\[
Tc\,q\leq P_T\leq TC\,q.
\]

These constants compare metrics on the same tangent spaces and do not rely on
the convenience of choosing `q=g_tilde`.

The inherited local hyperbolic charts can be centered at the disk origin by a
hyperbolic isometry and shrunk to Euclidean disk radius `r_i<=1/2`. Every point
has such a neighborhood; compactness gives finitely many covering neighborhoods.
On each of these chosen charts, with `s=u^2+v^2<1/4`,

\[
P_T=\frac{4T}{(1-s)^2}I_2,\qquad
4T I_2\leq P_T\leq\frac{64T}{9}I_2.
\]

Different chart radii cause no problem because the same enclosing radius gives
the displayed common constants. There is no claim that the chart centers alone
cover the manifold, or that one disk of radius `1/2` injects at every point.

This verifies uniform bounds for **one fixed finite atlas**, and an intrinsic
comparison with any fixed background metric. Bounds relative to the identity
matrix cannot be coordinate invariant over *all* possible changes of coordinates:
replacing `z` by `w=a z` divides the metric coefficient matrix by `a^2` at the
corresponding point. No positive lower bound survives arbitrary `a`. Also, the
nonzero Euler characteristic prevents a single global smooth tangent frame on
this surface. Neither is a defect in a question stated in local coordinates;
they are reasons to state the exact meaning of the uniformity condition.

## 6. Curvature, scaling and completeness

A local isometry pulls back Gaussian curvature. Thus `K(g_tilde)=-1`.
In the chosen disk coordinates this can also be checked directly. Write

\[
P_T=e^{2\phi}(du^2+dv^2),\qquad
\phi=\log(2\sqrt T)-\log(1-u^2-v^2).
\]

With `s=u^2+v^2`,

\[
\Delta\phi=\frac4{1-s}+\frac{4s}{(1-s)^2}
=\frac4{(1-s)^2},\qquad
K=-e^{-2\phi}\Delta\phi=-\frac1T.
\]

The checker verifies the entire polynomial identity in the numerator, rather
than a finite collection of numerical curvature values. Sectional curvature
on a surface is Gaussian curvature. Thus the curvature is uniformly strictly
negative for each fixed positive `T`, and is exactly `-1` at `T=1`.

For completeness, no additional covering theorem is needed. On a compact
Riemannian manifold the fixed-speed tangent sphere bundle is compact. The
geodesic vector field is smooth, and geodesic speed is conserved, so any
geodesic with a prescribed nonzero initial speed remains in one such compact
subset of `TM`. The local ODE extension theorem prevents a maximal solution
from stopping at a finite time while staying in this compact subset. Zero-speed
geodesics are constant. Hence all geodesics exist for all positive and negative
times. This establishes geodesic completeness for `g_tilde` and every `T*g_tilde`.
Alternatively, positive constant scaling leaves the Levi-Civita connection
unchanged, so it leaves the geodesics and their affine parameters unchanged.

At `T` tending to zero the metric degenerates only in the excluded limiting
case `T=0`; at `T` tending to infinity the negative curvature tends to zero.
The original claim fixes some `T>0`, and does not require constants uniform over
all intervals at once.

## 7. Local and global history fibers

On any sheet of a sufficiently small evenly covered disk `U`, the restriction
of `pi` is a diffeomorphism onto `U`, and `e` is injective. Thus `h` restricts to
an injective map on that sheet; its differential has rank two. Consequently
the constant-output history map is locally injective everywhere for `T>0`.

For `s` in `S`, its two distinct lifts `x_+`, `x_-` satisfy

\[
h(x_+)=e(s)=h(x_-),\qquad
\mathcal H_T(x_+)=\mathcal H_T(x_-).
\]

Conversely, equal attained histories imply equal constant values under `h`;
injectivity of `e` then implies equal projections under `pi`. Every projection
fiber has exactly two points. Hence **every attained history has exactly two
preimages**, for every fixed positive interval, and also for the entire real
time axis. The zero dynamics does not hide any additional state trajectories.

The history Gramian detects immersion (infinitesimal separation), while the
finite cover obstructs global injectivity. Completeness and negative curvature
on a surface do not remove the covering ambiguity. The smooth embedding into
dimension 17 makes the observation map a legitimate Euclidean-valued map.
