# Vertex unfolding general clause counterexample audit

Edition note (9 October 2026 UTC): the original authored audit below is preserved in full and without textual alteration after its title. Its recommendation and review instructions describe the historical audit stage; the subsequent independent AI acceptance is recorded in ACCEPTANCE.md. References to checker scripts, test outputs, and finite incidence checks describe supplementary verification performed during that original audit. Those files are intentionally omitted from this theoretical edition; no code has been converted into prose as a replacement for a proof. The full coordinate, boundary, disk-face, and strict-angle argument below is the accepted mathematical basis. PROVENANCE.md records the edition boundary.

## Finding and scope

The general assertion in [TOPP Problem 42](https://topp.openproblem.net/p42), asking for a vertex unfolding of every closed polyhedron with disk faces, has a published negative answer. The acceptance basis supplied here is a full coordinate reconstruction and verification of the perturbed counterexample P′ in Abel, Demaine, and Demaine, *A Topologically Convex Vertex-Ununfoldable Polyhedron*, CCCG 2011, Theorem 4 and Figure 5. The argument below verifies the embedding, disk-face condition, incidence constraints, and obstruction to every permitted connection. It does not rely on the title, abstract, or a numerical unfolding search.

This is an audit of an existing result, with zero fresh proof-search approaches. The exact-coordinate exposition and deterministic checks are authored verification of the published witness, not a new counterexample or a claim of new mathematical discovery. Final acceptance requires the reviewer to read this argument.

The separate question for geometrically convex polyhedra is not resolved by this witness. Nor does it resolve the intermediate question for nonconvex polyhedra all of whose faces are convex. The witness has nonconvex faces and is geometrically nonconvex.

## Exact target and permitted operations

The TOPP target has a closed polyhedral surface: every original edge is incident to exactly two original faces. Each face is a polygonal disk. Cuts may use the original edges, with selected original vertex connections retained so the cut surface stays connected. The planar layout must contain isometric copies of the original faces with pairwise disjoint interiors. Vertex hinges can rotate continuously; the interior of the layout may be disconnected.

No triangulation, face subdivision, grid refinement, or cut through a face interior is allowed in this target. Apparent contacts between formerly unrelated points in the final drawing do not glue components of the cut surface together. Connectivity must come from retained original incidences. A continuous collision-free folding motion is not required.

The original Demaine–Eppstein–Erickson–Hart–O’Rourke paper, [author manuscript](https://jeffe.cs.illinois.edu/pubs/pdf/vunfold.pdf), pp. 2–4 and 13–14, supplies this model and separates the simplicial positive result from the nonsimplicial questions. Its p. 13 question about convex *faces* should not be conflated with TOPP's geometrically convex *polyhedra* subquestion.

## Published witness reconstructed explicitly

Use the two coordinate reflections

- rₓ(x,y,z) = (−x,y,z),
- rᵧ(x,y,z) = (x,−y,z),

and the half-turn s(x,y,z) = (y,x,−z).

Let A=(1,2,1), B=(1,−2,1), E=(2,1,−1), C′=(5,−3,3), and D′=(5,3,3). These agree with Figures 1 and 5 of the 2011 paper: C is moved to C′ and its symmetric outer corners move correspondingly, while the central vertices and prism-tip vertices remain fixed.

Define six faces in a class D. Each displayed list is a polygon's cyclic boundary order:

1. T₊ = [A, B, C′, D′].
2. T₋ = rₓ(T₊).
3. Q₊ = [(5,0,−3), D′, A, E, (−2,1,−1), (−1,2,1), (−5,3,3), (−5,0,−3)].
4. Q₋ = rᵧ(Q₊).
5. R₊ = [C′, D′, (5,0,−3)].
6. R₋ = rₓ(R₊).

The remaining six faces, class L, are the images under s of these six faces. The letters D and L encode the paper's two shading classes; the argument depends only on this partition.

There are four triangles, four quadrilaterals, and four octagons. This is the full original facet list, not a triangulation or a list of subfaces.

## Embedded closed surface and disk faces

A solid description removes any dependence on perspective drawings. Put

U = { (x,y,z) : |x| ≤ 5 and 2|y|−3 ≤ z ≤ (|x|+1)/2 },

V = s(U), and K = U ∪ V.

U is the union of the two convex polytopes

Uₑ = { (x,y,z) : |x| ≤ 5, z ≥ 2y−3, z ≥ −2y−3, z ≤ (e x+1)/2 }, e∈{−1,1}.

Both contain the origin strictly in their interiors. Their s-images do too. Each of these four bounded convex polytopes has a continuous positive radial function on the unit sphere. The radial function of K is their pointwise maximum, hence also continuous and positive. Consequently the radial map u↦R(u)u is a homeomorphism from the unit sphere to ∂K. In particular, ∂K is an embedded closed connected polyhedral surface without self-intersections or handles. K is star-shaped about the origin.

We now identify its facets rather than infer them from an Euler count. On the upper boundary of U with x≥0, the plane is z=(x+1)/2. This boundary is hidden by V for 0≤x<1, and exposed for 1≤x≤5. The lower inequality for U becomes |y|≤(x+7)/4. Thus the exposed polygon is exactly T₊. Reflection gives T₋. The artificial crease at x=0 in the upper boundary of U lies inside V and is absent from ∂K.

On the lower boundary of U with y≥0, z=2y−3. Here U gives |x|≤5 and 0≤y≤(|x|+7)/4. A point on that plane is strictly inside V exactly when y>1 and |x|+y<3, except for the usual equality boundaries. Removing this centrally attached trapezoidal notch leaves precisely Q₊. Reflection gives Q₋. Each is a simple eight-sided polygon, whose notch opens onto its outer boundary; no enclosed hole is created.

At x=±5, V is absent because every point of V has |x|≤3. The exposed caps are exactly R₊ and R₋. Applying s accounts for the other six boundary facets. These twelve planes are distinct. The description exhausts ∂K, so there are no omitted boundary patches and no intersections between interiors of distinct faces.

The caps are triangles and T₊,T₋ are convex quadrilaterals. Q₊,Q₋ are simple notched polygons; their s-images have the same property. Every face is therefore a closed disk. Direct boundary incidence gives 20 vertices and 30 edges, with each edge in exactly two faces. Every vertex link is a 3-cycle, agreeing with the sphere description. These checks are reproduced with integer arithmetic in `check_2011_witness.py` and its output `WITNESS_CHECK.json`. Every gate uses an explicit failure check that remains active under Python optimization. `test_witness_validator.py` verifies the unmodified input and three real coordinate/incidence/angle corruptions in both normal and optimized modes; all corruptions are rejected at their intended gates. `VALIDATOR_TESTS.json` records the eight outcomes. These finite checks support the authored argument and are not a formal proof certificate.

## All possible connections between the two face classes

The only vertices incident to both a D-face and an L-face are

{(±1,±2,1)} ∪ {(±2,±1,−1)},

with independent sign choices, for eight vertices in total. All other vertices and their incident faces belong to one class. The reflections rₓ,rᵧ and the map s act transitively on these eight mixed vertices, allowing interchange of the two classes.

At A the incident faces are exactly T₊, Q₊, and s(Q₊). The first two lie in D, and the last lies in L. The three incident edges lead to B, D′, and E. Hence every possible connection across the D/L partition has the local type of one of the two pairs at A:

- s(Q₊) with T₊;
- s(Q₊) with Q₊.

This also exhausts mixed original-edge incidences: an edge between the classes has mixed endpoints of these types. The finite incidence checks verify the full list, rather than merely checking the representative angles.

## Strict local angle obstruction

If two polygonal faces retain a common original vertex, their planar isometric images have their original interior angles at the common point. For sufficiently small radius, each polygon contains its complete interior angular sector there. If the two angles have sum greater than 2π, their angular interiors overlap in a set of positive angular measure, and the two polygons overlap in positive area. This holds for every relative rotation and every reflection. It does not assume that the two faces have adjacent positions in a cyclic hinge ordering.

At A the relevant edge vectors are

AB=(0,−4,0), AE=(1,−1,−2), AD′=(4,1,2).

In s(Q₊), the sector at A is reflex. The smaller angle between AB and AE has cosine

(AB·AE)/(|AB||AE|) = 4/(4√6) = 1/√6.

Call this smaller angle θ. Since 0<θ<π/2, the actual face angle is α=2π−θ>3π/2.

The face T₊ has a convex angle β′ between AB and AD′. Its cosine is

(AB·AD′)/(|AB||AD′|) = −4/(4√21) = −1/√21,

so β′>π/2.

The face Q₊ has a convex angle γ′ between AE and AD′. Its cosine is

(AE·AD′)/(|AE||AD′|) = −1/√126,

so γ′>π/2.

Thus both α+β′>2π and α+γ′>2π strictly. The reflex/convex choices follow directly from the cyclic polygons above; the deterministic check independently verifies them at every mixed vertex by exact projected orientation signs. Decimal angles are merely diagnostic and are not used in the proof.

It follows that no D-face and L-face can retain any common original vertex in a nonoverlapping planar arrangement. They cannot retain a common edge either: identifying a rigid edge forces identification of the coordinates of both endpoint closures and produces the same unavoidable near-endpoint overlap. The conclusion does not change if one formally removes the endpoint itself while retaining a nontrivial part of the edge.

Both face classes are nonempty. Every connected arrangement of all original faces using retained original incidences would need at least one connection between D and L. All such connections are impossible. Therefore ∂K has no vertex unfolding in the full target model. In fact the obstruction remains valid under the more permissive convention allowing arbitrary rearrangement of incident faces at a hinge.

This completes the negative answer to the general disk-face clause without any appeal to the 2018 result.

## Topological and geometric convexity are different here

The graph has a planar embedding on the sphere ∂K. The deterministic incidence audit verifies connectivity after all deletions of zero, one, or two vertices (211 cases), so it is 3-connected. By Steinitz's characterization, it is the graph of a convex polyhedron. This verifies the paper's use of “topologically convex.” None of this says that the present coordinates form a convex solid.

They do not. The points p=(5,0,−3) and q=(0,5,3) belong to K, but their midpoint m=(5/2,5/2,0) belongs to neither U nor V: U would require z≥2 and V would require z≤−2. Thus K is geometrically nonconvex. Its octagonal faces also have reflex angles. The convex-polyhedron and convex-face subquestions cannot be discharged with this example.

## The 2018 orthogonal counterexample

Garcia, Gutierrez, Ruiz, and Winslow, *Vertex Unfoldings of Orthogonal Polyhedra: Positive, Negative, and Inconclusive Results*, CCCG 2018, pp. 217–222, [author PDF](https://andrewwinslow.com/papers/vufortho-cccg18.pdf), Theorem 3, gives a further counterexample with simple faces. Its definitions restrict cuts to original edges and explicitly allow arbitrary hinge angles and rearrangement of cyclic face order. Its positive grid result introduces extra cut edges and addresses a different model.

The complete Theorem 3 proof, PDF pp. 2–3, and all of its Figures 2–6 were read and visually inspected. Its strategy selects a face path from a putt face to a base face avoiding the other putt, then excludes its three possible endings using a direct overlap and a bounded-reach chain. The chain's span is bounded above by 2√5+√8<8. The remaining geometric exclusion depends on the notch-placement bounds illustrated in Figures 5 and 6.

This audit does not use that terse figure-driven placement argument as an independent acceptance dependency. In particular, one must interpret the “all other locations” wording in the last paragraph locally to the part entering the notch, and the paragraph's final reference to the putt boundary appears to carry terminology over from the preceding case, which concerns an ell. These observations are not a claim that Theorem 3 is false. A separate, fully quantified orthogonal-witness audit would need to state and verify the entire facet geometry and the placement bounds. The fully explicit 2011 proof above already supplies the exact negative result needed here.

## Source and publication checks

- [TOPP Problem 42](https://topp.openproblem.net/p42) still displays an Open label and entry revisions from August 2002. Its two clauses have different dispositions: the unrestricted disk-face claim is false, while the geometric-convexity subquestion is not answered by this audit.
- The 2011 paper is listed in the [official CCCG 2011 proceedings](https://cccg.ca/proceedings/2011/), with a link to the [three-page paper](https://cccg.ca/proceedings/2011/papers/paper85.pdf). Its full proof and all Figures 1–5 were inspected. The [author bibliography](https://erikdemaine.org/papers/VertexUnunfoldable_CCCG2011/) retains a stale “to appear” field and explicitly has `unrefereed = 1`. This is a published conference result; this audit does not call it a journal publication or independently verified peer-reviewed result.
- The 2018 paper's proceedings identity and pages are confirmed by the [author's publication list](https://andrewwinslow.com/academic.html) and [official conference proceedings](https://cccg.ca/proceedings/2018/proceedings.pdf). The author PDF's first-page spelling “Gutierrrez” differs from the “Gutierrez” spelling in the publication list. The citation above follows the author list. All six author-PDF pages match the official proceedings text exactly after removal of the added printed page-number footer. The theorem and all Figures 2–6 were also visually checked in the official proceedings, printed pp. 218–219 (PDF pages 228–229). The 2011 author PDF is byte-identical to the official individual paper. These comparisons are recorded in `VERSION_COMPARISON.json`. No journal version is assumed.
- The 2002/2003 foundational paper's inspected author manuscript is fifteen pages. Its page numbering is used above; TOPP separately cites the seven-page SoCG 2002 proceedings version, and the 2011 bibliography also cites the 2003 book chapter. These are not silently treated as one pagination.

## Audit result

Recommend acceptance of the **prior negative resolution of the general original-edge disk-face clause**, credited to Abel–Demaine–Demaine (2011), Theorem 4. The counterexample construction and local obstruction have been checked at the full strength of the target. The 2018 orthogonal result supplies additional published context but is not needed for that acceptance.

Do not report a new proof discovery, a geometrically convex counterexample, a resolution of the convex-face subquestion, or an independent acceptance of every step of the 2018 orthogonal proof. Source files and source screenshots are reading evidence only and are not part of this authored artifact.
