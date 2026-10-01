# Author turn 5: actual unmeasured holonomy and the limits of interpolation

**Final author attempt. The general source question remains unresolved after5/5 turns.** 2026-10-01.

This last route tests two possible ways to close the remaining gate: replace transverse dynamics by weights, or contract/glue the dynamics by interpolation. It supplies an actual normal unmeasured example within the positive product-carrier domain, and a precise failure of a natural interpolation formula. Neither settles the general branched case.

## 1. A compact transverse system with no full-support invariant measure

Let f:[0,1]->[0,1] be f(t)=t/(2-t). It is an increasing homeomorphism fixing0 and1. Put

    t_n=1/(1+2^n),  n in Z,
    K={0,1} union {t_n:n in Z}.

Then K is compact, f(t_n)=t_(n+1), and the only accumulation points of the orbit are0 and1. Every t_n is isolated in K.

There is no locally finite holonomy-invariant transverse measure of full support on K. Such a measure is finite on compact K. Invariance forces all singleton masses mu({t_n}) to have a common value m. If m>0, the measure of K is infinite; hence m=0. But an isolated t_n is a nonempty relatively open set, contradicting full support. In fact every finite invariant measure is supported on {0,1}. This distinguishes “some invariant measure” from a measure supporting the whole lamination.

## 2. Realization inside a fixed normal product carrier

Let S be a two-sided normal torus in a triangulated compact3-manifold, with an oriented normal product neighborhood as in turn2. Such an example exists in T^3: triangulate a product of a triangulated torus with a subdivided circle by standard prism tetrahedra and choose a torus level strictly between adjacent vertex levels. Each tetrahedron meets that level in a normal triangle or quadrilateral. Choose its small normal product neighborhood N.

Extend f to an increasing homeomorphism of J=[-1,2] that is the identity near the two outer endpoints. For instance extend monotonically across [-1,0] and [1,2]; smooth extensions are also available by extending the flow vector field -(log2)t(1-t) off [0,1] with a cutoff near the outer endpoints. Let Z^2 act on the transverse interval by f on the first generator and the identity on the second. Form the associated flat interval bundle over S and its closed sublamination

    Lambda=(R^2×K)/Z^2.

In this notation the Z^2 action includes deck translations on R^2. The ambient interval bundle is a product: an increasing interval homeomorphism fixing the endpoints is isotopic to the identity through (1-u)t+u f(t), and the second monodromy is the identity. Using this isotopy on the mapping-cylinder fundamental domain explicitly trivializes the bundle fiberwise. Transfer it by a fiber-preserving homeomorphism into N, with K lying strictly inside each interval fiber.

Over every simply connected normal disk of S, the flat bundle has a trivialization, and Lambda restricts to a product of that disk with K. Under the transfer into the normal product neighborhood, each slice is a graph over the normal disk and meets its boundary faces/edges in the corresponding normal arcs/points. Distinct slices are disjoint. Thus Lambda is a closed lamination normal to this fixed triangulation, fully carried by the unbranched torus. This construction uses actual product charts; it does not apply Brittenham's general normalization theorem to replace the lamination by a different one.

Its two fixed parameters give torus leaves. The orbit parameters give a noncompact leaf projecting as the corresponding covering of S, with nontrivial return dynamics f on the transverse set. The measure obstruction in Section1 is therefore genuine holonomy of a carried normal lamination, not just an arbitrary ordered set.

Two copies of Lambda satisfy turn2's hypotheses and can be stacked to give a closed normal output without any full-support transverse measure on either input. This verifies that the positive unbranched construction is genuinely beyond the measured-coordinate case. The example is not claimed essential, and no essentiality assertion is needed for Question7.4 as stated. It does not settle a general branched carrier.

## 3. A natural contraction of holonomy maps need not respect relations

The source remark asks whether a natural space of carried laminations, perhaps modulo monotone equivalence, could be star-like or contractible. One proposed mechanism is to interpolate holonomy maps toward a common model. Even in the simple interval-action setting, independently interpolating generators can leave the representation space.

Take the group Z^2 with generators a,b. One action on[0,1] sends a to F_0(t)=t^2 and b to G_0(t)=t^4; these commute because G_0=F_0 composed with F_0. A second action sends both generators to the identity. Coordinatewise midpoint interpolation gives

    F(t)=(t^2+t)/2,    G(t)=(t^4+t)/2.

Each is an increasing homeomorphism of[0,1], but they do not commute. At t=1/2,

    F(G(t))=369/2048,    G(F(t))=1617/8192,

and their difference is -141/8192. Therefore the midpoint tuple is not a Z^2 action. Pointwise convexity of individual interval homeomorphisms does not prove convexity of the space of holonomy representations with relations, let alone of a quotient space of laminations.

This is only a failed-formula control. The particular first action does have a path to the identity through representations: choose any path H_u from t^2 to t and send a to H_u, b to H_u composed with H_u. For a free group, arbitrary increasing generator maps have no relations to violate, and the coordinatewise contraction to the identity works on the marked representation space. None of these facts proves or disproves contractibility after imposing a particular branched carrier or an unspecified monotone-equivalence quotient.

## 4. Final gap and disposition

The tests show why both the weight and naive interpolation shortcuts are inadequate. The actual normal example confirms a useful positive unmeasured subclass; it does not provide coherent reconnection data at arbitrary switches. The compact certificate from turn4 remains conditional. We have not proved that matching quadrilateral types always admit such a certificate, that all reasonable reconnections give equivalent outputs, or that a chosen topology on the source space is contractible.

Nor has an intrinsic counterexample been constructed excluding every possible source-compatible operation for some normal pair. The torus intersection obstruction only excludes faithful unchanged unions; the split interval is an abstract, unrealized method countercontrol; and the interpolation failure only excludes one formula. None is promoted to a negative answer to Question7.4.

The five substantive author turns are now exhausted. Proposed original status: **unsolved,5/5**. Estimated completion30%. Freeze the exact scoped results and source boundaries for independent review; no additional proof-search turn, full-solution claim, or novelty assertion is warranted.
