# Complete independent metric-ball geometry audit

**Verdict: PASS for the frozen Euclidean noncocompact claim. Full original source remains unresolved. One stale README metadata sentence requires reconciliation before accepting the reviewed package.**

PR24 / 10000062 / AMR-099-0062. Exact original head `6b702110d1bd4b9220e2033fa5eed030911ce8c6`. Frozen `CANDIDATE.md` SHA-256 `3df33716dab169f07c9ff24434023d2945fc8121e03519f91a0a3fdb1ea30f84`. This audit checks the supplied construction and its precise scope; it adds zero substantive proof-search attempts. No candidate, canonical status, queue, PR, branch, publication, or external account was modified. All first-party writes are confined to this family's audit directory; downloaded foreign PDFs and rerun scratch are in its ignored `tmp/`.

## 1. Independence, assumptions, source, and success criterion

`SEALED_CRITERION.md` and `seal.json` were written at 2026-10-01T20:39:01.166811Z before reading historical reviewer text, historical checkers/results, or root/other-family findings. The seal digest is `e83734fa33fb732540bb0c1facd41b44349b54192ffe7445114cefb68446b9bc`. The frozen candidate was treated as a hypothesis. Root and nested research instructions were read; their budget and independent-review requirements are preserved.

The [archived original source](https://arquivo.pt/noFrame/replay/20201231041538id_/http://www.wisdom.weizmann.ac.il/~itai/erd100.pdf), Question5.7, printed page7, was freshly downloaded, text-read, rendered, and visually inspected. Its assumptions concern all vertex-centered ambient metric balls at radius r and triangles of diameter at most r. It allows Euclidean or hyperbolic geometry, uses unrestricted ambient isometries, and does not define periodicity or open-versus-closed balls. The candidate proves the stronger closed-disk restriction statement it explicitly defines. The [author-hosted alternate version](https://www.wisdom.weizmann.ac.il/~itai/erdos.pdf) was available in the browser's indexed primary copy, with the same question at page6; the direct fresh download returned404. The archived original is the actual fresh primary source used here.

The [published Frettlöh–Garber article](https://dmtcs.episciences.org/2142/pdf) was freshly downloaded and its definitions, Theorem2.2, Section2.3, and Figures8/17 inspected. It already contains the arbitrary alternating isosceles/chiral triangular-layer family and noncrystallographic members. Its corona condition is weaker than the present full metric-ball condition. Its Euclidean theorem yields a nonzero translation from congruent coronae; its hyperbolic theorem concerns monocoronal tilings, not the required full metric balls. No prior-family or worldwide-priority claim is justified by this audit.

Foreign source hashes and download outcomes are recorded in `source_downloads.json`: archived original SHA-256 `d49f0423f4420e0c3469ce4af09e07b3e5051ef4ab0f65b578c6f1fd58061745`; published prior-work PDF SHA-256 `5d652ce6d67dd9d0a5aa683ec6dd2b369ff8a913dec25cb318f8a60d8e7eebaf`.

The acceptance criterion is universal: every permitted bi-infinite layer sequence must define a locally finite face-to-face nondegenerate straight triangulation; every triangle must have diameter <=sqrt(10); and every pair of closed vertex-centered disks must have ambient-congruent restrictions of all vertex, edge, and face cells, including singleton/tangent traces, circle boundaries, and inherited parent-cell incidences. Coronae, graph balls, rooted vertex sets, counts, or finite tests alone do not suffice.

## 2. Global triangulation and exact diameters

For any strip with lower P_k=(b+2k,y), upper Q_k=(b+s+2k,y+h), 0<s<2, h>0, let D_k=[P_k,P_{k+1},Q_k] and E_k=[Q_{k-1},Q_k,P_k]. At normalized height t in [0,1], their sections are

- E_k: [b+2k+(s-2)t, b+2k+st];
- D_k: [b+2k+st, b+2(k+1)+(s-2)t].

The right endpoint of D_k is the left endpoint of E_{k+1}. Their interiors partition the horizontal line at every interior strip height. Boundary degeneracies are precisely the named shared sides and vertices, so this proves coverage, no overlap, no edge crossings, and face-to-face incidence. Consecutive strips share the same horizontal row-edge decomposition. The height pattern extends to both infinities. Uniform row separation1 and horizontal spacing2 imply local finiteness for any sequence, without recurrence or periodicity assumptions.

The short triangles have squared side lengths {5/4,13/4,4}, and tall triangles {4,10,10}. Their areas are1 and3. For a convex triangle the diameter is its longest side: every pair of convex combinations has distance bounded by the maximum vertex-pair distance. Thus all diameters are <=sqrt(10), with equality on each tall triangle. The source's weak inequality is essential to this example; the audit does not establish a strict-diameter variant.

## 3. Universal lower-root locality, all remote cells, and strict cap shielding

After translating any lower-row root to0 and reindexing the layers, the relevant row baselines at y=-4,-3,0,1,4 are -1-d_{-1}, -1, 0, d_0, d_0+1 modulo2. Since sqrt(10)<4, every band above y=4 or below y=-4 is disjoint from the disk. The three strips from y=-3 to4 depend only on central d_0. The only remote dependence is the short strip from -4 to-3.

At y=-3 the disk chord is the fixed base [p_-,p_+] with p_-=(-1,-3), p_+=(1,-3). Every downward cross-edge has direction v=(h,-1), h=-d_{-1} or 2-d_{-1}, so |h|<=3/2. At p_±,

p_± dot v = 3 +/- h >=3/2 >0,

and for every t>0 its squared distance is 10+2t(p_± dot v)+t²|v|²>10. These edges meet the closed disk only at their endpoint. Every other upper endpoint has |x|>=3; along its descending edge |x|>=3/2 and |y|>=3, giving squared distance >=45/4>10. The lower horizontal row y=-4 misses the disk, and outward horizontal row edges at p_± are singleton traces. These are strict exclusions of entire segments, not checks of far endpoints.

For an additional direct containment derivation, the cap triangle has vertices p_-,p_+,q with q=(1-d_{-1},-4). Put y=-3-t. Its horizontal section is [-1+(2-d_{-1})t,1-d_{-1}t], whereas the disk section is [-sqrt(1-6t-t²),sqrt(1-6t-t²)] for 0<=t<=sqrt(10)-3<1/6. For h=d_{-1} or 2-d_{-1}, 1-ht>0 and

(1-ht)²-(1-6t-t²)=(6-2h)t+(h²+1)t² >=3t.

Thus the complete circular cap lies inside that triangle, strictly away from its descending sides for t>0. Its geometric trace is exactly D intersect {y<=-3}, independent of the remote apex. No other remote triangle has a positive-area trace. This supplies an explicit whole-face argument rather than a vertex-star argument.

At EACH p_± there are exactly three positive-length edges, three singleton edges, four positive-area faces, and two singleton faces. The singleton edges are the downward side toward the cap, the other downward side, and the outward horizontal row edge. They can be distinguished without relying on their exterior slopes by their positive-face incidences: respectively cap face, no positive face, and fixed outward tall face. The two singleton faces are then distinguished by their adjacent singleton edges. This supplies a literal bijection preserving inherited vertex-edge-face incidence and the outside fan order for both remote chiralities. The geometric restriction remains ambient-isometric even when coincident singleton traces retain distinct parent-cell labels.

No interior tangency or further boundary-only piece is omitted: all edges in the fixed three strips are matched as whole edges, the remote descending edges are either strictly excluded or have one of those endpoint singletons, and the entire remote cap has just been identified. The same maps restrict to open disks.

## 4. Explicit global maps and complete local-case reduction

Reflection R(x,y)=(-x,y) maps the whole family to

d'_j=2-d_j, a'_j=-a_j+4j.

It sends L_{j,k}->L'_{j,-k-2j} and U_{j,k}->U'_{j,-k-2j-1}. For short-strip D/E triangles it sends D_{j,k}->D'_{j,-k-2j-1} and E_{j,k}->E'_{j,-k-2j}; for tall-strip D/E triangles it sends D_{j,k}->D'_{j,-k-2j-2} and E_{j,k}->E'_{j,-k-2j-1}. These are actual named whole-cell identities, including every side and vertex. The offsets satisfy the correct recurrence. In particular central chirality3/2 maps to1/2, not merely to a congruent rooted vertex set.

The half-turn H(x,y)=(d_0-x,1-y) maps the whole family to

d'_n=d_{-n}, a'_n=d_0-a_{-n}-d_{-n}.

Here a'_0=0 and a'_{n+1}-a'_n=1+d'_n. It sends L_{j,k}->U'_{-j,-k}, U_{j,k}->L'_{-j,-k}. Short D_{j,k} maps to short E'_{-j,-k}, and short E maps to short D'_{-j,-k}; tall D_{j,k} maps to tall E'_{-j-1,-k}, and tall E maps to tall D'_{-j-1,-k}. This proves the upper-root reduction globally and covers all strip incidences.

For any root v, first translate its lower-row anchor L_{j,k} to0; if v is upper, apply H; if its central chirality is3/2, apply R. This ambient isometry F_v maps its complete disk to the same canonical central-chirality1/2 restriction. Different surrounding sequences affect only the shielded cap/singleton cells, whose explicit local bijection is given above. For roots v,w the composition F_w inverse composed with F_v is the required ambient isometry. Arbitrary bi-infinite external choices are handled analytically, not by enumerating sequence prefixes.

For positive faces in the fixed region, disk intersections are convex and connected. The inward halfplanes of exactly those actual triangle sides meeting the open disk determine the clipped positive-area face. To check sufficiency, connect an interior point of the face to any hypothetical extra point admitted after deleting inactive constraints. A first exit from the triangle inside the disk would cross an actual side segment inside the disk, contradicting inactivity. Circle arcs are therefore determined by the disk and these halfplanes; closures retain their endpoints. Boundary-only faces are separately matched above.

## 5. Translation group and noncocompact full symmetry

For the supplied one-exception sequence d_0=1/2 and d_j=3/2 for j!=0, length2 edges are precisely the horizontal row edges, because neither short nor tall cross-edge length is2. Their row-line spacing pattern alternates1 and3. A translation symmetry must preserve row type, so its vertical component is4m. The unique shortest upward short cross-edge has positive horizontal component for d=1/2 and negative component for d=3/2. Translation preserves this metric detection of chirality, hence d_{j+m}=d_j for all j. A unique exception forces m=0. Every row has vertex spacing2, so the horizontal component is2n. Conversely all translations (2n,0) preserve every named cell. Thus the translation subgroup is exactly2Z x {0}.

Any full ambient symmetry preserves the horizontal length2 edges, so its linear part is one of four diagonal orthogonal matrices. The kernel of the linear-part map is exactly the translation subgroup; its index is at most4. A compact fundamental set for the full group would produce, using finitely many coset representatives, a compact fundamental set for horizontal translations. Such translates cannot cover points of arbitrarily large positive or negative height. The full group is not cocompact. No assumption that only translations need inspection is used.

## 6. Complete frozen-source and historical reproduction audit

All16 frozen attempt files were SHA-256 checked against `snapshot_manifest.json` AND byte-compared with their exact original Git objects at PR head `6b702110d1bd4b9220e2033fa5eed030911ce8c6`. All match, including candidate, both checker copies, all saved receipts, historical review/verdict, source/readiness/status records, and the turn ledger. `frozen_source_verification.json` records each path and hash. The candidate SHA matches the historical review and verdict; the submitted checker matches its archived review copy.

Historical scripts were copied to three separate ignored run directories so their automatic writes could not alter frozen artifacts. Submitted `verify.py` and `review/submitted_verify.py` each pass16 rooted cases and reproduce saved `verification.json` byte-for-byte. Historical `review/independent_checks.py` passes212 assertions across64 rooted cases and reproduces its `independent_results.json` byte-for-byte. First-party reproduction receipts retain exact script/output hashes, exit codes, stdout and stderr.

The historical independent script compares positive-face counts, not their full geometry, while the submitted script compares active oriented halfplanes. The historical report explicitly relies on both and its analytic argument. That limitation does not invalidate the claim, and the new independent certificate below checks positive-face geometry and all inherited incidence pairs directly.

Provenance/budget disposition is conservative: frozen `turns.jsonl` contains exactly one turn, labeled `scoped_candidate`; frozen status uses1/5 and says `full_source_solved=false`, `new_discovery_claim=false`. The exact-head queue says `unsolved | 1/5`, while the base says `queued | 0/5`. The original reported model/effort labels are archival provenance, not independently retrievable model execution attestations. No attempt counter was reset or incremented by this audit. No target-group occurrence for10000062/AMR-099-0062 was found in the present related-target-group file; this is a bounded exact-ID check, not a worldwide duplicate certificate.

Required metadata repair: frozen README's final sentence says no shared queue/catalog/state files are changed, but this original PR changes QUEUE.md and advances its row to unsolved1/5. This sentence is stale at the frozen PR head. The reviewed package should state the actual queue update (or remove the inaccurate sentence) while retaining the1/5 partial/unresolved status. Historical frozen bytes should remain preserved. This is not a mathematical repair and does not authorize silently rewriting historical review evidence.

## 7. New exact rational controls and full-cell certificate

`full_cell_checks.py` imports no historical verifier and uses only the standard library with fractions.Fraction. Its final run passed1398 assertions. It exhausts128 seven-bit assignments at both row types (256 cases), including nonconstant continuations outside the enumerated window, and16 additional roots with shifted layers and far horizontal indices. These finite comparisons supplement the universal proof, not replace it.

For each root, the complete certificate has8 original vertices,28 positive-length edge pieces,6 singleton edge cells,23 positive-area face pieces,4 singleton face cells, and164 inherited vertex-edge/edge-face/vertex-face incidence pairs. The34 edge keys and27 face keys each have multiplicity1 after distinguishing singleton cells by their positive-face incidences and adjacent edges. Thus equality supplies an explicit cell bijection rather than a histogram. `canonical_cell_certificate.json` lists all geometric keys and incidences: full endpoints for positive edges, inward active halfplanes for positive faces, and exact singleton points with incidence identities. Circle arcs follow from those halfplanes and the common closed disk.

The exact generic classifier also checks a triangle whose only trace is an interior-edge tangency at(1,3), with no original vertex inside the disk, and a triangle containing the entire disk with no visible edge or vertex. This challenges nearest-vertex shortcuts and the center-inside case. Every baseline face-side halfplane is checked to contain its endpoints and orient strictly toward its opposite vertex.

New controls, distinct from the historical squared-radius1001/100 control:

| Mutation | Exact detection and meaning |
| --- | --- |
| Squared radius10+1/4096 | Changing preceding chirality changes canonical full-cell signatures while rooted vertex sets remain equal. This refutes radius-flexibility of the prescribed proof; it does not exclude every other isometry at a larger radius. |
| Squared radius10-1/4096 | Tall triangles still have squared diameter10, so the full target diameter hypothesis fails even if local disks could remain congruent. |
| Discard all singleton traces | Vertices and positive-edge/positive-face counts remain unchanged, but the full restricted-cell/incidence signature fails. |
| Tall-strip shift9/8 | Both the diameter bound and the prescribed reflected congruence fail. The isosceles shift1 cannot be casually altered. |
| Omit chirality reflection | All piece counts remain unchanged, but the canonical geometry/incidence signature differs. |
| Flip the cap halfplane | The exact point(0,-25/8), with squared distance625/64<10, belongs to the true cap and is excluded by the reversed inequality. |

No negative control is promoted beyond what it actually checks. In particular, the larger-radius test is a canonical-map failure, not a new classification of all possible larger-disk isometries.

## 8. Strongest verified result and exact remaining gap

The strongest verified result is the supplied specialization of a prior layered Euclidean family: every closed vertex-centered radius-sqrt(10) disk has the same complete restricted triangulation, all triangle diameters are at mostsqrt(10), and the one-exception member has translation group exactly2Z x {0} and a noncocompact full symmetry group. No mandatory geometric correction to frozen CANDIDATE was found.

It is a counterexample to the explicitly named Euclidean cocompact/crystallographic conclusion. It has a horizontal translation and is not strongly aperiodic. For the weaker Euclidean convention of at least one nonzero translation, it is not a counterexample; the prior planar monocoronal theorem already applies because the diameter bound places each entire incident triangle inside its root's closed disk. The source does not determine which periodicity convention was intended. The hyperbolic full metric-ball clause remains untreated, and prior corona/rhombus constructions cannot supply it without the missing full-ball verification. Novelty of the specialization and historical first priority are not established by this geometric audit.

Classification: verified, attributed, explicitly scoped Euclidean partial result; original exact-source status unresolved,1/5 preserved. No paper, DOI, release, publication or contact is recommended or performed by this family. Audit completion estimate100%; original-source completion is not assigned100%.
