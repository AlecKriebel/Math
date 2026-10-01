# Independent final partial review: Ghomi7000013

**Verdict: PASS for the corrected, explicitly separated partial results. Original intended-category problem remains unsolved after five substantive author turns.**

Reviewed on2026-10-01. Corrected `REFINED_RESULTS.md` SHA-256: `04f615c6ee601ad5062e7b4e1258b5c599e019d98c11a89ae70338688f417f70`. Corrected `FIVE_TURN_WIP_MANIFEST.json` SHA-256: `b3d2a85525b257ab77d0733605f3e7de93d131fcc8d23409566eb1180a01edfd`. All23 bound files match. The only mandatory review correction was to state the closed2-manifold hypotheses explicitly in the triangular rigidity theorem; the correction and its log are now frozen. All finite witness data are unchanged.

The reviewer did not contribute to the refined constructions. The parent-suggested sliding-cap mechanism is disclosed as an author contribution; this reviewer independently checked its implementation. This audit is not a historical novelty or human-peer-review certification.

## 1. Source boundary remains in force

The prior qualified audit of [Ghomi's survey](https://people.math.gatech.edu/~ghomi/Papers/op.pdf), p10, and [Alexandrov's cell-complex definition](https://arxiv.org/abs/math/0211286), Section3.1, remains applicable. Ghomi's displayed question does not specify every face/correspondence convention. A separate standard PL definition does not settle his unspoken intent. The simultaneous embeddedness, convex-maximal-face, nonflatness, and coherent-coorientation version remains unresolved here.

The final package carefully distinguishes three refined examples. They cannot be combined as if each supplied all missing hypotheses of the others. Equal cooriented area vectors are stronger than the source's potentially unoriented word parallel; incidence preservation is a separate requirement. The audit evaluates the precise matching actually supplied, rather than assuming all these notions equivalent.

## 2. Nine-face roof and dent

Both surfaces are boundaries of solids under a continuous positive piecewise-affine graph over the square and above the bottom plane. Thus each is an embedded closed sphere. Every listed face is convex and maximal, and the exact adjacent-normal cross products are nonzero. No flat subdivision edges are involved.

The roof/dent area-vector matching is correct: bottom and walls match themselves, and opposite roof triangles match. Exact signed-volume integration gives14/3 and10/3, proving noncongruence independently of the correspondence. However, the supplied cooriented matching takes a triangle's wall adjacency to a different wall, so it does not define the stronger coherent correspondence. The finite checker explicitly verifies this failure. It is therefore a valid counterexample to the cooriented normal-area multiset formulation, with its incidence limitation retained.

This statement concerns the specified cooriented matching. It should not be rephrased as a universal assertion about every possible matching under the weaker unoriented notion of parallel planes.

## 3. Edge-attached sliding cap

The geometry and area bookkeeping are correct. The two maximal faces that absorb the cap motion are a top notched polygon of area47 and a back stepped polygon of area10. They are simple polygons with no holes but are nonconvex. The other eight maximal faces are convex rectangles. All adjoining planes are nonparallel. The point/face lists in the two realizations give the same coherent incidence structure and equal corresponding oriented area vectors.

The stated ambient map has positive slopes4/3,1,1/2 in its nonconstant x regions and slope1 outside. It is a global orientation-preserving homeomorphism, fixes the base box as a set, and translates the original cap exactly into the shifted cap. This proves embeddedness and spherical topology without mistaking a finite incidence check for a geometric embedding proof.

The largest planar patch is uniquely the bottom rectangle, area48, centered at the origin. Direct box integration gives volume50 and centroids(0,1/10,14/25) and(1/25,1/10,14/25). Their squared distances809/2500 and813/2500 differ. Hence no global Euclidean isometry, including a reflection, can identify the surfaces. The two nonconvex maximal polygons are essential; triangulating them would change the stated no-flat-edge category.

## 4. Corrected nonflat triangular rigidity theorem

The corrected theorem explicitly assumes closed connected triangulated2-manifolds, two incident triangles per edge, connected face adjacency, and a coherent vertex/edge/face correspondence. Those hypotheses are needed. Before correction, the wording could include a single triangle, whose area and plane direction do not determine its shape.

For every edge in the corrected setting, the two incident nonparallel face planes determine its line direction. Parallel corresponding face planes imply parallel corresponding edges. In one triangular face write its independent edge vectors as u,v and its third as-u-v. The corresponding oriented vectors have coefficients a,b,c along these three directions. Closure forces a=b=c. Equal positive areas give a²=1. The fixed vertex correspondence makes the signed scale on a shared edge the same in either incident triangle, so connected face adjacency propagates one common value+1 or-1. Connected vertex adjacency then integrates the edge equalities to p'_v=lambda p_v+t for a single translation t. This is a congruence.

Neither convexity nor embeddedness is needed for that corrected conclusion. The result does not extend automatically to higher-sided convex polygons, since parallel quadrilaterals need not be homothetic. Adding diagonals introduces flat edges and invalidates the edge-direction argument. These limitations are correctly stated.

## 5. Convex quadrilateral immersed tori

The16-vertex,16-face abstract meshes are closed connected orientable2-manifolds with Euler characteristic0 and cyclic vertex links. Every quadrilateral is planar, simple, strictly convex and nondegenerate; every adjacent pair is nonflat. Corresponding faces have equal oriented area vectors and the incidence structures are identical.

The algebraic mechanism checks exactly. Consecutive original radii multiply to3, so the reciprocal-radius profile has edge increments-1/3 times the original radial increments. Its vertical increments are likewise-1/3 times the original. In p+tau p*, the meridian differences scale by1-tau/3, while each quadrilateral's radius sum scales by1+tau/3. Thus its full oriented area vector scales by1-tau²/9. For tau=±1/2 both multipliers are35/36 and all necessary radial and profile factors remain positive. An independent symbolic calculation verifies all three components for a general angular sector.

The model is explicitly self-intersecting. The two nonadjacent profile segments meet transversely at their interior parameter2/3, and this produces closed polygonal self-intersection rings in the four-angle mesh. Their vertex radii are47/18 and37/18. The term ring must not be interpreted as a circular cross-section: there are only four angular directions. Local immersion is consistent with this global crossing, since the profile itself is locally embedded and r stays positive; the angular polygon is star-shaped around the axis.

All pairwise vertex distances give squared diameters386/9 and338/9. A polygonal surface with convex faces is contained in the convex hull of its vertices, whose diameter equals the maximum vertex distance; since the vertices belong to the surface, these are its actual diameters. Different diameters prove noncongruence. Signed volumes vanish for these immersed examples; no bounded-solid argument or embeddedness is inferred from them.

## 6. The period obstruction is route-specific

For a straight meridian segment from(r_i,z_i) to(r_(i+1),z_(i+1)) in r>0,

integral dz/r² = Delta z_i/(r_i r_(i+1)),

including the constant-radius limiting case. A reciprocal-radius parallel dual requires the negative of this increment for its vertical coordinate. Closure therefore requires the sum of these edge integrals to vanish. For a simple closed meridian polygon, Green's theorem gives the signed integral of-2/r³ over its enclosed region, which is nonzero. Thus this particular reciprocal-radius dual route cannot close for a simple embedded rotational profile. The bow-tie profile avoids that condition through signed cancellation, at the cost of the expressly disclosed self-intersection.

This does not rule out all embedded coherent polygonal examples, all other dual constructions, or other torus parametrizations. The final gap statement does not overextend it.

## Validation and disposition

- All23 corrected frozen input hashes verified
- Independently authored checker passes **1,068 exact assertions**, including simple-polygon checks, planarity, oriented edge pairing, nonflatness, cyclic vertex links, all finite area data, volume/distance invariants, exact crossings, and symbolic area/period identities
- Author714-control refined witness and verification receipts replay byte-for-byte in an isolated copy
- Original triangulated example and its separate qualified review remain frozen as history
- No floating-point geometric tolerance or downloaded executable is used

The final author budget contains five substantive attempts with distinct outcomes. Review correction of the missing closed-surface hypothesis is validation, not another search turn. The original intended-category target remains unresolved; an unsolved5/5 partial-result draft is appropriate after the parent's publication gate. No unqualified claim that Ghomi's intended problem is solved is supported by this audit.
