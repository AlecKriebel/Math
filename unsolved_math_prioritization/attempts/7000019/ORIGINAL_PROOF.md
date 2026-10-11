# A small-width rigidity result for constant-area strips

**Status: scoped partial result; independent adversarial AI review passed.**
The original one-width problem remains unresolved in this attempt.
AI-assisted and unrefereed; historical priority is not established.

Target: **7000019 / AMR-069-0019**, Ghomi's Problem 4.3.

## 1. Exact scope

Ghomi's 2019 survey asks whether a closed surface whose strips of one fixed
width have constant area must be a sphere. The problem appears in the
section on convex surfaces. His own earlier 2017 formulation explicitly
assumes that the surface is the boundary of a convex body [1,2]. We
preserve that intended convex scope, rather than exploiting disconnected
surfaces. The distance is a positive constant h, not a freely variable
parameter tending to zero.

The following result has two explicit additional hypotheses: boundary
regularity and a comparison with the inradius.

**Theorem.** Let K be a compact convex body in R³ with nonempty interior,
and let S = ∂K be of class C^{2,α}, for some 0 < α < 1. Suppose a number
h > 0 has the property that

\[
 \operatorname{area}\{y\in S:t\le u\cdot y\le t+h\}=C
 \tag{1.1}
\]

for one constant C, whenever u is a unit vector and both bounding planes
intersect S. If

\[
 h<2r_{\rm in}(K),
 \tag{1.2}
\]

then K is a ball.

Here r_in is the largest radius of an inscribed Euclidean ball. In
particular, (1.2) is **not** merely h < diam(K), the assumption in the
original question. No conclusion for the remaining range is asserted.

## 2. Averaging a centered strip

Let a=h/2. Define the nonempty open inner parallel set

\[
 E=\{x\in\operatorname{int}K:
       \operatorname{dist}(x,S)>a\}.
\]

For x∈E, a slightly larger ball than B(x,a) lies in K. Hence for every
unit vector u, each of the two planes

\[
 u\cdot(y-x)=-a,\qquad u\cdot(y-x)=a
\]

meets S: the line through x in direction u leaves the bounded convex
body on both sides beyond these levels, and the corresponding sections
have boundary on S. Thus (1.1) gives

\[
 \int_S \mathbf1_{\{|u\cdot(y-x)|\le a\}}\,dA(y)=C
 \qquad(u\in S^2).
 \tag{2.1}
\]

For every nonzero z with |z|>a, rotation invariance of the ordinary area
measure dω on the unit sphere gives

\[
 \int_{S^2}\mathbf1_{\{|u\cdot z|\le a\}}\,d\omega(u)
 =\frac{4\pi a}{|z|}.
 \tag{2.2}
\]

Indeed, rotate z to the vertical axis. The allowed vertical coordinate
of u is the interval [-a/|z|,a/|z|], and spherical area in the coordinates
(longitude, vertical coordinate) is dφ ds. This also fixes the factor of
2: a is the half-width, while the original strip has width h=2a.

For x∈E, every y∈S has |y−x|>a. Integrating (2.1) over u, then applying
Tonelli's theorem and (2.2), yields

\[
 4\pi C
 =4\pi a\int_S\frac{dA(y)}{|x-y|}.

\]

Consequently the unnormalized Newtonian single-layer potential

\[
 U(x)=\int_S\frac{dA(y)}{|x-y|}
 \tag{2.3}
\]

satisfies

\[
 U(x)=\frac{C}{a}=\frac{2C}{h}\qquad(x\in E).
 \tag{2.4}
\]

All integrands are nonnegative and finite on compact subsets of the
interior, so there is no conditional-integrability interchange here.

## 3. From the potential to the ball

The function U is harmonic in int(K). To justify differentiating under
the integral locally, take a compact subset of int(K); it has a positive
distance from S, and every derivative of the Newton kernel is then
uniformly bounded over that subset times S. The surface has finite area.

The interior of a convex body is connected. Harmonic functions are real
analytic, so unique continuation applied to the nonempty open set E
and (2.4) shows that U is constant throughout int(K).

We now apply the established electrostatic rigidity theorem of Reichel
[3, Section 2, printed p. 622]: a bounded C^{2,α} domain with connected
exterior whose constant positive surface-charge density produces a
constant interior single-layer potential is a ball. The hypotheses hold
here: K has the stated boundary regularity; its exterior is connected by
convexity; the density in (2.3) is identically one. Reichel uses the kernel
1/(4π|x−y|), which differs only by a constant factor and does not change
the constancy hypothesis.

It follows that K is a ball, proving the theorem. Conversely, a radius-R
sphere has strip area 2πRh for every admissible 0<h<2R, consistent with
U=4πR and (2.4). □

## 4. What the original hypothesis does imply about width

A simple necessary condition helps identify the gap. Let w(u) be the
width of K in direction u, and A=area(S). Under the original assumptions
0<h<diam(K) and (1.1),

\[
 \min_{u\in S^2}w(u)>h.
 \tag{4.1}
\]

For otherwise continuity of w, connectedness of S², and
max_u w(u)=diam(K)>h give a direction with w(u)=h. The slab between the
two supporting planes then contains all of S, so C=A. In a direction
with w(u)>h, choose a strip strictly between the support planes. Both
planes meet S, while an open cap of S is left outside; its area is
positive. This gives C<A, a contradiction.

However, (4.1) alone does not imply (1.2). For example, the regular
tetrahedron with vertices

\[
 (1,1,1),\ (1,-1,-1),\ (-1,1,-1),\ (-1,-1,1)
\]

has inradius 1/sqrt(3) and minimum width 2. To see the latter, write the
absolute coordinates of a unit direction in descending order a≥b≥c≥0.
The six edge differences give w(u)=2(a+b), and
(a+b)²≥a²+b²+c²=1, with equality on a coordinate axis. Thus the choice
h=3/2 satisfies h<min w but h>2r_in. This tetrahedron is **not** claimed
to satisfy the constant-strip-area property. It only disproves the
purported geometric implication needed by a shortcut.

## 5. The projection-density obstacle

In a direction with a regular area pushforward density f_u(t),
differentiating the strip identity gives only

\[
 f_u(t+h)=f_u(t)
\]

on the interval where both endpoints are interior levels. A single
period does not force constancy. For example, the positive density
`1 + (1/2) cos(2πt/h)` on [0,3h] has the same integral h over every
contained interval of length h, yet is nonconstant. This is a
one-dimensional diagnostic, not a surface counterexample. The missing
all-direction compatibility remains a genuine geometric condition.

The averaging proof avoids this particular unsupported inference, but
requires E to contain an open set. If h≥2r_in, that set is empty. The
proof then establishes no constancy on any open interior region, and
analytic continuation has no starting set. Neither the strip condition
nor (4.1) has been shown here to rule out that range. Extension to
nonsmooth convex boundaries is also outside the stated partial theorem.

## 6. A scope warning about disconnected surfaces

If the short statement is interpreted to allow disconnected nonconvex
surfaces, it has an elementary negative example that does not answer the
intended convex question. Take the union of concentric spheres with
radii 2 and 1/2, and h=3. Its diameter is 4. For either normal direction,
a pair of h-separated planes meeting the union has lower offset in
[-2,-1]. Every such slab contains the entire inner sphere. Its area is
therefore `2π·2·3 + 4π·(1/2)² = 13π`, independently of the planes.
The union is not a single sphere and is not the boundary of a convex
body. Source [2] makes clear why it is excluded from the intended target.

## References and priority

1. M. Ghomi, *Open Problems in Geometry of Curves and Surfaces*, revised
   2 September 2019, Problem 4.3, printed p. 12.
   https://people.math.gatech.edu/~ghomi/Papers/op.pdf
2. M. Ghomi, *Converse of the Archimedean property of the sphere*,
   author-posted formulation, 9 October 2017. The surface is explicitly
   convex and the width is one fixed positive number.
   https://mathoverflow.net/questions/283109/converse-of-the-archimedean-property-of-the-sphere
3. W. Reichel, *Radial Symmetry for an Electrostatic, a Capillarity and
   some Fully Nonlinear Overdetermined Problems on Exterior Domains*,
   Z. Anal. Anwend. 15 (1996), 619–635, Section 2.
   https://doi.org/10.4171/ZAA/719
   https://ems.press/content/serial-article-files/34877
4. D.-S. Kim and Y. H. Kim, *Some characterizations of spheres and
   elliptic paraboloids II*, arXiv:1208.5361, Proposition 2 and Theorem 3.
   These concern cap-area functions for all sufficiently small heights,
   not the single prescribed height in the present problem.
   https://arxiv.org/abs/1208.5361

The averaging calculation is elementary and the rigidity theorem is
classical. No historical-priority claim is made for this restricted
consequence. No full resolution of Ghomi's fixed-width question is
claimed by this package.
