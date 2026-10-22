# Independent acceptance review of the second-pass convex-reduction edition

## Verdict

**Accept the fixed second-pass prose edition as a faithful, complete, privacy-scoped presentation of the accepted partial investigation.** No substantive proof was shortened or removed in its transformation. Its explicit examples, preserved correction history, and publication boundary pass this independent review. The ten reviewed edition files remain unchanged.

This accepts an edition of historical partial results. It is not an additional substantive mathematical pass, a final-pass declaration, human peer review, a proof or counterexample to the intended general problem, a novelty claim, or a certification of the current literature status. The lifetime attempt count remains unknown; at least two substantive passes are confirmed. The earlier October 11 degree-two heading has no recovered proof here.

The maximum-vertex-degree-three corollary remains a deduction from the specifically credited published convex full-nerve consequence in this second edition. This review neither replaces that dependence nor inserts subsequent coordinate-realization or extension theorems into the historical text.

## 1. Reviewed edition and evidence boundary

The reviewed repository directory is `unsolved_math_prioritization/attempts/3326_convex_reduction_20261012`. Its exact public inventory consists of:

- `README.md`
- `CONVEX_REDUCTION_PROOFS.md`
- `CONVENTIONS_AND_LOCAL_OBSTRUCTIONS.md`
- `INDEPENDENT_PROOF_REVIEW.md`
- `EXACT_EXAMPLES.json`
- `EXAMPLE_GUIDE.md`
- `ACCEPTANCE_AND_CORRECTIONS.md`
- `SOURCE_LEDGER.json`
- `SOURCE_IDENTITIES.json`
- `PUBLIC_MANIFEST.json`

The public manifest's SHA-256 is `c657c6aa9192602494751d696fffe940c6ea84edeac73e01e2a545e492cf9883`. It identifies nine payload files totaling 77,416 bytes and excludes itself by an explicit self-reference convention. Including the manifest there are exactly ten public files. An independently supplied external preparation seal identifies the complete preparation; that operational seal is not part of the prose publication.

All five complete original source documents and all five complete transformed counterparts were read: the convex-reduction proof report, convention/local-obstruction supplement, accepted independent proof review, scholarly source ledger, and principal source identities. The original and transformed proof texts were compared in full. A separate reconstruction check independently traversed the 193 ordered edit spans in both directions, checked every intervening unchanged substring, rebuilt each whole document, and compared it to both the retained original and the distributed version. This is complete-text preservation, not a heading or excerpt comparison.

The new review also reran the edition's checks and used a separately written exact-rational geometry and incidence verifier on the distributed fixtures. Historical descriptions of source retrieval and inspection remain historical descriptions; this edition review does not claim to have repeated a literature search or freshly verified remote availability of every public URL.

## 2. Transformation completeness

The author proof report changes only its final provenance sentence to point to the distributed scholarly PDF identities. The accepted independent proof review changes only its identification sentence to refer to the distributed public manifest. No proof, qualification, source dependence, numerical certificate, or rejection-history paragraph in either report was omitted.

The convention supplement makes four metadata-only replacements: it removes an operational queue rank, restates the lack of publication action, replaces a reference to a separate geometric effort with the distributed proof-report link, and states the prose edition's exclusion boundary. Its literal-singleton example, arbitrary-star proof, pair/triple criterion, source-separation caveat, and literature limitations are intact.

The principal source-identity document removes an operational attribution and simplifies one metadata key. Its public scholarly PDF titles, URLs, byte counts, SHA-256 values, inspection statements, and negative novelty/status flags remain intact.

The source ledger retains all six scholarly source records and all six retrieval-failure/recovery records. It keeps each substantive claim, inspection distinction, and limitation. It removes raw query strings, an empty publication-action field, private filenames, and identities of excluded extracted text, rendered page images, and an author-homepage capture. Four public scholarly PDF identities remain, each matched independently to the retained source bytes. One historical problem-record inspection phrase is restated without the operational record reference. The task and source-policy descriptions are restricted to the published edition's purpose. A structured comparison, independently applying these bounded transformations, recovers exactly the distributed ledger.

The full-byte retained inputs include the accepted original proof materials, the initial assertion-based author checker, the repaired checker, the accepted audit and its correction history, and the superseded audit prose. There are 91 retained source files. All 91 were compared against their canonical source bytes before and after the recovery and control work.

## 3. Mathematical conventions and dependency

The principal target is a finite covered loopless linear hypergraph. Equivalently, one may use a finite covered Sperner linear hypergraph after accounting for isolated singleton components. Objects are indexed by vertices and are nonempty closed filled planar convex sets. Hyperedges are exactly the inclusion-maximal subfamilies with a common point. A degree bound counts hyperedges incident with a vertex; it is not a bound on hyperedge size.

These hypotheses are consistently maintained. Contact-only models, one-sided contacts, disjoint interiors, triangle boundaries, and selected incidence points are not substituted for unrestricted common intersections. Pairwise intersection graphs alone are not treated as full hypergraph representations.

The credited convex-representation starting point is the consequence stated on page 135 of de Fraysseix, Ossona de Mendez and Rosenstiehl, *Representation of Planar Hypergraphs by Contacts of Triangles*, LNCS 4875, pages 125–136. The chapter credits Ossona de Mendez's *Realization of Posets*. The second edition explicitly does not independently derive the full-nerve consequence from the general separation theorem and does not certify an arbitrary normalized dual-edge hull construction. This boundary appears consistently in the principal proofs, convention supplement, independent review, README, and acceptance discussion.

The source-separation growth discrepancy is also preserved accurately as the reviewed historical observation: the printed condition is weaker than the subsequent estimate uses, while choosing exponential coordinates with base greater than the dimension supplies the stronger inequality. It is not described as a failure of the published theorem.

Sources: [2008 chapter](https://doi.org/10.1007/978-3-540-77537-9_15), [2002 paper](https://jgaa.info/index.php/jgaa/article/view/paper48), and [historical OPG problem](https://www.openproblemgarden.org/op/linear_hypergraphs_with_dimension_3).

## 4. Complete proof review of the preserved deductions

### 4.1 Witness compression

For every maximal edge choose one common witness. For a vertex take the convex hull of witnesses for its incident edges. Coverage makes each hull nonempty; finiteness makes it compact; convexity of the original object places the hull inside that object.

Every nonempty original nerve face extends to a maximal face because the index family is finite. The witness of that maximal face lies in every compressed object indexed by the original face. Conversely, shrinking cannot create a formerly empty common intersection. Thus all faces and all nonfaces, including higher-order ones, are preserved. If distinct maximal edges shared their chosen witness, their union would be a face, contradicting maximality. The empty hypergraph and empty face are explicitly handled, rather than tacitly excluded.

A vertex of degree at most three produces a hull of at most three points. Its hull is a point, segment, or triangle. Nothing in this argument bounds the number of extreme points at a vertex incident with four or more edges. The preserved statement and its degree qualification are correct.

### 4.2 Compact-nerve stability

For a nonempty finite subfamily of nonempty compact sets with empty intersection, the infimum over points of the maximum distance to those sets is positive. If it were zero, points approaching all members would be bounded because their distance to one fixed compact member tends to zero. A convergent subsequence would have a limit in every closed member, contradicting empty intersection.

There are finitely many nonfaces. Choose a positive perturbation tolerance below every associated positive distance gap; if no nonface exists, any positive tolerance works. Containing each old compact object preserves each old face. Keeping each replacement within its tolerance-neighborhood prevents a point from entering all replacements indexed by an old nonface. Hence the entire nerve is unchanged. The proof includes empty triple intersections with nonempty pairs and does not rely on a pairwise-only check.

### 4.3 Nondegenerate triangle inflation and rationalization

A small dilation about an interior point treats a genuine triangle. A sufficiently small surrounding triangle treats a point. For a nondegenerate segment with endpoints a,b, write u=b-a and let n be its quarter-turn. The replacement vertices

    a-eta*u-eta*n, b+eta*u, a-eta*u+eta*n

form a nondegenerate triangle for eta>0. In coordinates parallel to u,n, its base is at longitudinal coordinate -eta and its tip at 1+eta. Both original endpoints, at longitudinal coordinates 0 and 1 and transverse coordinate zero, lie strictly inside. Convexity includes the entire segment strictly inside. Each new vertex lies within sqrt(2)*eta*|u| of the old segment; convexity of distance to a convex set extends this bound over the triangle.

Choosing all perturbations inside the common compact-nerve tolerance preserves every face and nonface while making all objects nondegenerate triangles. This proves the triangle-only equivalence for the stated finite unrestricted triangle/segment/point representations, not for contact systems.

After inflation every chosen desired witness has a positive interior margin in finitely many triangles. Sufficiently small vertex perturbations preserve these margins. The positive nonface distance gaps continue to prevent unwanted intersections under small Hausdorff perturbations. Density of rational coordinates supplies rational triangle vertices. The conclusion is existential; no algorithm or complexity bound is inferred.

Combining the credited convex-realization consequence, witness compression, and this inflation establishes the historical degree-three corollary within its stated dependence. The second edition's wording is correct for that derivation and is preserved unchanged.

### 4.4 Nested singleton scope repair

Maximal intersecting subfamilies form an antichain. Therefore edges {a} and {a,b} cannot both be maximal-intersection hyperedges of any family of sets. The two orders a,e,b,f and b,a,f,e realize exactly a<e, a<f, b<f. The poset is not a chain, so its dimension is exactly two.

This diagnoses a literal wording mismatch. It does not refute the intended loopless problem. In a linear hypergraph any proper edge containment forces the smaller edge to have size one. A singleton in a Sperner linear hypergraph is isolated, because any further incident edge would contain it. Removing isolated singleton components restricts the incidence poset and cannot increase dimension. After representing the remaining finite family, separate distant triangles reinsert those components. Conversely the loopless class is contained in the Sperner linear class. This proves the stated equivalence, while deleting nested singleton edges from a non-Sperner input changes that input.

### 4.5 Arbitrarily many exposed witnesses

For p_i=(i,i²), the functional ell_i(x,y)=y-2ix+i² takes value zero at p_i and positive value (j-i)² at each other p_j. Its values on the downward leaf below p_i are negative. Thus the hull of the p_j meets that leaf exactly at p_i, and p_i is exposed in the hull. Distinct leaves have distinct x-coordinates and are disjoint.

An inscribed replacement retaining every leaf intersection must contain every p_i. An extreme point of the old hull remains extreme in any contained convex replacement that contains it. At least four such points cannot fit into a triangle or segment as its extreme points. This proves the inscribed-replacement obstruction for arbitrary k>=4.

The displayed forward, reverse, and leaves-before-center orders realize the star incidence poset. For the dimension-three lower bound when k>=3, a hypothetical two-order realizer must put each leaf before the incomparable center in some order. Two leaves occur before the center in one order. Reversing their two nonincident leaf-edge comparisons in the other order creates a directed cycle together with the required incidences. Hence two orders cannot suffice.

The underlying star has a simple segment representation using one horizontal central segment and disjoint vertical leaves. The obstruction concerns fixed geometry and an inscribed replacement; it is not hypergraph nonrepresentability.

### 4.6 Fixed-neighbor area obstruction

The central unit square, four short outward diagonal leaves with parameter between 1 and 7/6, and the sides of the outer square of half-side 4/3 have exactly the four star edges and four cycle edges stated in the report. The leaves end strictly before the outer boundary. Adjacent outer sides meet, opposite sides do not, and no unwanted triple occurs.

Any convex central replacement preserving the leaf incidences contains four points on the diagonal rays, with radial parameters t_i>=1. Their diagonals cross at the origin, so they are in convex cyclic order. Their quadrilateral has area

    (t1+t3)(t2+t4) >= 4.

The replacement must avoid the entire outer-square boundary. It contains an interior leaf point; a segment to any point outside the outer-square interior would cross that boundary. Convexity therefore confines the replacement to the outer square.

A triangle in a square of side s has area at most s²/2. The absolute determinant defining twice its area, with two vertices fixed, is a convex function of the third. Replacing each vertex successively by a square corner without decreasing the objective reduces the maximum to corner triples, each of area at most half the square. Here the bound is 32/9<4. A segment has area zero. Both contradict the necessary lower bound.

This stronger local obstruction permits moved leaf witnesses and enlarged central objects; the eight neighboring objects remain fixed. The displayed three-order realizer proves incidence dimension at most three, with the star subposet giving equality. The hypergraph itself has a segment representation, so no global counterexample is claimed.

### 4.7 Pair/triple full-nerve criterion

For the downward closure of a covered linear Sperner hypergraph, suppose every subset of a set A of size at most three is a face. If A has at least four members, choose a,b,c in A and an edge containing them. For each further x there is an edge containing a,b,x. It shares two vertices with the first edge, so linearity makes the edges equal. The first edge contains all of A. Therefore every minimal nonface has size at most three.

It follows that realizing each edge by a common point and excluding every nonedge pair and triple is sufficient. Any unwanted larger common intersection would make all its pairs and triples faces, forcing the larger index set into the downward closure. Realizing edges realizes all faces, and Sperner maximality recovers exactly the edge family. This is a combinatorial argument for arbitrary nonempty sets. The optional Helly reduction for checking positive planar convex intersections is separate and is not needed for this proof.

### 4.8 The nonplanar five-vertex example

The five supplied segments lie on x=0, x+y=4, y=0, y=x-2, and y=x/3. Their endpoints and six listed witnesses give maximal pair edges 12,23,34,14 and maximal triple edges 135,245. Exact independent evaluation recovers all ten intersecting pairs, only the two specified intersecting triples, no higher face, and 17 nonempty faces in total.

The three listed orders realize the incidence poset on its eleven elements. Restricting to vertices 1,2,3 and edge elements a,b,e yields the standard example S3: its three missing-incidence pairs cannot have two reversed in one extension without a cycle through the two cross-incidences. Three orders are therefore necessary and sufficient.

The nine listed paths connect branch classes {1,3,f} and {2,4,e}, have distinct internal vertices outside those classes, and account for all 14 incidence-graph edges. They prove a subdivision of K3,3. Nonplanarity of this incidence graph is fully compatible with the exhibited unrestricted segment representation.

## 5. Independent finite checks and meaningful rejection controls

The separately written edition-review checker uses exact rational convex hulls, point containment, and boundary-segment intersections. A vertex of a nonempty compact polygon intersection is an original vertex or an intersection of boundary segments. Original endpoints also handle contained segments, collinear overlap, and isolated point cases. Candidate points are tested against every member of the subfamily. This is distinct from the edition's rational half-plane-feasibility implementation.

The independent baseline checks:

- Five-vertex segments: all 31 nonempty subfamilies, 17 faces, six maximal faces, six exact maximal witnesses, and all 110 ordered distinct incidence-poset pairs.
- Fixed-neighbor family: all 511 nonempty subfamilies, 17 faces, eight maximal faces, all 272 ordered pairs, the exact four outer sides and four leaves, 64 ordered square-corner triples, and 81 radial-parameter choices.
- Inflated five-vertex triangles: all 31 nonempty subfamilies, 17 faces, the same six maximal edges, the exact inflation formula, and strict containment of both original endpoints in each nondegenerate triangle.
- Exposed four-leaf star: all 31 nonempty subfamilies, nine faces, four maximal edges, 72 ordered pairs, and the exact exposing-functional evaluations.
- Nested singleton: all 12 ordered pairs and proper edge containment.
- Empty-triple fixture: all seven nonempty subfamilies, six faces, three maximal pairs, and an empty triple.
- The S3 incidence pattern and all 14 edges in the K3,3 subdivision certificate.

Six controlled baseline replays, covering ordinary Python, -O, and -OO under hash seeds 0 and 123, have byte-identical outputs. An initial ordinary replay also agrees. Each baseline contains eleven altered-fixture rejection tests and one explicit-gate test. The changes lose a required triple witness, violate an incidence order, extend a leaf to a blocker, falsify the area bound, create a concurrent triple invisible in the pairwise graph, corrupt inflation coordinates, move a witness, alter a subdivision endpoint, reverse the exposed-leaf direction, alter the nested edge, or replace an integer face count with a Boolean.

A separate source-mutation harness changes actual checker logic in temporary files: it loses closed polygon boundaries, substitutes pairwise-only testing for full common intersection, changes the area divisor, or disables the explicit gate. Each of these four substantive source mutations rejects in all three interpreter modes, giving twelve additional rejections. They are not merely hash mismatches, appended unconditional failures, or timeouts.

The preparation's own validation and 27 controls were also rerun in ordinary, -O, and -OO modes. Successful outputs agree, and control records agree after removing only their declared optimization-level field. These controls distinguish semantic fixture failures, privacy/link/scope failures, and integrity/preservation failures rather than calling every rejected changed hash a semantic test.

Finally, both accepted historical source-mutation harnesses were replayed: the repaired author's four mutations and the accepted independent audit's four mutations reject in all three modes, for 24 historical source-mutation rejections. Their normal baselines remain optimization-safe. The accepted audit baseline also reproduces its arbitrary-star and 109-small-hypergraph regressions. All mutation files are temporary copies; canonical sources are unchanged. No timeout is accepted as a rejection.

The finite tests support the displayed finite certificates. They do not replace the compactness argument, arbitrary-k proof, rationalization argument, or general pair/triple proof.

## 6. Correction history and deterministic evidence

The initial author checker used assertion gates that disappear under optimized Python. That initial version is retained as history and is not certified as optimization-safe. The accepted repair replaces those gates with explicit `VerificationError` exceptions. The corresponding proof report's checker discussion and the acceptance history fully describe the distinction. This review reproduced the historical defect on a temporary source copy with an invalid area inequality: ordinary Python rejected it with an assertion failure, while -O and -OO accepted it after disabling those assertions. This deliberate demonstration confirms why the initial checker was rejected; it is not acceptance of the invalid certificate. The repaired source contains no assertion gates and rejects its false-area mutation in all three modes.

The original empty-hypergraph and empty-face ambiguity was repaired explicitly. The S3 lower-bound wording was also corrected to identify two cross-incidences and two assumed reversals, rather than four incidences. The complete corrected arguments are preserved.

The earlier independent audit had an unordered set representation in a rejection diagnostic. Its mathematical checks passed, but the nondeterministic evidence failed a roundtrip before terminal acceptance. The accepted repair sorts each face and then the face list before formatting the diagnostic. The public acceptance history retains the failure, repair, and superseded-edition distinction. This review inspected the actual one-line diagnostic difference and reran the accepted harness.

The preparation subsequently normalized temporary-directory prefixes in a symlink diagnostic. This affected deterministic evidence only; the public mathematical files did not change. The second edition's accepted control records preserve stable diagnostics across modes. Sorted traversals, explicit exception gates, exact expected failure classes, and temporary-copy permissions were reviewed; none is replaced by a claim that read-only flags make data immutable.

## 7. Privacy, links, and actual restoration

The exact public allowlist was checked independently, including files located under input directories whose names alone would otherwise misleadingly suggest publication eligibility. The ten public files contain authored mathematical prose, small explicit geometry/realizer examples, public scholarly metadata, and actual distributed-file identities. They contain no executable programs, raw search datasets, copied source PDFs or extracted source text, private source material, private personal data, private coordination records, or operational identities of omitted artifacts.

Every distributed payload identity matches the manifest. Every 64-hex identity found in the public text belongs to an actual distributed file or one of the four permitted scholarly PDFs. The retained source bytes independently confirm those PDF identities. Excluded source and operational hashes do not occur in the edition. Local document links resolve to the exact allowlisted public files; the preserved public scholarly URLs have the expected syntax and hosts. This is not a claim of fresh successful remote retrieval.

Recovery was performed again, rather than accepted from a digest or prior receipt. The full preparation and its external seal were independently packed into a deterministic archive and compared byte-for-byte with the retained archive. The exact 25 file members were safely extracted and compared with the canonical preparation. All 91 retained source files were decoded into actual files and their sizes, hashes, and bytes checked. The restored preparation then passed ordinary, -O, and -OO validation using those restored sources.

Separately, all 171 retained full-byte chunks were read in verified contiguous offset order and assembled into an archive. Those complete recovered archive bytes match the independently rebuilt archive. This second route was separately extracted, all 91 source files restored again, and all three validation modes replayed successfully. Thus both reconstruction and full-byte store restoration were exercised. A hash alone was not treated as a backup.

Only newly created review/recovery files and temporary control copies were made writable. The original public edition, its complete preparation, and all retained canonical source files remained byte-identical. Static read-only permissions help protect the snapshot; they do not establish immutability, concurrency safety, or protection against an actor able to change permissions.

## 8. Final acceptance boundary

No correction to the fixed ten-file second edition is required by this review. Its full proofs, credited dependence, source-inspection limits, literal-scope warning, local-obstruction distinction, five-vertex representation, and rejection/correction history are preserved and correctly qualified.

This acceptance does not insert subsequent mathematics into the second pass and does not certify the infinite conjecture from finite tests. The intended general problem remains unresolved within this historical investigation. No remote publication or queue modification is part of this edition review.
