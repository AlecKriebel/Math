# PR 38 / 2765 trace and geometry family

Frozen head: `980719c79e13ffbc3f5cfbf149c325ea2fb51df0`. Frozen snapshot manifest: `2c58f3aa5f73920fa62c7103648deee899db3a12f3f48c940576f99eff74dfe2`.

**Verdict: PASS_PARTIAL_SOURCE_SCOPE, retain unresolved/source-scope hold. No full solution or novel-result credit.**

## Independence and exact target

The complete literal source record was read and recorded first. Its embedded OPEN-TRIAGE was necessarily exposed and quarantined in `literal_source_record.json`. The reconstruction was sealed before RESULTS, old reviews, prior reports, SOURCE_AUDIT, or sibling interpretations. `independence_seal.json` pins the original reconstruction; it has not been rewritten after comparison. All sixteen original file hashes matched the frozen snapshot.

The full target is about every positive current with the same length as an arbitrary closed geodesic in every metric in the allowed family. A self-intersecting reference is allowed. The mathematical package expressly adopts a closed orientable genus >= 2 formulation for its first three propositions, and a separate complete finite-area cusped formulation for its fourth. Ordinary convex combination means a finite convex combination, but the source does not explicitly spell out finiteness. Neither finite checks nor the simple-reference case settles the arbitrary-reference target.

## Exact equivalence families

On a closed surface, the current fiber condition is `i(c,L_X)=i(gamma,L_X)` for all X. Taking rescaled weak limits of Liouville currents proves equality against every measured lamination. The equality is taken before the limit, so zero intersection values cause no division problem. This necessary condition is strictly weaker for pairs of curves than equality across every hyperbolic metric. It must not be reversed.

Equality against all closed-curve intersection tests determines a current; this is the full marked intersection spectrum of a current. Equality of metric length functions as X varies is a different question. In particular, Otal-type current separation cannot be applied by changing the indexing set from curves to metrics. A pair of metric twins already gives a nonzero signed difference invisible to all Liouville tests. Such a signed difference is not itself an admissible positive current.

Leininger `math/0302280v1` has closed orientable g > 1 scope and primitive unoriented curve conventions. Its Proposition 3.2 proves curve hyperbolic equivalence iff squared-trace equivalence by analytic continuation and representation-variety irreducibility. Its Section 5 uses current continuity to derive lamination tests. No trace function on arbitrary currents is supplied.

Jyothis `2309.14532v3`, submitted 2025-02-19, is the operative version used by the package. Section 2.2 defines simple marked length spectrum as intersections with simple curves. Section 5, Theorem 1.3 and Remark 1.4 give equal-simple-intersection, equal-self-intersection pairs without hyperbolic equivalence. The six-arc mechanism on pants is the operative proof. Version 3 requires a,c odd and b even; v1's family differs. An abstract/snippet suggesting strong simple equivalence is not a substitute for an all-continuous-maps proof; this audit does not promote that stronger claim. The package uses the weaker valid distinction.

## Formula and geometric countercontrols

The unchanged originals use reversal words `aababb`, `bbabaa`. At the actual level-two parabolics A=[[1,2],[0,1]], B=[[1,0],[2,1]], their matrices are [[97,22],[22,5]] and [[5,22],[22,97]], both trace 102; the wrong word `aaabbb` has trace 38. Thus they are hyperbolic examples, not a parabolic degeneracy. Their universal reversal identity in eight independent entries was replayed, and their cyclic and inverse cyclic classes differ.

The independently reconstructed Horowitz words `aaBab`, `aabaB` obey

`tr(A^2 B^-1 A B) = tr(A^2 B A B^-1) = x^2 y z - x z^2 - x y^2 + x`,

where x=tr A, y=tr B, z=tr AB. The six-parameter determinant-one symbolic residuals vanish identically. At the same A,B they have trace -30, giving positive length `2 acosh(15)`. This derivation validates the all-representation identity, rather than inferring it from integer samples. On a closed surface a pants/free-group retraction preserves nonconjugacy and allows all free-group representations to extend; an arbitrary subgroup inclusion alone would need more care about ambient conjugacy.

For a concrete control of the converse failure, Jyothis v3 Eq.8 with k=2,t=3 gives triples (17,12,3) and (19,8,5). They have total half twists 32 and the same source-defined self-intersection count 34 and three varying arc counts (17,32,18). Her other three pants arc types are constant through the family. The Eq.9 word matrices at A,B have traces 6270 and 6654. These two traces cannot yield equal squared-trace functions. Doubling the pants and folding gives a closed genus-two surface retraction, so these representations extend to that closed surface; Leininger's trace theorem then separates the metric length functions there. The arc and self-intersection formulas are geometric source claims verified from the operative proof, not proved merely by this arithmetic control.

The Gamma(2)/{+-I} model also has a direct geometric check: the ideal quadrilateral with vertices -1,0,1,infinity has A pairing the vertical sides and B pairing the two semicircles. The endpoint and midpoint Möbius maps check exactly. The standard ideal polygon side-pairing theorem gives a complete genus-zero surface with three vertex-orbit cusps and area 2pi. The original quotient/permutation computation agrees. Neither the quotient dimension calculation alone nor a finite group table proves singleton marked Teichmueller space; the ideal-pants/three-marked-points uniqueness argument supplies that step.

## Simple-reference support audit

The package's simple-reference theorem passes on closed oriented genus >= 2 surfaces, for a positive integral multiple of an essential simple curve alpha. Both separating and nonseparating cuts have components of positive genus. Thus an interior pants decomposition plus simple dual curves can relatively fill every cut component while staying disjoint from alpha. A genus-one one-boundary component is handled by two interior curves crossing once; higher-complexity components admit cuff-dual extensions. There is no pants-only exception in this closed-surface cut.

Positivity turns each zero intersection into an exclusion from support: a transverse crossing persists in an open geodesic box of positive measure. Complete geodesics avoiding the resulting arrangement cannot stay in a bounded disk lift. In a lifted compact annulus collar, a complete geodesic at bounded distance from the boundary axis has the axis's two ideal endpoints, hence equals it. Coincidence with a selected interior curve is excluded by a crossing dual. Passing through an arrangement vertex produces a transverse crossing unless the entire geodesic coincides with an edge. The only remaining support is the lift orbit of alpha. Invariance gives a common atomic weight, and one positive metric length fixes it. No diffuse or spiraling support evades the argument.

The argument stops for a filling self-intersecting reference: the required zero-intersection simple tests are unavailable. This is an actual gap, not an instruction to extend the simple-case proof by analogy.

## Punctured scope and original source

The primary K3 book matches the literal problem on printed pp.98–99; both were inspected visually. Printed p.84 admits finite-type oriented surfaces with punctures/boundary, and p.96 says complete hyperbolic metrics without adding finite area. The AIM URL in the embedded source triage is a four-page workshop report and cannot support the numbered question. The mathematical package already supplies the correct author-hosted book pointer.

Under complete finite-area cusp metrics and all Radon currents on the cusped thrice-punctured sphere, Teichmueller space is a singleton. The Liouville current is locally finite on geodesic charts and diffuse. The local intersection density has angular factor |sin(theta-phi)|. The exact integral over [0,pi)^2 is 2pi; in standard unoriented normalization `i(L,L)=(pi/2)Area=pi^2`. Hence the original AB geodesic of length `2 acosh(3)` can be matched by `c=(2 acosh(3)/pi^2)L`. A countable union of closed lift orbits has zero Liouville measure, so even countable atomic combinations cannot equal c.

This argument is conditional on the metric and current conventions. Complete funnels allow boundary-length parameters; complete alone does not yield the singleton family. Trin's published Proposition 2.2 proves that a compact-core current cannot represent all cusp metric curve lengths: boundary-winding curves have uniformly bounded intersection with any fixed core current, while their cusped metric lengths diverge. Her Example 2.1 also shows noncompact intersection continuity can fail. Her Section 3.1 establishes the finite oriented Liouville volume, without confusing it with normalized current length. BIPP Section 2 independently admits Liouville Radon currents for every discrete subgroup and defines the noncompact pairing. These operative facts confirm the package's conditional example and its convention exclusions.

## Replay, repairs, and exact remaining gap

`replay_and_corruption_receipts.json` records actual `/usr/bin/python3` runs with SymPy 1.14.0. Both original scripts were copied byte-for-byte into this private family, and saved stdout was byte-identical to the original 30/72 JSON receipts. Full stderr is saved, including five expected failures after actual code corruption. The mutants alter matrix data, a trace word, cusp permutations, an angular integrand, and a negative-control word. They reject at the expected substantive assertions. `geometry_controls.py` adds 25 exact controls with full JSON stdout; it certifies no arbitrary-current theorem.

Mandatory mathematical repair: **none found in the package's expressly scoped partial propositions**. Mandatory source/metadata repair: preserve a fresh audit note distinguishing the author-hosted numbered problem from the incorrect AIM workshop citation in the frozen embedded triage; do not overwrite the historical frozen record. Surface/current/metric scope must remain explicit. Promotion to a solved result must remain on hold.

Strongest valid package: closed-surface ML necessary condition, simple-reference rigidity, compact convex fiber (with closed carrier), plus the conditional non-atomic finite-area S_0,3 example. The exact full gap is exclusion or construction of non-finitely-supported positive currents in the fiber of an arbitrary self-intersecting closed reference geodesic, followed by the finite convex normalization conclusion. Compactness or Krein–Milman gives no closed-curve extreme-point classification. No full resolution or exhaustive priority claim follows from the bounded sources inspected here.

Original substantive turns remain 2/5. Audit adds zero. No outside contact, canonical/shared edit, Git-index change, commit, remote mutation, or merge was made. Root owns publication acceptance and any final remote/head pin.

Primary URLs are pinned with hashes and actual versions in `primary_source_receipts.json`; foreign raw files and rendered page images remain in ignored `tmp/` and are excluded from publication.
