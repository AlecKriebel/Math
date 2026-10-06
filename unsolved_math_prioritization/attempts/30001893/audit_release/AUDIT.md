# Independent adversarial audit: convex partition dimensions

Problem 30001893, OWR-11136-024. Audit date: 2026-10-05.

## Verdict

**PASS, PARTIAL RESULT ONLY. Five substantive approaches out of five are retained. The full source problem is not solved.** No blocking mathematical error was found in the frozen manuscript's stated range n >= 4. The accepted global conclusion is

    4n - 5 <= dim C(R^3,n) <= 3 binomial(n,2).

The regular, pointed-central, and cylindrical statements are valid with their stated restrictions. The six-equation, five-cell example has local relevant dimension 15; it does not prove a general upper bound. Attribution to inspected 2015 sources is appropriate. Neither novelty nor current worldwide openness is certified.

This audit is separate from the author freeze. No author file was modified, no helper was used, and no remote write was performed. The exact binding is in BINDING.json. The author ZIP is 23,424 bytes with SHA-256 966970b14c7350553393b14ca378ad764d8ae2cd38b47cb00556fd6c51bf4e81.

## 1. Primary-source and target binding

The original [2011 Oberwolfach report](https://publications.mfo.de/bitstream/handle/mfo/3259/OWR_2011_44.pdf?isAllowed=y&sequence=1), printed p.2539, PDF page 81, was independently rendered from the bound PDF and visually inspected. Its Problem 2 asks for the maximal realization-space dimension for n > 3 convex pieces in three-space. The printed discussion really uses 4n-1 for regular three-dimensional diagrams. It also gives planar counts 4n-1 and 3n-1. These are genuine printed statements, not an extraction artifact.

The [2015 Leon-Ziegler preprint](https://arxiv.org/pdf/1511.02904), p.21, was independently rendered and inspected. Theorem 6.2 states regular dimension (d+1)(n-1)-1 for d,n >= 2. Conjecture 6.3 states the full three-dimensional 4n-5 value. The planar theorem gives 4n-7 for n >= 3. The manuscript correctly distinguishes these statements from the original wording. No official erratum was inspected; “corrected” here describes the mathematically justified later count, not a verified publication of an erratum.

Definitions, the hyperplane-coordinate structure, and the metric were checked in the preprint; Proposition 5.4 and the Section 6.3 discussion were checked in the [2015 dissertation](https://refubium.fu-berlin.de/bitstream/fub188/829/1/Thesis.pdf). These sources support the claimed conventions, gauges, and restrictions. The 2018 version of record remains uninspected. No statement is attributed to its complete text.

The exact live catalog statement, its review, and upstream raw records remain uninspected. Descriptor-observed hashes are not independently recomputed source hashes. This audit does not certify the task's rank or its entire historical catalog trail. The numerical ID and OWR identifier are the supplied task binding; the mathematical question is independently bound to the cited original page. The brief original question does not spell out every boundary or topological convention: the manuscript explicitly uses the standard formalization in the inspected 2015 sources. If the unavailable catalog imposes different conventions, those would require a new comparison. An audit of the authored mathematics does not remove these source limitations.

## 2. Definitions, dimension, and topology

The manuscript uses labeled, nonempty, open, convex regions with pairwise disjoint interiors and closure coverage. Because regions are open, “disjoint interiors” is simply disjointness. Nonempty open regions are full-dimensional. The proof never imports empty cells from the compactification or treats independently assigned boundary labels as parameters. No quotient by Euclidean or affine transformations is taken.

Spherical symmetric-difference volume is a genuine metric on these open convex regions: distinct regular-open convex sets cannot differ only on a null boundary set. Dimension is semialgebraic dimension of canonical finite realization pieces, not a claim about every possible Hausdorff metric. The manuscript's local charts are semialgebraic and have the usual topological dimension.

An explicit continuity detail supports the graph-coordinate argument. For a sequence of partitions converging in the spherical metric with an adjacency retained at the limit, take a convergent subsequence of its normalized separating coefficients. The limiting inequality separates the limiting regions, since otherwise an open ball strictly on the wrong side would yield a positive symmetric-difference volume. The retained common facet forces the unique oriented limiting support plane. Thus the inverse support-coordinate map is continuous within a fixed adjacency piece. Conversely, convergence of finitely many coefficients gives convergence of region indicators away from limiting hyperplanes; dominated convergence on the sphere proves metric continuity. This uses genuine nonempty regions and cannot be extended indiscriminately to disappearing cells.

Semialgebraicity can also be checked directly: nonemptiness, closure coverage, equality of halfspace-defined regions, and the existence of a two-dimensional common facet are first-order real conditions. Quantifier elimination and finite subdivision into combinatorial pieces justify the dimension comparisons. No dimension conclusion is being inferred from an arbitrary continuous surjection, which would be invalid.

## 3. Approach-by-approach adjudication

### Approach 1: supporting planes and the global upper bound

PASS. Strong signs on the two open sets follow from ordinary weak affine separation: a nonconstant affine function cannot vanish at an interior point of a full-dimensional set contained in one weak halfspace. This does not require positive distance between closures.

The coverage argument proves that each closed region equals the intersection of the chosen weak halfspaces. A full-dimensional closed convex set is the closure of its interior, so passing back to strict inequalities recovers precisely the original open region. No face-to-face assumption has slipped into this step.

Every facet contains an open patch abutting at least one other region. A finite subdivision of the facet by the other polyhedra supplies such a patch, including at non-face-to-face configurations. Adjacent support planes recover all facets and hence the entire region. Nonadjacent separators are consequently auxiliary variables and are removed by the canonical adjacency projection. At most binomial(n,2) normalized planes, with three parameters each, establishes the bound. Nonpointed, nonessential, and degenerate partitions remain included, provided the regions are nonempty and full-dimensional as required.

Dependency: finite canonical semialgebraic pieces and facet recovery. The proof supplies them; the continuity argument above makes the topology identification explicit. This is a coarse quadratic bound. Compatibility codimension sufficient for 4n-5 is still unknown in this work.

### Approach 2: regular diagrams and exact fibers

PASS. The common affine function has four coefficients. Subtracting it and normalizing the remaining coefficient vector removes five representation redundancies, not five physical transformations of the partition. Positive scaling matters; a negative scale reverses maximization and is not the same gauge.

The upper bound is valid for all regular diagrams, including diagrams with larger fibers. Equality uses an open family with an exact fiber proof. At a simple vertex the new slope is a strict interior convex combination of the four old slopes. Therefore the positive homogeneous maximum-minus-average has a positive minimum on the unit sphere. Its small sublevel region is a bounded tetrahedron. The insertion preserves finite preselected facet witnesses, creates four new simple vertices, and can be repeated for every n >= 4.

An adjacency witness is chosen where its two functions tie and strictly dominate all others. Its supporting plane and a nearby witness vary continuously under small coefficient perturbations. Finite witnesses give the required open coefficient neighborhood; mere visibility at one exceptional point would not suffice.

For two representations of the same partition, every retained adjacent difference is a positive scalar multiple of the same support equation. On a triangle with two independent coefficient differences, the scalar factors coincide. The base K4 and the insertion triangles propagate a single scalar throughout the connected retained graph. Every fiber in the stated neighborhood is exactly common-affine-plus-positive-scale. Fixing the first function and one nonzero x-coefficient gives an open 4n-5 chart with injective semialgebraic image. This is a proof of dimension, not parameter counting alone.

Independent finite support: the five-cell coefficient system has a five-dimensional infinitesimal fiber when every adjacent equation is enforced, computed by exact rank 25 in 30 unknowns. This checks that example; the preceding analytic triangle argument, not that rank computation, proves the all-n claim.

Range: the frozen constructive proof uses n >= 4. The cited theorem has n >= 2. For n=2 the oriented affine plane has dimension 3. For n=3, the functions 0,x,y give an open K3 chart; the same single-triangle fiber argument yields 7. For n=1 the space is a point and 4n-5 is not the regular dimension. There is no unnoticed n=1 extension.

### Approach 3: pointed central fans

PASS. Pointedness is essential. The section of a full-dimensional pointed closed polyhedral cone is a spherical polygon contained in an open hemisphere, hence a disk, with short, unambiguous geodesic edges. Insert T-junctions, then remove degree-two straight subdivisions. A genuine degree-two bend would make one of its two neighboring regions nonconvex. The graph is a connected cellular spherical graph with minimum degree three. Euler and the degree sum give V <= 2n-4 and E <= 3n-6. This also bounds the finitely many possible combinatorial types.

A fixed type is determined by its ray directions; no edge-plane degrees of freedom are omitted. The upper bound at fixed apex is 2V <= 4n-8. The lower family starts with a simple polytope with n facets, obtained by repeated sufficiently small vertex truncations. Its spherical graph is trivalent. Strict spherical convexity, open-hemisphere containment, nonzero incident angles, and positive separation of disjoint compact edge pairs persist under independent small ray perturbations. The resulting embedded graph has the same disk faces and covers the sphere. Each labeled partition recovers its rays, so this is an injective open ray chart.

The common intersection of all closed cones is the apex. If a nonzero displacement belonged to all of them, completeness would put its negative in one cone, violating pointedness. Thus moving the apex really adds three parameters. The exact dimensions 4n-8 and 4n-5 are justified for n >= 4.

Range and exclusions: fewer than four such pointed full-dimensional cones cannot cover three-space. Each spherical polygon needs at least three vertices, whereas the Euler bound for n <= 3 is incompatible with that. Without pointedness, hemispheres, digons, lineality, and nonunique apex data invalidate this proof. The manuscript does not extend it there. A general affine partition with several finite vertices is outside this class.

### Approach 4: cylinders and nonregularity

PASS. The finite trivalent planar construction begins with three sectors of angles less than pi. A small triangle cuts off a vertex in each surrounding cell, retaining convexity and adding two finite vertices and one region. Repetition gives V=2n-5 and three unbounded rays. The strict-angle and separated-direction margins make the proposed local chart open, not merely a set of formal vertex assignments. Finite edges are determined by their endpoints; ray directions contribute three further parameters. Thus the planar family has dimension 2V+3=4n-7.

Extrusion with kernel span(a,b,1) adds two direction parameters. A bounded planar cell ensures its cylinder's lineality is exactly this line, so the partition recovers a,b. Intersecting with z=0 recovers the planar partition. Translation along the extrusion line leaves it unchanged and is correctly not counted. This proves a 4n-5-dimensional family. These nonessential partitions are allowed by the target conventions.

The explicit four-cell example is valid. Its pairwise opposing boundary inequalities give disjointness. Independent exact Fourier-Motzkin elimination exhausted all 64 strict sign patterns of the six boundary lines: 19 are feasible and each belongs to exactly one displayed region. This proves coverage off the lines; closure coverage follows from density. The four witnesses establish nonempty open cells.

The three outer adjacency lines have coefficient determinant -1. Three affine-function differences around a cycle sum to zero, so nonzero scalar multiples of three independent line equations cannot represent them. This establishes nonregularity. The condition persists locally. Restriction to z=0 rules out a regular representation of the extrusion. Further sufficiently local triangle insertions can preserve open portions of all three outer adjacencies and their support lines, retaining the obstruction for larger n.

This construction reaches but does not exceed the conjectured dimension. It supplies no density or exhaustiveness claim about general partitions.

### Approach 5: exact incidence rank and local dimension

PASS. The listed four vertices are exactly the vertices of the bounded tetrahedral cell, each a four-function tie. Their outgoing rays are correctly charted. Every one of the six exterior faces has a finite edge and the two indicated rays. Coplanarity is the displayed determinant equation.

Independent symbolic expansion and differentiation reproduce the entire 6-by-20 Jacobian. The all-ones row relation holds. The first five rows, with columns 0,1,4,5,6 in zero-based indexing, have determinant +1. Thus rank is exactly five. The author correctly does not infer dimension merely from rank deficiency.

The author's local upper bound follows from the implicit-function theorem applied to the five independent equations. The lower bound follows from the continuous injective gauge-fixed 15-parameter regular family through this point. For every neighborhood of the example, continuity supplies an open parameter neighborhood within it, still of dimension 15. Unique vertex/ray reconstruction prevents a hidden fiber. Hence the relevant local dimension is exactly 15.

An additional independent polynomial certificate makes the dependency explicit. Write R for the 3-by-4 matrix with ray columns r_i and set

    alpha_i = (-1)^i det(R with column i deleted),
    F_ij = det(v_j-v_i, r_i, r_j),   i < j.

Then sum_i alpha_i r_i = 0 and, identically in all coordinates,

    sum_(i<j) alpha_i alpha_j F_ij = 0.

To verify the second identity, collect the coefficient of v_i in the scalar triple products. It is -alpha_i r_i crossed with sum_j alpha_j r_j, hence zero. At the frozen example all four alpha_i are -1. Their products remain nonzero nearby, so the sixth equation follows exactly from the first five there. Together with the nonzero minor, the full incidence zero set is locally a smooth 15-dimensional manifold. The valid partition subset has dimension 15 by the author's regular-family lower argument. The independent program verifies this identity by full sparse-polynomial expansion, not numerical sampling.

This identity is confined to this four-ray example. It is not an all-types rank theorem. In a general chart, one needs sufficiently large nonzero minors over every relevant stratum or a separate bound for exceptional rank strata; auxiliary fibers must also be removed. Those are exactly the unresolved dependencies stated in the frozen manuscript.

## 4. Adversarial tests and what they do not establish

All four documented author commands were replayed against the untouched release. Ordinary and optimized outputs match in both modes. The scientific output matches the frozen EXACT_RESULTS.json byte-for-byte. The freeze-enabled author run has 2,636 checks/guards and rejects 20 controls, including eight file/manifest mutations. The unextended scientific run has 2,540 checks/guards and 12 rejected controls.

The separate independent program does not import author code. It uses exact rational arithmetic, sparse symbolic differentiation, permutation determinants, strict-linear feasibility over every sign chamber, and the global polynomial identity above. Normal and optimized outputs match. It rejects 22 controls spanning false ranks, wrong minors, invalid geometry, gauge omissions, range errors, source-count substitution, binding corruption, and claim inflation. Scope guards detect prohibited claims; they are not mathematical proofs that a broader theorem is false.

Finite tests, hash matches, and normal/-O parity do not prove the general upper bound. Universal conclusions accepted here depend on the audited analytic arguments. A “six equations therefore codimension six” claim is decisively false in the exhibited example. A “rank five at one point therefore dimension fifteen” argument would still be invalid without the additional reasoning supplied above.

## 5. Findings, dependencies, and release limits

No failed retained mathematical statement requires changing the original freeze. The following qualifications must remain attached to any use of the audit:

1. The original printed 4n-1 is preserved as historical source wording; 4n-5 is the later justified regular count. Do not substitute one silently for the other.
2. The accepted bound is a partial result for n >= 4. No proof is supplied for a 4n-5 upper bound on arbitrary affine realization strata.
3. Canonical semialgebraic coordinates, continuity, open valid strata, and exact fibers are indispensable to the dimension arguments. Raw parameter counts alone are insufficient.
4. Pointedness and a common apex are indispensable for the spherical graph route. Recoverable lineality and a fixed transverse slice are indispensable for the cylinder route.
5. Exact catalog/raw-source identity and a complete current literature/history audit remain outside verified scope. No global-openness, novelty, or priority claim follows.
6. The author status intentionally remains “audit pending” inside the immutable author freeze. This separate bound audit supplies the present audit result; changing that frozen field would break the binding.

The audit package includes authored analysis, code, results, negatives, and verification metadata only. Source PDFs, extracts, images, raw records, and private coordination are excluded. The manifest is an inventory and integrity record, not an authorization to publish. No remote publication occurred.
