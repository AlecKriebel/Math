# Turn 5: the essential-surface route and the exact product correction

**Final substantive author turn: scoped partials only. Original Problem 12.11 remains unsolved, 5/5.** This route seeks a lower bound that survives efficient shadow descriptions by replacing raw vertex/gleam counts with the non-product part of an essential-surface cut. The resulting conditional criterion is valid and includes the known alternating calculation when the canonical surfaces are supplied. The missing general shadow-to-surface/decomposition construction is not assumed.

## 1. The credited geometric theorem and its domain

Let M be a compact orientable 3-manifold with torus boundary whose interior is complete hyperbolic of finite volume. Let S be a properly embedded, two-sided orientable incompressible and boundary-incompressible surface, excluding sphere, disk and boundary-parallel components. Disconnected S is allowed. Let N be M cut open along S, with its natural parabolic boundary pattern, and let G=guts(N).

Agol–Storm–Thurston Theorem 9.1, together with the geodesic-boundary estimate of Miyamoto recorded in their Section 2 and the characteristic decomposition, gives

    vol(M) >= vol(G) >= v_oct (-chi(G)).                 (1)

Equivalently, the intermediate bound is one half of v_3 times the Gromov norm of the double of N. The graph-manifold/product pieces contribute no such norm, whereas doubling the hyperbolic guts doubles its volume. The geometric inequality is credited prior work. We do not replace the actual guts by a convenient subpolyhedron or by an arbitrary remainder after deleting some product patches.

This theorem bounds the actual M. If M is reconstructed from a boundary-marked shadow P, that reconstruction must identify the same exterior as the target knot. Hyperbolicity and the essential-surface conditions are hypotheses here, not consequences of a picture or a face count.

## 2. An exact conditional criterion with all product information

Suppose the actual characteristic submanifold Sigma of N has been identified, with frontier a union of annuli and tori. Its components are I-bundles over compact bases B_j of nonpositive Euler characteristic and Seifert-fibered components. Put

    beta(S)=sum_j (-chi(B_j)).                           (2)

There is no subtraction for the Seifert pieces because their Euler characteristic is zero.

**Proposition.** Under these hypotheses,

    -chi(G) = -chi(S)-beta(S),                           (3)

and hence

    vol(M) >= v_oct[-chi(S)-beta(S)].                    (4)

In particular, if a shadow construction certifies -chi(S)>=a(P) and certifies the upper bound beta(S)<=b(P) on the *entire actual characteristic I-bundle contribution*, then

    vol(M) >= v_oct max(0,a(P)-b(P)).                    (5)

### Proof

A compact orientable three-manifold with torus boundary has Euler characteristic zero, by the usual doubling identity. Restoring a product neighborhood of S to N gives

    chi(M)=chi(N)+chi(S)-2chi(S),

so chi(N)=chi(S). Since N=G union Sigma and their frontier consists of annuli and tori, inclusion-exclusion gives chi(N)=chi(G)+chi(Sigma). An I-bundle has the Euler characteristic of its base, and each Seifert component has Euler characteristic zero. Therefore chi(Sigma)=sum_j chi(B_j)=-beta(S), proving (3). Equation (4) follows from (1), and (5) follows from the stated one-sided estimates and nonnegativity of volume. QED.

The frontier hypothesis is substantive. If a proposed cellwise decomposition has frontier A of nonzero Euler characteristic, the general bookkeeping instead reads

    -chi(G) = -chi(S)+chi(Sigma)-chi(A).                  (6)

A collection of rectangles or disks cannot be silently treated as the annular frontier of the actual characteristic submanifold. Nor is a lower bound on beta enough: it gives an upper bound on the candidate deficit, in the wrong direction for (5). Finding some product regions does not prove an upper bound on all of them.

This is a reduction to exact topological certificates, not a completed combinatorial condition automatically read from general gleams. In particular, listing a surface in normal coordinates would not by itself certify incompressibility, boundary incompressibility, or completeness of the characteristic decomposition.

## 3. A rigorous obstruction to omitting the product term

Take a fixed finite-volume hyperbolic surface bundle over the circle with compact fiber F and chi(F)<0. Such bundles include the once-punctured-torus examples discussed by Futer–Kalfagianni–Purcell in *Cusp areas of Farey manifolds*, Sections 2 and 4; the figure-eight complement is a standard example. Only existence and finite volume are used here, not a numerical volume evaluation.

For any integer m>=1, let S_m consist of m distinct parallel fibers. Every component is two-sided and incompressible. One direct verification is that the infinite cyclic cover is F times the real line, so the fiber group injects. The fiber is also boundary-incompressible: a boundary-compressing disk would lift to this product, and projection to F would homotope its essential boundary arc into boundary(F), a contradiction. The same argument applies to the union of fibers.

Cutting the circle base at m points gives exactly m product intervals. Thus cutting M along S_m gives m copies of F times I. They are all characteristic I-bundle pieces; the guts are empty. Consequently

    -chi(S_m)=m[-chi(F)],
    beta(S_m)=m[-chi(F)],
    -chi(guts(M cut S_m))=0.                             (7)

The ambient manifold and its finite volume stay fixed. Therefore no positive constant times -chi(S), and no function tending to infinity with -chi(S), can be a universal volume lower bound for the allowed disconnected essential surfaces without controlling product pieces. Even a single connected fiber has negative Euler characteristic and empty guts. This last fact alone disproves the inference that negative Euler characteristic forces nonempty guts; the quantitative unbounded countercontrol uses the parallel union.

This is a countercontrol to the proposed surface-based method. It is not a counterexample to a condition that rules out parallel/product padding, and it is not a counterexample to Problem 12.11.

## 4. Alternating coverage when the canonical surface certificate is available

Let D be a prime alternating twist-reduced diagram of a hyperbolic link, with black and white checkerboard surfaces B and W. Let r_B and r_W count its non-bigon black and white regions. Lackenby's Theorem 5 gives the exact identities

    -chi(guts(M cut B))=r_W-2,
    -chi(guts(M cut W))=r_B-2.                            (8)

These are characteristic-submanifold computations, not replacements of guts by the whole cut manifold. They encode the essential product-region removal omitted by a raw checkerboard Euler characteristic.

The checkerboard surfaces can be one-sided. In that case use the frontier of a regular neighborhood as the two-sided orientable surface. As explained in Lackenby's Section 3, cutting along that frontier adds the neighborhood of the original checkerboard surface as an I-bundle component; removing the characteristic I-bundles leaves the same guts. Thus (8) does not acquire an extra factor of two.

Apply (1) separately to the two checkerboard certificates. They need not be disjoint from each other for this separate application. It gives

    vol(M) >= v_oct max(r_W-2,r_B-2)
            >= (v_oct/2)(r_B+r_W-4).                    (9)

The twist-reduced planar graph has r_B+r_W=t(D)+2, so

    vol(M) >= (v_oct/2)(t(D)-2).                         (10)

The factor 1/2 in the averaged estimate is essential: two inequalities for the same volume cannot be added without also doubling the left side. This reproduces the credited strengthened alternating volume estimate. It can be zero at twist number two, consistently with the bounded-volume family in turn 4.

Equations (8)–(10) demonstrate that the correct product-sensitive route genuinely covers the alternating class once its canonical checkerboard structure is present. However, obtaining a new condition for a more efficient general shadow requires a way to construct and verify the corresponding surfaces and complete product correction from that shadow. The existence of an unrelated alternating diagram or the name “guts” does not provide those data.

## 5. Final boundary after five substantive turns

The five routes now separate three types of information:

- A certified relative special-shadow filling presentation supplies a valid long-slope volume bound, but no universal alternating-preserving conversion to that form has been established.
- A marked canonical shadow has an exact gleam-saturation test for alternation and the known twist-number bound. This recovers the original baseline rather than the desired efficient-shadow extension.
- A general boundary-marked shadow could support the product-sensitive criterion (5), but the required essential surfaces and complete characteristic-product estimate have not been derived from its intrinsic decorated polyhedron.

The raw-count and sign-only countercontrols rule out particular shortcuts, not the existence of a normalized solution. The conditional volume criteria cannot be promoted to full source coverage while their certificate/coverage hypotheses are unproved. The final original-target status is therefore **unsolved after five substantive author turns**, subject to independent review of every retained partial.

No historical novelty is asserted. All deep hyperbolic, shadow-reconstruction and essential-surface results are credited to their primary sources. Finite arithmetic and permutation programs corroborate only the exact parts they explicitly test. There is no sixth proof search hidden in review, literature checks or packaging.
