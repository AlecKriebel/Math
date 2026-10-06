# Sealed independent reconstruction: potential/PDE family

Timestamp: 2026-10-01 22:50 UTC. Scope: target 7000019, original PR28 head `90a81313f3f65a7914fb6d5a9950fa087ea7467e`.

This file was composed before opening any original proof, review, verification script, sibling-family artifact, or repository history. Only the assigned task, directory names, and the primary sources below had been read. Subsequent corrections belong in a separate file; these bytes must not be edited.

## Literal target and precise partial claim

Ghomi's Problem 4.3 is on printed page 12 of *Open Problems in Geometry of Curves and Surfaces*, last revised September 2, 2019. Its stated object is a closed surface of diameter d and one prescribed strip separation h<d. The MathOverflow formulation explicitly specifies a convex surface as the boundary of a compact convex set with nonempty interior and specifies 0<h<d. Both bounding parallel planes must intersect the surface. The hypothesis concerns one common strip area, independent of both direction and position, for that one h. It is not an all-width hypothesis.

The candidate partial statement I will audit is:

Let K be a compact convex body in R^3, let S=boundary K be C^{2,alpha} for some 0<alpha<1, and let r_in(K) be its inradius. Suppose 0<h<2r_in(K) and that H^2(S intersect {t<=u dot y<=t+h})=C for every unit u and every t for which both bounding planes meet S. Then K is a Euclidean ball. This is strictly restricted relative to the target by both the regularity and h<2r_in condition. Since 2r_in<=diam(K), the condition implies the target's diameter inequality. No resolution of h>=2r_in or nonsmooth convex surfaces follows from this argument.

## Universal averaging mechanism (independent derivation)

Write a=h/2, D=int K, sigma=H^2 restricted to S, and

E_a={x in D: dist(x,S)>a}.

For a compact convex body, S has finite area: its boundary is locally a Lipschitz graph, with a finite compact cover. For the smooth partial claim this also follows immediately from a finite smooth atlas. Thus sigma is a finite positive Borel measure. Compactness of K and continuity of distance supply an incenter attaining the maximal interior distance to S; a<r_in gives an incenter c with dist(c,S)>a. Distance is 1-Lipschitz, so a ball of radius smaller than r_in-a around c lies in E_a. In particular E_a is a nonempty open set. Equality a=r_in does not suffice: for a sphere E_a is empty.

For any x in E_a, some ball B(x,a+epsilon) lies in D. Hence for every unit u both x dot u-a and x dot u+a lie strictly between K's minimum and maximum u-coordinates. Each corresponding plane cuts the surface: one may use the connected line segment through x in directions +/-u and its endpoints on S. Thus the original strip hypothesis applies to the centered strip {y: |u dot(y-x)|<=a}, with value C for every u. Convexity is used to make the domain and these slicing statements unambiguous; the ball condition by itself gives the plane intersections.

For a fixed vector z with length r>a, rotate z onto the polar axis of S^2. The spherical area element is sin(theta) dtheta dphi. The coordinate s=cos(theta) has measure 2pi ds on [-1,1]. Therefore

integral over S^2 of 1_{|u dot z|<=a} dH^2(u)
=2pi integral from -a/r to a/r ds=4pi a/r.

The normalized directional probability is a/r. More generally for r>0 it is min(1,a/r), and for z=0 it is 1. This saturated kernel is the actual formula away from the inner core and explains why blindly retaining a/r when r<a fails.

The joint integrand 1_{|u dot(y-x)|<=a} is Borel and nonnegative. Tonelli applies to H^2 on S^2 times finite sigma on S, with no signed cancellation and no differentiation of moving strip edges. Every y in S is at distance greater than a from x in E_a. Consequently

4pi C
= integral over S of integral over S^2 1_{|u dot(y-x)|<=a} dH^2(u) dsigma(y)
=4pi a integral over S 1/|x-y| dsigma(y).

For the unnormalized Newtonian single layer P(x)=integral_S |x-y|^{-1} dsigma(y), this gives P(x)=C/a=2C/h on E_a. For Reichel's normalization U=P/(4pi), it gives U=C/(2pi h). Either consistent normalization is permissible, but mixing them loses a factor 4pi. The factor 2 is tied to h being the full separation rather than a half-width. For a radius-R sphere the strip area is 2pi R h, and P=4pi R inside, confirming the constants.

This identity is a universal theorem, not numerical evidence. It does not require C^{2,alpha}; finite surface measure and a nonempty inner core are enough for the averaging identity. It is specific to dimension 3: on a circle the band probability is (2/pi)arcsin(a/r), not a/r; in general dimension the marginal density is proportional to (1-s^2)^{(n-3)/2}.

## Interior continuation

For each compact subset L of D, its distance to S is positive. The Newton kernel and all derivatives are uniformly bounded on L times S. Differentiation under the finite integral is justified, so P is harmonic on D. Harmonic functions are real analytic. Because D is connected (indeed convex), P-2C/h vanishing on nonempty open E_a implies it vanishes everywhere in D. This is an identity theorem, not a global mean-value argument and not a conclusion from one point. A core reduced to one point is insufficient for this proof. No continuation across S is claimed.

## Exact external rigidity requirements and a separate PDE route

Primary source: Wolfgang Reichel, *Radial Symmetry for an Electrostatic, a Capillarity and some Fully Nonlinear Overdetermined Problems on Exterior Domains*, ZAA 15 (1996), 619-635, DOI 10.4171/ZAA/719. The electrostatic application is in Section 2, printed page 622. Section 4 gives its overdetermined exterior theorem and moving-plane proof, printed pages 624-633; the relevant case is locally uniformly elliptic case (I), g=1, f=0. I have read the full relevant argument in the primary PDF, including the critical-plane comparison, internal-tangency and orthogonal-corner contradictions, the topological symmetry step, and Appendix 1's corner-lemma hypotheses. OCR obscures alpha/closure symbols and the kernel formula; I will inspect the PDF pixels/local text before accepting the exact regularity notation.

The exact usable content is that a bounded sufficiently smooth domain G with connected exterior, bearing a constant nonzero positive density on its entire boundary, cannot have its single layer constant throughout G unless G is a ball. The uniform density and whole-domain constancy are essential. I must verify that the PR applies this precise statement with G=D, density=1, and the R^3 kernel.

One can check every hypothesis independently by reducing to Reichel's exterior PDE theorem. With U=P/(4pi), continuity of the single layer gives the constant boundary trace b>0. For a C^{2,alpha} boundary, the layer-potential jump formula in the outward normal nu of K is

partial_nu U|exterior - partial_nu U|interior = -1.

The interior derivative vanishes because U is constant in D. Thus exterior partial_nu U=-1. The unnormalized formula is -4pi, not -1. C^{2,alpha} boundary and constant Dirichlet trace allow exterior harmonic boundary regularity through second derivatives; the proof must not demand C^2 traces merely from an arbitrary continuous density. Here the density is constant and the Dirichlet trace already constant.

The exterior Omega=R^3 minus K is connected: fix an interior center c and a containing ball; every exterior point can be moved radially away from c to the containing sphere without crossing K, and points on that sphere can be connected. Positivity of U follows from its positive kernel/density. U tends uniformly to 0 at infinity, by U(x)<=sigma(S)/(4pi(|x|-max|y|)). On truncated exterior domains the maximum principle, then a limit as the outer radius tends to infinity, gives U<=b. Equality at an interior exterior point forces constancy by the strong maximum principle, contradicting decay and b>0. Thus 0<U<b on Omega.

These facts put U in Reichel's case (I) with Laplacian, f=0, constant b Dirichlet trace, constant negative Neumann trace relative to the body's outward normal, and decay to 0. Case (I)'s moving-plane proof then forces radial symmetry and a ball. No sign-sensitive use of an exterior-domain normal pointing into K should be made without flipping the Neumann sign.

The primary proof uses a reduced exterior half-space so that reflections remain in Omega. The comparison w=U(reflection)-U is harmonic, has nonnegative boundary values, and vanishes at infinity. Its critical position either has internal tangency, where equal constant normal derivatives contradict Hopf's strict derivative, or an orthogonal boundary intersection, where constant Dirichlet/Neumann traces force a second-order zero and violate the corner lemma. Connectedness of Omega then propagates the matching component across the critical plane. Repeating in all directions gives a ball. For the Laplacian the corner lemma's mixed-coefficient bound is automatic because the coefficient matrix is the identity. This mechanism is independently checkable and does not assume the desired radial symmetry.

## Planned adversarial controls and exact gaps

1. Normalize the orientation distribution and compare the full-width and half-width versions against a sphere. Deliberate factors 2, 4pi, and a/r outside the core must be rejected.
2. Prove the min(1,a/r) formula also for finite atomic measures, to test Tonelli without relying on smoothness, then test a nonconstant shell density to show constant-density rigidity cannot be omitted.
3. Test a smooth ellipsoid with h<2r_in. Its interior uniform layer should vary, so it must fail the common-strip hypothesis. This only falsifies implementation failures; finite quadrature never verifies the universal theorem.
4. Test an ellipsoid with 2r_in<h<diam. The inner core is empty and the route gives no conclusion. Such a body is a boundary control, not a counterexample to the original question.
5. Verify core at strict and equality cases exactly. Constant harmonic value at one point supplies no continuation (e.g. harmonic x_1).
6. Verify boundary trace, jump signs, and the layer's exterior decay using the exact radius-R sphere formulas U=R inside and U=R^2/r outside, whose outward derivative at r=R is -1.
7. Check all frozen original files and the trial-budget ledger; any claim that one quadrature or source-token check proves the analytic chain is unacceptable.

Strongest independent conclusion at sealing: the averaging-to-interior-constancy argument is proved under h<2r_in. The smooth rigidity conclusion is supported by the precise applicable primary theorem and independent PDE hypothesis reconstruction, pending pixel-level regularity verification and comparison with the frozen PR. The full Ghomi question remains untouched in the complementary width regime and for nonsmooth surfaces. Route status: viable restricted theorem; blocked as a full-target route at the empty-core barrier without a materially new mechanism.

Discovery-goal completion estimate: 35% toward a complete audit; 0% evidence of a solution of the full target.

Sources: [Ghomi PDF](https://people.math.gatech.edu/~ghomi/Papers/op.pdf); [MathOverflow formulation](https://mathoverflow.net/questions/283109/converse-of-the-archimedean-property-of-the-sphere); [Reichel primary PDF](https://ems.press/content/serial-article-files/34877).
