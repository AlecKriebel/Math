# Independent acceptance review of the third-pass coordinate and cyclic-core edition

## Verdict

**Accept the fixed third-pass prose edition as a complete, faithful, privacy-scoped presentation of the accepted coordinate and cyclic-core results, together with its unchanged historical companion edition. No correction to the fixed edition is required.**

The complete coordinate construction, complete cyclic-core proof, both independent mathematical reviews, complete second-edition acceptance, source attribution, finite diagnostics, and exact examples are preserved. The separately labeled integration correctly discharges the historical convex-consequence dependency using the accepted coordinate theorem and the previously accepted inflation proof. It does not rewrite the frozen core proof or the older edition.

This is an edition acceptance, not a fourth substantive mathematical pass, a final-pass declaration, human peer review, a general solution or counterexample, a novelty claim, or a certification of current literature status. At least three substantive passes are confirmed; the lifetime count remains unknown. The intended general triangle-and-segment problem remains unresolved in this investigation. Work on subsequent cyclic-rooted blocks is outside this fixed edition and outside this review.

## 1. Fixed edition and complete review boundary

The new repository directory is `unsolved_math_prioritization/attempts/3326_coordinate_core_20261012`. Its exact inventory consists of thirteen files:

- `README.md`
- `FULL_NERVE_COORDINATE_PROOF.md`
- `CYCLIC_CORE_EXTENSION_PROOF.md`
- `COORDINATE_PROOF_REVIEW.md`
- `CORE_PROOF_REVIEW.md`
- `SECOND_EDITION_REVIEW.md`
- `CORE_VERIFICATION_SUMMARY.md`
- `COORDINATE_SOURCE_IDENTITIES.json`
- `COORDINATE_VERIFICATION_SUMMARY.json`
- `EXACT_EXAMPLES.json`
- `EXAMPLE_GUIDE.md`
- `INTEGRATION_AND_ACCEPTANCE.md`
- `PUBLIC_MANIFEST.json`

The manifest has SHA-256 `2c0b5b35a842ebd875efbd9bda39e943b9240ae4e2be7e5dd6369dd975208c11`. It lists the other twelve files and explicitly excludes itself from its payload list. The ten files of the sibling `3326_convex_reduction_20261012` directory remain byte for byte unchanged. Thus the reviewed preparation contains exactly twenty-three public files. This new acceptance report is separate from that fixed inventory.

I read the full coordinate proof, full core proof, full coordinate and core reviews, full integration, complete second-edition acceptance, all accompanying summaries and source metadata, and the preserved second-edition proofs, convention supplement, independent review, and correction history. The review does not rest on verdict paragraphs or proof excerpts. The eight complete mapped original documents and their complete distributed counterparts were compared, and every change was inspected in context.

An independently written preservation check traverses all seventy-six edit spans in forward order. It checks every unchanged interval, every original and replacement span, and the complete trailing interval. Reassembling the full documents in both directions reproduces exactly the accepted sources and distributed files. Every retained input is compared against the canonical complete bytes, including the final coordinate and core acceptance records and the complete second-edition acceptance. This checks full-text preservation, rather than merely matching section names, counts, or hashes supplied by the edition builder.

## 2. Transformation scope and historical integrity

The coordinate proof has only bounded editorial substitutions: removal of an operational queue rank, replacement of a private-checker description by a reference to its accompanying historical verification summary, and a publication-boundary sentence. None changes a definition, theorem, displayed formula, proof step, example, source credit, numerical diagnostic, or limitation.

The cyclic-core author proof and its complete verification summary are unchanged. In particular the core proof still says that its concurrent coordinate deduction had not yet been assumed accepted. The new README and integration identify that statement as historical and give the later deduction separately. The report is not retrospectively made to claim evidence it did not yet have.

The coordinate source-identity file removes only identities of excluded extracted text and a rendered page image. Both scholarly PDF identities and all authored attribution and inspection statements remain. The coordinate verification summary removes two identities of excluded computational outputs and annotates its original pending-review status with the later completed review. Its fixture counts, root-certificate counts, checked-pair counts, optimization modes, negative-control counts, and scope remain intact.

The coordinate independent review replaces its identification sentence with the distributed proof and manifest references. The core independent review makes three metadata-only sentence replacements: an omitted author-manifest identity becomes a distributed-manifest reference; identities of separate acceptance artifacts become references to the complete included coordinate proof, review, and integration; and identities of undistributed raw checker outputs become a sentence preserving their separate pinning and substantive verification boundary. The original core proof's identity remains because that complete report is actually distributed unchanged. No mathematical review paragraph is removed.

The complete second-edition acceptance is included unchanged, with SHA-256 `022e261c647ab6069e01ce39f8675ba22cbaad0275c0036609185b5247cc678c`. It preserves the original five-source, 193-span transformation review, ninety-one retained source files, exact earlier examples, optimization-defect demonstration, deterministic-diagnostic repair, credited dependency, and historical two-pass status. Its old status statements are accurately contextualized by the new integration; they are not silently revised. Every one of the ten older public files matches both its original bytes and the identities in both edition manifests.

## 3. Coordinate full-nerve proof

### 3.1 Scope and normalization

The theorem takes a finite hypergraph with nonempty edges covering its vertex set and a supplied length-d incidence-poset realizer. Vertex and edge elements are distinct labels, including for singleton edges. The supplied realizer need not have minimum length. Reversing every order gives the dual realizer. With consecutive ranks r_i and integer B>d, the unnormalized coordinates are F_i(x)=B raised to r_i(x). Each edge vector is divided by its positive coordinate sum to obtain q_e, and C_v is the convex hull of the q_e for edges incident with v.

The resulting sets are nonempty compact filled convex hulls in the coordinate-sum-one hyperplane. Deleting one coordinate is an affine bijection from this hyperplane to R^(d-1), so it preserves all convex combinations and intersections. Coordinates are rational. The exact nerve claim is the downward closure of the original edge family. Sperner is needed only to identify every original listed edge as a maximal face. Linearity is not a hypothesis of this general coordinate theorem.

### 3.2 Minimal nonfaces

For an inclusion-minimal nonface S={v_1,...,v_k}, coverage gives k>=2. Minimality provides an edge e_i containing S minus v_i and omitting v_i. The e_i are distinct: equality of two such edges would contain their union S. Each incomparable pair v_i,e_i must be reversed in one original extension. If one extension reversed both i and j, the two cross-incidences would force the strict cycle e_i<v_i<e_j<v_j<e_i. Therefore k distinct orders are necessary and k<=d. This proof applies to k=2 and does not require a convention restricting the name of the standard example to larger k.

### 3.3 Reciprocal inequalities and different radial lifts

For a vertex w, the positive functional h_w(z)=sum_i z_i/F_i(w) is at most d/B on every F(e) incident with w. This follows because the incident edge precedes w in every dual order by at least one rank. For an omitted incidence, the realizer supplies a reversed rank in at least one coordinate, giving h_w(F(e))>=B. These are inequalities on unnormalized vectors; substituting normalized vectors without their scale factors would be invalid.

If x=sum_e lambda_e q_e lies in C_v, define t_v as the reciprocal of sum_e lambda_e/s_e, where s_e is the positive sum of F(e)'s coordinates. Then alpha_e=t_v lambda_e/s_e are nonnegative, sum to one, and satisfy t_v x=sum_e alpha_e F(e). This is an actual radial lift into the unnormalized hull. Different objects can require different t_v for the same x.

For a hypothetical common point of a minimal nonface S, select a vertex v with minimum t_v. For every other w, positive linearity and t_v/t_w<=1 give h_w(t_v x)<=d/B. Their sum is at most (k-1)d/B. Every edge incident with v omits at least one other w in S, whose functional on that edge vector is at least B. All other summands are positive. Thus the same summed functional is at least B on every generating vector and on their convex combination t_v x. The bounds contradict (k-1)d/B<=d(d-1)/B<B. This excludes every minimal nonface, and hence every nonface. An edge witness q_e supplies the converse for every face.

The coefficient-mass restatement is also correct. The omission classes cover all supporting edges of the minimum lift, while their total allowed mass is less than one. Overlap only makes the covering inequality weaker, so it does not invalidate that contradiction.

### 3.4 Exceptional cases and planar consequence

The empty hypergraph uses the empty family. Coverage handles every nonempty hull; the empty face is conventional. For d=1 a minimal nonface would require 2<=k<=1 and cannot occur. Nested singleton edges give the same downward closure as their maximal edges and cannot both survive as distinct maximal intersection faces. Isolated singleton components are harmless. This remains a convention distinction, not a resolution or refutation of the intended loopless question.

For incidence dimension at most three, orders may be repeated to obtain d=3. Using B=4 gives planar rational hulls. A vertex incident with at most three edges has at most three generators, hence a point, segment, or triangle. The accepted compact-nerve stability argument and outer inflation then produce nondegenerate rational triangles while preserving every face and nonface and making the chosen edge witnesses interior.

The proof does not supply a three-corner bound at arbitrary degree. The four-leaf star's central coordinate hull has four extreme vertices. That same hypergraph has a different segment representation, so this is a limitation of the coordinate construction. The frozen second-edition fixed-neighbor and inscribed-replacement obstructions also concern particular conversion procedures, not all global representations.

## 4. Cyclic-core theorem and exact integration

### 4.1 Private boundary arcs

For a full-nerve representation of a covered loopless linear hypergraph, group an object's intersections with other objects by the incident hyperedge. Each group is nonempty and compact. Distinct groups are disjoint: a shared point would realize a triple, and the uniqueness of an edge containing each of its two pairs with the fixed vertex would force the groups to be equal. This uses the full nerve, not merely the pairwise intersection graph.

If the polygon boundary were covered by these groups, their intersections with the connected boundary would be a finite disjoint closed cover. Exactly one group could be nonempty, so one group would cover the whole boundary. An edge witness belongs to every object forming that group. Every point of the polygon lies on a segment from that witness to a boundary point; convexity of the group member containing that endpoint puts the entire segment in that member. The group would cover the whole polygon, contradicting a second nonempty incident group. Therefore an object of vertex degree at least two has a private boundary point.

The finite union of other objects is compact. A private point consequently has an avoiding neighborhood, within which a side-interior point can be selected and the polygon locally agrees with a closed half-plane. The argument does not assume that every edge group meets the boundary. It also does not claim a private boundary for arbitrary degree-one objects; strict containment is a legitimate counterexample to that stronger assertion.

### 4.2 Rational pendant insertion

In rational affine coordinates at a private side-interior point, put the old triangle locally in y<=0. A sufficiently small rational radius r makes the entire closed radius-r disk avoid all other old objects. The common base a=(-r/2,-r/2), b=(r/2,-r/2), and distinct rational circle tips t_i=r(2s_i/(1+s_i^2),(1-s_i^2)/(1+s_i^2)), with -1/4<s_i<1/4, give nondegenerate rational triangles for all fresh vertices of one new edge.

Every tip lies above y=r/2 with horizontal coordinate of absolute value less than r/2. The stated cross-section formula shows that q=(0,-r/4) lies strictly inside every new triangle and inside the parent. Hence the whole intended edge has a common interior witness. Every new triangle misses every old object except its parent, so no unintended subfamily involving a new object can intersect. This establishes the full nerve.

Each tip lies outside its parent. The tangent of the strictly convex circle strictly separates it from the other distinct tips and the common base points, which are interior to the disk. Thus it has a private neighborhood among all old and new objects, and a nearby private side arc. Future descendants can use that arc to avoid the grandparent. The construction is simultaneous for all new members of a hyperedge and does not place every child wholly inside the parent.

After another insertion at the same root, its degree is at least two and the boundary lemma can be reapplied. An insertion at a different root avoids every other old object, so it cannot destroy their private arcs. Finite iteration is justified without pretending that one fixed arc survives every insertion at its own root.

### 4.3 Whole-edge backbone

In a connected incidence component with nonempty graph 2-core, the outside components are trees with one attachment. An outside cycle, or a path connecting two core nodes, would itself survive pruning. Initially select all edges whose edge-nodes survive, keeping their whole original vertex sets. Core vertices have selected degree equal to their core degree. Included noncore vertices have selected degree one, because two core-edge neighbors would put them in the core. In an empty-core component select one whole edge.

Whenever a selected degree-one vertex has an omitted incident edge, add one such whole edge. The new edge has exactly one previously selected vertex; a second would create an outside cycle or a second attachment. The selected root becomes degree two and all new vertices begin at degree one. Subsequent additions cannot inadvertently increase an old degree-two or degree-three vertex. The process terminates with maximum vertex degree at most three, and every remaining attachment root has selected degree at least two.

Keeping whole edges ensures that the selected incidence poset is an induced subposet. Restricting each realizer order therefore preserves the dimension bound. Omitted components attach only at selected vertex-nodes and are read away from that root, with one old parent and all other vertices fresh at each step. This is exactly the permitted pendant operation and reconstructs every original hyperedge without truncation or identification.

### 4.4 Discharging the historical dependency

Apply the accepted coordinate theorem to the backbone's restricted three-order realizer with B=4. Its full nerve is the downward closure of the whole selected edges. Covered loopless linearity makes these edges Sperner. Maximum vertex degree three gives rational points, segments, or triangles. The unchanged accepted stability and inflation proof supplies rational nondegenerate triangles with the same full nerve and interior witnesses.

The boundary lemma supplies arcs at every omitted-tree root because each has selected degree at least two. The rational graft then reconstructs the omitted trees. Separate components fit in disjoint rational boxes, and the empty hypergraph is handled separately. This proves the stated sufficient condition: vertex-node degrees in the incidence graph's 2-core are at most three. Additional tree incidences at core vertices, and degrees outside the core, are unrestricted.

This is a valid composition of accepted results and removes the earlier omitted convex-consequence deduction from the integrated theorem. The frozen author proof still reports its historical dependence accurately. The integration does not establish a theorem for an arbitrary vertex of degree four entirely inside the cyclic core. Nor does it claim that arbitrary pendant attachment preserves incidence dimension three.

### 4.5 Nonplanar example and uniform family

The seven-vertex example keeps the five-vertex nonplanar core and adds the two-level chain g={1,6}, h={6,7}. The displayed realizer has 210 ordered distinct pairs. Its induced S3 gives the lower dimension bound, and the retained nine internally disjoint paths supply the K3,3 subdivision of the incidence graph. The first five triangles use the exact inflation formula, and the two displayed added triangles give the intended additional edges without a grandparent incidence.

The uniform family attaches z to vertex 1 and leaves u_0,...,u_k to z. Its three-order proof covers old/old pairs, old/new pairs, g with old elements and star elements, z with leaves and incident edges, pairs of leaves, pairs of edge elements, diagonal incidences, and off-diagonal leaf/edge pairs. The positive-index and zero-index cases and k=0 endpoint are all treated. The original S3 and K3,3 subdivision persist. Thus the all-k proof gives a connected nonplanar dimension-three family with unbounded degree outside the fixed cyclic core; its finite regressions do not supply the universal quantifier by themselves.

## 5. Independent exact examples and substantive mutation tests

The separately written checker for this acceptance uses exact rational point containment, convex hulls, original vertices, and intersections of boundary segments. It does not import the edition's half-plane-feasibility implementation. For a nonempty bounded intersection of convex polygons, a vertex is an original vertex or a crossing of boundary edges. Original endpoints also handle contained segments, collinear overlap, and isolated-point cases. Every candidate is tested against every member of the subfamily. Explicit closed-contact and pairwise-without-common-point controls check the two important edge cases.

Its complete fixture checks give:

- Three-edge standard example: 30 ordered incidence-poset pairs; all seven nonempty subfamilies; six faces and three maximal faces; all three exact normalized witnesses, complete segment hulls, and three root certificates.
- Four-leaf star: 72 ordered pairs; all thirty-one nonempty subfamilies; nine faces and four maximal faces; all four exact witnesses and four central extreme vertices; six minimal nonfaces and twelve root certificates.
- Nonplanar two-level attachment: 210 ordered pairs; all 127 nonempty subfamilies; twenty-one faces and eight maximal faces; all seven nondegenerate rational triangles, strict containment of both endpoints in each of the first five inflated triangles, the exact two graft triangles, the 2-core, maximum full degree four, maximum core degree three, and the missing intersection of objects 1 and 7.

In total this independently reproduces 312 ordered pairs, 165 nonempty subfamilies, and fifteen exact minimum-lift certificates. It recomputes the rank vectors, normalization, all reciprocal bounds, minimal nonfaces, lower and upper bounds, and strict gaps instead of trusting stored numerical verdicts. The standard-example lower bounds are 4425/1024, 4233/1024, and 4425/1024 against upper bound 3/2.

Ten altered-fixture controls independently reject an invalid order, corrupt normalization, inadmissible base, missing root, incorrect radial bound, grandparent intersection, incorrect core, degenerate triangle, Boolean count, and incorrect inflation scale. An additional direct gate control confirms explicit exceptions are active.

The checker is replayed under ordinary Python, -O, and -OO, each with hash seeds 0 and 123. All six outputs are byte-identical. A separate source-mutation harness alters actual checking logic in disposable writable files: strict instead of closed polygon boundaries, pairwise-only instead of full common intersection, maximum instead of minimum root lower bound, reversed rank orientation, and a disabled explicit gate. Every mutation rejects in all three interpreter modes with its expected substantive audit diagnostic, for fifteen source-mutation rejections. These are not hash-only failures or appended unconditional exceptions. The disabled-gate mutation is caught because the altered fixtures cease to reject; the harness does not rely on the disabled gate to certify its own failure.

The preparation's validation and all thirty-five controls are also replayed in all six mode/seed combinations. Each kind of output is byte-identical. Its controls distinguish thirteen semantic fixture mutations, four strict-parser failures, seven privacy/link/scope failures, eight closed-integrity failures, fixed-map and prior-preservation failures, and one explicit-gate failure. Rejected changed hashes are not described as semantic mathematical tests. Every mutation uses a writable disposable copy. No timeout is counted as rejection.

The earlier coordinate and core reviews' larger diagnostic counts and correction histories are retained in full. This edition acceptance adds its own small-fixture and preservation checks; it does not relabel those historical checks as newly repeated infinite proofs. In particular it preserves the coordinate review's exact barycentric primal/Farkas method, the core review's independent clipping and backbone checks, and the historical assertion and unordered-diagnostic repairs.

## 6. Source credit, privacy, links, and recovery

Source credit remains with Ossona de Mendez's rapidly increasing-coordinate and radial-normalization construction and the convex maximal-intersection consequence stated by de Fraysseix, Ossona de Mendez and Rosenstiehl. The new proof is explicitly an exponential specialization and a direct full-nerve deduction. The earlier printed growth-condition discrepancy remains accurately attributed and limited: B>d supplies the stronger inequality actually used, without asserting that the published existence theorem fails. Source-inspection statements remain statements of the actual prior inspections. This edition review does not claim a new literature search or fresh remote availability check.

Primary references: [Realization of Posets](https://jgaa.info/index.php/jgaa/article/view/paper48) and [Representation of Planar Hypergraphs by Contacts of Triangles](https://doi.org/10.1007/978-3-540-77537-9_15).

The unchanged source ledger retains all six scholarly records and six retrieval-failure/recovery records, including the distinction between full download, full text inspection, selected-section inspection, visual inspection, and abstract-only access. The singleton convention, segment-only versus mixed-object distinction, adjacent point-line literature, and missing historical proof remain explicit. None of these records is a present-day open-status or novelty certificate.

The independent privacy pass checks the exact twenty-three-file public allowlist, every payload identity, and all sixty-six Markdown links. Every local link resolves inside that allowlist. Public URL hosts and syntax match the preserved scholarly destinations; no new remote-retrieval success is inferred. Every 64-hex identity in public text denotes an actual distributed file or one of the four permitted scholarly PDFs. All four scholarly identities match complete retained PDF bytes. Directory labels alone confer no publication eligibility.

The public files contain authored proof and review prose, complete small rational examples, permitted scholarly metadata, and actual distributed-file identities. They exclude copied source PDFs and extracted documents, rendered screenshots, programs, raw computational datasets or logs, private sources, private personal information, private coordination records, and identities of omitted operational artifacts. No broader publication permission is inferred from the word public in an input path.

Recovery was exercised again from actual bytes. The entire sealed preparation and external seal were independently packed with the specified deterministic ordering and metadata. The resulting archive is byte for byte identical to the retained input archive. Its thirty-eight regular members were safely extracted and compared to the canonical preparation. All 169 retained input records were decoded into actual files, and the nested earlier snapshot's ninety-one source files were separately restored and compared with their canonical bytes.

A second route reads and verifies all 334 content-addressed full-byte chunks in contiguous offset order, reconstructs the complete archive, extracts it separately, restores the same 169 plus ninety-one records, and repeats the comparisons. Both restored preparations pass validation under ordinary Python, -O, and -OO with the expected byte-identical output. This supplies six successful restored validation runs. A hash or a previous receipt was not treated as a backup.

Only newly created review and recovery artifacts and disposable controls were written. The fixed preparation, public edition, and all canonical retained inputs remain byte-identical. Read-only permission bits protect a static snapshot but do not establish immutability, race safety, or a remote guarantee.

## 7. Final acceptance boundary

The fixed thirteen-file third-pass edition and ten unchanged historical companion files pass this independent review without modification. Full source and proof preservation, explicit historical integration, exact finite examples, metadata-only exclusions, mathematical scope, optimization-safe controls, deterministic evidence, and actual byte recovery are accepted.

The accepted scope is the full downward-closed nerve of finite covered input under the coordinate theorem, and rational nondegenerate triangle realizations for the stated incidence-dimension-three degree-three or 2-core-degree-three sufficient classes. Objects are closed and filled, and intersections are unrestricted. External trees may have unbounded degree. No arbitrary degree-four cyclic-core theorem, general counterexample, literal nested-maximal-edge representation, contact theorem, fourth-pass result, final-pass status, or lifetime count is asserted. No remote publication or queue modification is part of this edition review.
