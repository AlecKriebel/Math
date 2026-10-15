# Accepted prior negative result for the general TOPP 42 clause

Date: 9 October 2026 UTC. Problem 5500042 / TOPP 42.

## Accepted mathematical statement and attribution

There exists an embedded closed polyhedral surface whose original faces are polygonal disks and which has no vertex unfolding obtained by cutting only along original edges and retaining original incidences to connect all faces. Each face must remain an isometric copy with pairwise disjoint face interiors in the final planar layout. Retaining arbitrary vertex hinge angles, reflections, or rearrangements of incident faces does not rescue this witness.

The accepted prior result is Abel–Demaine–Demaine, *A Topologically Convex Vertex-Ununfoldable Polyhedron*, CCCG 2011, Theorem 4 and Figure 5. The coordinate reconstruction and audit are authored verification of that published witness, not a new counterexample or new mathematical discovery. The full argument is in GENERAL_CLAUSE_AUDIT.md.

## Why the written proof proves the target

The twelve cyclic face lists define the boundary of K = U union s(U), where U is given by |x| <= 5 and 2|y| - 3 <= z <= (|x| + 1)/2, and s(x,y,z) = (y,x,-z). The union is a union of four bounded convex polytopes with the origin strictly inside each. Their continuous positive radial functions show that the boundary is an embedded sphere. The complete written boundary-exposure calculation identifies all twelve facets and proves that each is a disk, including the four notched octagons.

The original face partition into D and L has eight mixed original vertices. The two reflection symmetries and s reduce every cross-class original incidence to the two pairs at A = (1,2,1). The relevant vectors AB = (0,-4,0), AE = (1,-1,-2), and AD′ = (4,1,2) give cos(theta) = 1/sqrt(6), cos(beta′) = -1/sqrt(21), and cos(gamma′) = -1/sqrt(126). The reflex angle alpha = 2 pi - theta exceeds 3 pi/2; beta′ and gamma′ each exceed pi/2. Thus alpha + beta′ and alpha + gamma′ both exceed 2 pi strictly.

Any retained cross-class original vertex or edge therefore forces positive-area local overlap, regardless of relative planar orientation. A connected layout of both nonempty classes would require such an incidence. This proves the negative result in the exact original-face, original-edge target. Accidental contact between unrelated layout points does not connect the cut surface, and no collision-free unfolding motion is assumed.

These paragraphs are a summary, not a replacement: every coordinate, cyclic face list, analytic boundary argument, angle derivation, model hypothesis, and limitation in the original written proof is preserved in the included audit.

## Separate independent AI review

After the authored audit, separate independent AI review read its full argument, independently checked the U/V boundary exposure and exact angle computations, and visually inspected all three pages of the 2011 source. The review also independently replayed the repaired eight-case validator suite in normal and optimized Python modes. That replay was supplementary; its scripts, fixtures, raw outcomes and logs are not part of this theoretical edition.

The earlier audit's recommendation and pending-review sentences are retained as historical text and do not negate this subsequent acceptance. No fresh substantive proof-search approach was used. This is AI mathematical/source review, not human peer review or formal proof-assistant verification. The review does not imply the conference publication was refereed.

## Limits and source qualifications

- The coordinates are geometrically nonconvex. The midpoint of (5,0,-3) and (0,5,3) lies outside K. The octagonal faces have reflex angles. Neither the geometrically convex polyhedron clause nor the convex-face variant is resolved here; neither residual is declared globally open.
- The historical finite graph check of 3-connectivity supports the auxiliary “topologically convex” description. It is not needed for the accepted general disk-face negative conclusion and is not promoted here into a new analytic proof.
- The official CCCG 2011 index lists the paper, and the author-hosted PDF is byte-identical to the official individual paper. The author bibliography explicitly gives unrefereed = 1 and retains a stale “to appear” field. The paper is a published conference result, not a journal publication or an independently verified peer-reviewed result.
- Garcia–Gutierrez–Ruiz–Winslow's CCCG 2018 Theorem 3 supplies corroborating orthogonal context. Its source proof and figures were inspected, but the figure-dependent notch-placement bounds were not separately quantified and accepted here. The audit retains its exact caveats about the “all other locations” wording and the final putt/ell terminology. It neither declares the theorem false nor relies on it to establish the accepted 2011 conclusion.
- The inspected foundational author manuscript is fifteen pages; its pagination is not conflated with the seven-page SoCG 2002 version or the 2003 book chapter. Extra subdivision/grid cuts would change the target.
- SOURCE_INSPECTION.json is byte-identical to the original inspection record. VERSION_COMPARISON.json preserves the original page indices, exact-match flags, timestamp and 2011 byte-match finding, omitting only the twelve derived page-text fingerprint fields documented in PROVENANCE.md. SOURCE_CATALOGUE.json adds the edition's rehash of six retained public-source records (five PDFs and one HTML file). Hash identity is not mathematical correctness, and packaging made no new source-reading pass.

No executable scripts, fixtures, computational result files, execution logs, copied third-party source bodies or images, datasets, private inventories or inventory digests, private sources or coordination, queue changes, or unrelated repository edits are included.
