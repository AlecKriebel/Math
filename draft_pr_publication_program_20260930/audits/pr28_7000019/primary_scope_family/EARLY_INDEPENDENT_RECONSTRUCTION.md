# Independent source and mechanism reconstruction, before packet access

UTC checkpoint: 2026-10-01 22:54 UTC. Estimated completion of this source/scope audit: 20%; estimated completion of the original discovery goal is not measured by an audit. No original proof, prior review, original script, sibling family output, or publication packet has been opened at this checkpoint. The assignment's head and theorem labels are leads to test, not evidence.

## Literal sources and interpretation

Freshly fetched Ghomi PDF: *Open Problems in Geometry of Curves and Surfaces*, cover states last revised September 2, 2019. Printed p.12, section 4, problem 4.3, is titled “Surfaces with strips of constant area.” It asks about a closed surface in R^3 of diameter d with one constant h<d and constant area between any two planes at separation h which intersect the surface. The displayed statement does not explicitly say convex, parallel, smooth, or h>0; section 4's title supplies convex context, plane separation supplies the usual parallel-slab meaning, and the author's 2017 question explicitly supplies 0<h<d and convexity. These are interpretation/clarification, not words to silently insert into a verbatim 2019 statement.

Freshly fetched author MathOverflow question 283109: posted October 9, 2017, displayed edited October 17, 2017. The body explicitly fixes one 0<h<d, says parallel planes, requires both planes to intersect S, and defines a convex surface as the boundary of a compact convex set with interior points. It explicitly asks whether S must be a sphere. Comments raise narrow-direction/vacuity issues. The assertion in the 2017 body that the problem is open is historical source evidence, not a certificate of status in 2026.

Formal intended convex target: for every compact convex body K in R^3 with nonempty interior, let S=boundary K, d=diameter K, and surface measure sigma=H^2 restricted to S. If there exist h with 0<h<d and one C such that sigma({y in S : t<=u.y<=t+h})=C for every unit u and every t for which both endpoint planes meet S, does K have to be a Euclidean ball? No a priori smoothness, inradius restriction, strict convexity, or varying-height limit belongs to this target. Global constancy in both offset and orientation is part of the target. Success requires a proof on that entire class or a valid nonspherical counterexample on that class.

The weaker hypothesis “constant in t separately for each u, with C=C(u)” is a materially different problem. Tangent-cap constancy for every sufficiently small t is also different from a single fixed h.

## Independently reconstructed partial mechanism

Set a=h/2. Assume additionally boundary K is C^(2,alpha), 0<alpha<1, and a<r_in(K). Choose x with dist(x,S)>a. For every unit u, both planes u.y=u.x-a and u.y=u.x+a intersect S, because the ball of radius >a centered at x lies in K. Their slab area is C. Average over uniform u in S^2 and apply Tonelli. For each y, u.(y-x)/|y-x| is uniform on [-1,1], so

    average_u 1{|u.(y-x)|<=a} = min(1,a/|y-x|).

Since |x-y|>a for all y in S,

    C = a integral_S |x-y|^(-1) d sigma(y).

Thus U(x)=integral_S |x-y|^(-1) d sigma(y)=C/a on a nonempty open core. U is harmonic on the connected interior of K. Real analyticity/unique continuation of harmonic functions extends the constant to that entire interior. This use of unique continuation is local-to-global *inside K*; it supplies no continuation of the truncated kernel into the boundary layer before harmonicity has been established.

Reichel's 1996 paper DOI 10.4171/ZAA/719, printed p.622, section 2, assumes a bounded C^(2,alpha) domain with connected exterior. In dimension 3 its single-layer kernel is gamma(r)=1/(4*pi*r). A constant positive surface density inducing constant interior potential forces a ball. Normalization: choose rho=1, so Psi=U/(4*pi), and the exterior normal derivative jump is -1 after the interior derivative is zero. Convexity gives connected exterior. Thus Reichel applies to the reconstructed partial theorem.

I read the relevant electrostatic body pp.622-623, the general theorem's hypotheses and Theorem 1 pp.624-625, its complete proof pp.627-630, and the supporting corner-lemma appendix pp.631-633, independently of the packet. Case I uses g=1, f=0 and C^2 regularity up to the exterior boundary; the electrostatic section explains why C^(2,alpha) boundary supplies it. This is an imported published result, not a newly proved characterization.

## Boundary cases and exact remaining gap

A sphere of radius R has slab area 2*pi*R*h whenever both planes intersect it and 0<h<2R. Its constant interior U equals 4*pi*R, so a*U=2*pi*R*h; normalizations agree. The direction-averaged clipped kernel is continuous at r=a and equals 1 there; r<a is not a/r. The core is empty when a>=r_in, and at a=r_in it need not contain any open subset. Diameter does not control twice the inradius: the ellipsoid with semiaxes (3,1,1) has d=6 and 2r_in=2, so h=3 is permitted by the original target but excluded by this mechanism. This ellipsoid illustrates the uncovered parameter region; it is not claimed to satisfy the slab premise.

Exact remaining original-target gap: derive rigidity for fixed h satisfying 2*r_in<=h<diameter, and for the source target's nonsmooth convex bodies. Neither harmonic continuation nor Reichel by itself removes these hypotheses. If a route merely asserts that the truncated potential is harmonic everywhere inside, or that h<d guarantees a nonempty core, it transfers the central difficulty to an unsupported claim and is blocked.

## Adjacent literature read independently

Kim and Kim, arXiv:1208.5361v1, submitted August 27, 2012, *Some characterizations of spheres and elliptic paraboloids II*. Read full pp.1-10. Their Proposition 2 and Theorem 3 concern the area of tangent caps as a function of sufficiently small height t, independent of the contact point. Their proof on pp.5-7 takes t->0, extracts constant Gauss-Kronecker curvature from Lemma 8, then invokes a constant-curvature characterization. Those quantifiers do not prove fixed-h slab rigidity. Their Proposition 2 points back to a 2012 paper and classical Blaschke/Stamm references, which are relevant adjacent prior art. No worldwide novelty or absence conclusion follows from this bounded inspection.

No paper, immutable release, or DOI is justified by this reconstruction alone. The partial theorem may be valid but its novelty remains unclaimed and the full source target remains unresolved by this mechanism.
