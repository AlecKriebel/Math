# PR36 original16: independent graph and dynamics audit

**Verdict: PASS for the original graph and dynamics argument, using the explicitly imported established critically-fixed realization/classification theorem. No fatal gap found in this family.** The finite checks are a reproducibility certificate for graph data, not a certificate for the analytical imports, proof prose, historical novelty, or an explicit rational-map formula. This verification adds **0 substantive research attempts** and does not change candidate science.

Frozen head: `35be7fe58a2832c4d7012cf69c973810fb4c42f8`. Actual base: `01358d66fc67d1c462bddf31c0d4ee5b120e6737`. All 16 numeric-path artifacts and the 17-path diff are bound to this scope. Original candidate SHA256: `aa598dc779b4115c9a7522335b364a5d9dcddf11ceec707fd46943984e8ffabf`.

## Literal scope and independence

AIM Problem 2.6 asks whether all PCF maps are defined over their field of moduli. I read the full frozen `source_record.problem` and recovered the live primary title and question publicly by curl before reading CANDIDATE. It has no extra odd-divisor, rigidity, portrait-size, or degree assumption. One algebraic PCF conjugacy class with non-definable field of moduli suffices for a negative answer.

Exposure deviation is explicit: the first read of the entire source_record also displayed its upstream prior report. That introduced odd-divisor/Silverman context before live primary retrieval, so this run is not perfectly source-first unexposed. I did not read the original graph checks/results/diagram, old graph review, siblings, or root interpretations before sealing my reconstruction. I still have not read sibling/root findings. The literal scope seal and independent proof-assessment seal are preserved separately and hashed in the source ledger.

## Embedded graph and complete symmetry calculation

Use cycle vertices 0,1,2,3, with pendant paths 0–4, 1–5–6, 2–7, 3–8–9. Quarter-circle tangents and the stated radial coordinates give exact counterclockwise rotations:

| Vertex | Neighbor order |
|---|---|
| 0 | 3,1,4 |
| 1 | 0,2,5 |
| 2 | 1,7,3 |
| 3 | 2,8,0 |

There are ten vertices, ten edges, one cycle, two faces, and degree multiset 1,1,1,1,2,2,3,3,3,3. Every abstract automorphism preserves the unique cycle and alternating pendant lengths. Restriction to the cycle is therefore id, h:j↦j+2, s0:j↦−j, or s2:j↦2−j modulo 4, with forced extensions down paths. Complete orientation-sign lists are:

| Cycle action | Signs at vertices 0,1,2,3 | Possible ambient orientation |
|---|---|---|
| id | +,+,+,+ | preserving |
| h | −,−,−,− | reversing |
| s0 | −,+,−,+ | none |
| s2 | +,−,+,− | none |

This proof is independent of a numerical search. My exact implementation also exhausts all 1,152 degree-compatible vertex permutations and obtains the same four full permutations and signs. The graph is simple, so vertex action determines each edge action. The preserving induced action is identity; the reversing action h fixes no vertex or edge and exchanges the two faces. These statements concern induced permutations; there remain sphere homeomorphisms supported away from the graph.

J(z)=−1/conjugate(z) sends every rational coordinate to the claimed partner, maps the actual circle/radial arcs accordingly, and exchanges inside with outside. Under the exact stereographic sphere formula it sends every point to its antipode, so it is a fixed-point-free antiholomorphic involution globally, not only on the vertex list.

The original SVG was parsed separately. Its cycle circle and pendant path agree with the coordinates under (x,y)↦(270+75x,180−75y); all ten marker centers agree using exact fractions. The diagram and prose therefore define the same embedding and cyclic orders.

## Realization and naturality

The full independent reconstruction is in `proof_assessment_seal.md`. The accepted input is the orientation-preserving graph classification, together with its intrinsic inverse fixed-ray/charge construction. Source proofs were read rather than inferring equivariance from the word “bijection.” The realized class has degree 11, ten fixed critical points, local degrees 2,2,2,2,3,3,4,4,4,4, and ramification sum 20=2·11−2. Its postcritical set is those ten vertices. No local degree is 11, so no polynomial conjugate exists. Its ten fixed critical orbifold weights are infinite and the orbifold Euler characteristic is −8, excluding flexible Lattès behavior.

A commuting conformal basin map is a disk rotation fixing the center; commutation with the monomial forces a root-of-unity factor. An anticonformal basin map is the corresponding antirotation. Both permute the entire intrinsic union of fixed internal rays. Charge edges are indexed by Tischler faces, their endpoints are the two distinct critical boundary points, and their cyclic order is the order of incident face sectors. Changing arcs within disjoint simply connected faces preserves this data and gives an isomorphic embedded charge graph. Thus existing dynamical automorphisms necessarily act uniformly on the charge rotation system. This does not assert that every abstract graph automorphism lifts.

Complex conjugation mirrors immediate basins and fixed rays and therefore mirrors the charge class. The map cJ gives an orientation-preserving isomorphism G→cG. Classification supplies cfc=L f L⁻¹, hence A=L⁻¹c commuting with f. Holomorphic automorphisms have identity charge action, hence fix ten critical points and are identity. It follows that A²=id and A is the unique antiholomorphic dynamical automorphism; its induced reversing action is h.

Each charge edge labels a Tischler face. Since h fixes no charge edge, the ten Tischler faces form five distinct A-pairs. Choosing one arc in a pair and its A-image in the partner gives an actual A-invariant charge graph. It is connected by the source construction and has no A-fixed point: vertices are paired and distinct edge interiors lie in distinct face interiors. A reflection's fixed circle separates the sphere into two disks it exchanges, so no connected nonempty invariant graph avoiding that circle exists. A therefore is fixed-point-free. A real model would supply a commuting reflection, contradicting uniqueness of A.

The order of these dependencies is sound: trivial holomorphic group precedes A²=id, which precedes equivariant arc choices; graph action uses intrinsic Tischler sectors before an invariant arc choice. No circular assumption of an already invariant chosen charge graph occurs.

## Closure of the original question

The seal independently checked the finite normalized critically-fixed algebraic locus argument. The equation W|H²⁰ correctly forces critical support into the fixed-point set in degree 11 on the nonzero-resultant locus; the quotient has degree 220. Finitely many plane graphs with ten edges give finitely many conjugacy classes, and finitely many critical triples give finitely many normalized representatives. A finite constructible Q-defined locus has algebraic coordinates. Drawing coordinates do not imply coefficient algebraicity.

Post-seal old-review inspection made one transition explicit that is implicit in the candidate and sealed outline: a complex Möbius conjugator between two algebraic maps is algebraic here. Their critical points are algebraic; select three distinct critical points and their three images. The unique transformation carrying one algebraic triple to the other is over Qbar. I independently checked this elementary clarification after reading it; it neither changes the construction nor introduces a fresh research route.

For an algebraic representative, the class stabilizer contains an open coefficient-field Galois subgroup and thus has number-field fixed field K. Conjugation belongs to the stabilizer, so K⊂R in the chosen embedding. A K-model would be a real model and is impossible. This is enough for the literal universal question. No exact K, coefficients, quaternion computation, total-reality claim, minimum degree, or historical novelty follows or is needed.

## Original artifacts and unchanged replay

`original_binding_and_replay.json` records:

- Every original16 byte string matches snapshot SHA256, size, Git blob, and the exact frozen head path.
- The 97,918-byte diff's SHA256 and ordered 17-path list match the parent snapshot manifest.
- Unchanged `verify_graph.py` replay stdout matches every byte and the full parsed JSON of `graph_verification.json`.
- Unchanged old `review/independent_checks.py` replay matches every byte/full JSON of `review/independent_results.json`, including all 183 assertions and 39 search nodes.
- All original review-summary/status hash links agree; the old review has the original candidate hash.
- Full independently derived permutation/sign maps, cyclic rotations, and charge face cycles match original diagnostics, allowing only cyclic starting-point changes.
- Independently retrieved Hlushchanka v2 PDF exactly matches original `source_manifest.json` reference hash `67890033472cb3bb4187936f4d34e6c59d0487cbf71eda9e8c98f6b887755950`.

The graph family did not redownload the other four original foreign-reference files and does not claim to reproduce their hashes. Primary-reading locators, version pins, hashes, retrieval failures and successful public recovery are in `source_reading_ledger.json`. Downloaded foreign sources are excluded from the authored manifest and ignored from version control.

## Executed exact and corruption controls

The original graph is not promoted merely because a checker prints PASS. `packet_coverage_results.json` records ten actually materialized and executed mutant packets, using the original check programs unchanged wherever the mutation is prose/source:

| Executed mutation | Original finite-code outcome | Additional coverage |
|---|---|---|
| Literal question narrowed to rigid/odd-divisor subclass | both outputs unchanged | original source hash rejects |
| Candidate degree changed to 12 | both outputs unchanged | candidate hash rejects |
| Candidate falsely claims fixed faces/arbitrary invariant arcs | both outputs unchanged | candidate hash rejects |
| Candidate holomorphic group changed to order 2 | both outputs unchanged | candidate hash rejects |
| Saved ramification receipt changed to 19 | fresh outputs unchanged | full receipt comparison/hash rejects |
| SVG vertex coordinate changed | outputs unchanged | SVG binding/hash rejects |
| Primary citation hash replaced with zeros | outputs unchanged | citation binding rejects |
| Operative theorem text broadened to disconnected/loop graphs | outputs unchanged | source bytes differ; read theorem necessary |
| Original hardcoded rotation corrupted | original assertions reject | actual graph data covered |
| Old independent check coordinate corrupted | old assertions reject | exact coordinate data covered |

The theorem-text mutant lives privately with foreign sources. A hash failure establishes changed data, never false mathematics. Both original scripts read neither candidate prose, source statement, source manifest, SVG, nor saved receipts; these outcomes are expected scope limitations, not newly discovered scientific counterexamples to the candidate.

My own 16 embedding controls enumerate all four local order choices on this same abstract graph. All-inside has two preserving/two reversing actions and fails rigidity. A one-vertex order flip has one of each type but its reverse fixes vertices/edges, failing the invariant-graph-free-action step. My first prediction that this latter control was chiral was false; the exact first-failure record is preserved and the expectation was corrected. These controls show that orientation counts alone are insufficient.

Exact boundary controls also compute five disjoint edges: degree 6 with ten proposed distinct critical fixed points exceeds the degree-7 fixed-point form, so a connectedness-free realization claim cannot hold. One loop would give total degree 2 but local degree 3 at its sole vertex, which is impossible. These concrete falsifications show the source hypotheses matter; finite controls never prove the universal source theorem.

## Limits and deliverables

The mechanism is a graph-defined critically-fixed PCF class with a unique free antiholomorphic involution. Evidence comprises the sealed reconstruction, primary proof readings, exact geometry/automorphism calculations, original byte replays, and actual false-prose/source controls. The original graph/dynamics route is not blocked; no unsupported equivalent central claim was substituted.

All work is in this dedicated family folder. No outside individual was contacted; no branch switch, candidate science edit, shared queue/state/history change, remote write, preprint, acceptance action, or DOI occurred. The original turn count stays 1/5. This report is independent mathematical verification, not historical priority or formal/peer review.

Reproduce from the repository root:

    python3 draft_pr_publication_program_20260930/audits/pr36_20001424/graph_family/independent_graph_audit.py
    python3 draft_pr_publication_program_20260930/audits/pr36_20001424/graph_family/replay_and_binding.py
    python3 draft_pr_publication_program_20260930/audits/pr36_20001424/graph_family/packet_coverage_controls.py

The primary-theorem-text control reruns when the private retrieved text exists; its original execution receipt and source hashes remain in the delivered JSON when sources are unavailable. Authored closure is hashed by `authored_manifest.json`, which excludes itself, foreign sources, caches, and temporary files.
