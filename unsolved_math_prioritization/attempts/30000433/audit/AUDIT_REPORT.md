# Independent adversarial audit: five-or-six edge-degree triangulations

Problem 30000433 / OWR-1194-002, catalog rank 812. 6 October 2026 UTC.

## Verdict

**Accept the scoped partial results with the separate A1 quotient-certificate supplement. The source problem remains UNSOLVED; four substantive approaches have been used.**

The frozen author archive passes all original replay and mutation tests. The independent reconstruction reproduces every stated numerical result and the supporting geometry. One narrow omission in the self-handle certification was identified and repaired in this audit supplement: an abstract simplicial quotient needs a check for unintended identifications between different simplices, in addition to a no-collapsed-simplex check. The required condition holds in the actual example, and no topology, count, or universal-problem status changes. See `CORRECTION.md` and `verify_quotient_guard.patch`.

The original freeze is unchanged. This audit is independent AI-assisted mathematical/code review, not human peer review or formal proof-assistant certification. No novelty or priority is established.

## Immutable input and full-record matching

The author ZIP has 21,187 bytes and SHA-256 `b64c3b92a96f180b51d22ddd343e9458fc7181f7d8117d5117a4b6a7215dcdf7`. Its manifest SHA-256 is `ac8006591dde3c8d85cbf2bc47dcb375f7b572107c159bc9a4118e16b8ed0873`. Every declared member size and hash was checked. Its ten-member inventory matches the supplied freeze receipt.

The three complete corpus files were independently hashed and the entire target record and associated report entry were reviewed. The report is absent and is represented as `{}`. Default Python `json.dumps([record, report], sort_keys=True)` produces 3,552 UTF-8 bytes with SHA-256 `48336d46884d5c1b7cb087f2ca3c3a5f5c2426fd761e15572df88dc93e303f94`, exactly matching the catalog. Rank, ID, problem number, and zero prior substantive approaches in the catalog agree. Public hashes and source-inspection metadata are in `SOURCE_CHECKS.json`; corpus contents are excluded.

## Source identity and bounded prior checks

Fresh inspection of Sullivan's Problem 5 on printed p. 693 (PDF page index 40) confirms two separate questions: universal edge degrees 5/6 and the stronger TCP restriction on degree-six edges. The question itself leaves closedness, orientability, and the exact triangulation category implicit. The note expressly limits its results to finite closed abstract simplicial PL 3-manifolds, with balls identified separately. Its elementary lemmas need no orientability; its explicit examples are orientable. This scope is sufficient for the claimed partial results and does not purport to answer all categories of the source question. [Original report](https://ems.press/content/serial-article-files/46044)

The Brady–McCammond–Meier theorem has closed orientable hypotheses and permits degree four. It does not eliminate degree four. [Author PDF, Theorem 1.2](https://math.ou.edu/~nbrady/papers/edgedegrees.pdf)

The Elder–McCammond–Meier condition instead limits degree-five edges in each triangle; its conditional word-hyperbolicity theorem cannot be substituted for TCP existence. [Author PDF, Definition 1.1 and Theorem 1.2](https://web.math.ucsb.edu/~mccammon/papers/thurston.pdf)

The Lutz–Sulanke–Sullivan 2007 report explicitly discusses closed TCP triangulations and includes products of surfaces with S1 and spherical examples among known families. Thus the S3 and S2 × S1 examples here are controls, not new topological existence results. [Report, printed p. 229](https://ems.press/content/serial-article-files/46090)

The 2026 Huszár–Maria theorem gives maximum valence nine with treewidth control and uses tetrahedron face-pairing triangulations. It supplies neither the 5/6 conclusion nor a strict simplicial certificate for these examples. [Official paper, Theorem 2 and Section 2.2](https://drops.dagstuhl.de/storage/00lipics/lipics-vol367-socg2026/html/LIPIcs.SoCG.2026.58/LIPIcs.SoCG.2026.58.html)

Read-only repository searches for the exact ID in code and pull requests and the exact problem number in issues returned no target-specific results. Four fresh web discovery queries, alongside the primary-source inspections above, located no full resolution. These are bounded checks, not exhaustive proofs of current openness or historical priority. Direct access to the target UnsolvedMath page again failed; the full supplied record and primary report establish the target independently. No remote state was changed.

## Claim-by-claim mathematical audit

### 1. Link curvature and TCP

Accepted. A closed PL vertex link is a simplicial 2-sphere, so Euler's identity yields total valence defect 12. With valences only 5 and 6, exactly twelve link vertices have degree five. Endpoint double counting yields E5 = 6V. Closed 3-manifold incidence and Euler characteristic then give T = 5V + E6.

Under TCP, the degree-six vertices in a vertex link form an independent set. Around a degree-five link vertex the neighboring vertices form a 5-cycle, whose independent sets have at most two members. Counting incidences between the two link vertex classes gives 6q ≤ 24. Therefore q ≤ 4, E6 ≤ 2V, and 5V ≤ T ≤ 7V. No orientability is used. The note correctly avoids asserting a complete link classification or that all values q = 0,1,2,3,4 occur.

### 2. Stellar and Pachner barriers

Accepted. In a positive-dimensional stellar subdivision, a new edge has degree three for a tetrahedron or four for a triangle or transverse edge of a subdivided edge star. In a nonempty finite sequence of such moves, the final move supplies the obstruction. This does not apply to arbitrary subdivisions, welds, or compound changes.

For ordinary 3-dimensional Pachner moves, 1–4 and 2–3 introduce degree-three edges, while 3–2 and 4–1 require one. Consequently the minimum-degree-four class has no edges in its induced single-Pachner-move graph. Paths temporarily leaving the class remain possible. No stronger obstruction is justified or claimed.

### 3. Octahedral replacement size

Accepted. An interior vertex in the proposed ball has a spherical link of minimum valence five, hence at least twelve neighbors. With only six boundary vertices, at least seven interior vertices are necessary. If there is no interior vertex, any tetrahedron on the octahedral boundary vertices must use an opposite-vertex diagonal. This is an interior edge whose cyclic link has at most four vertices, contradicting the minimum-degree-five hypothesis. The unsubdivided-boundary hypothesis is essential and is stated. No existence at the lower bound is implied.

### 4. Conditional gluing, geometry, and topology

The two-summand induced-boundary hypothesis is sufficient. After each vertex star is removed, a seam edge loses exactly two incident tetrahedra per side. Its new degree is d1 + d2 − 4. Since each old degree is 5 or 6, the result stays within 5/6 exactly when every paired old seam edge had degree five. Nonseam edges retain their degree. All seam triangles then have three degree-six edges and violate TCP. Removing tetrahedra instead would produce seam degree at least eight. These statements are conditional and do not provide matching links in arbitrary manifolds.

The 600-cell verification is a genuine convex-boundary certificate. The positive-definite Gram matrix gives affinely independent facet vertices; all other listed vertices lie strictly behind each supporting plane. The axis vertices imply a full-dimensional hull with the origin inside. Since every selected triangular ridge has two selected incident facets and the convex hull's facet adjacency graph is connected, the selected facets exhaust the hull boundary. This proves S3, rather than inferring S3 from homology. Cyclic edge links, connected closed vertex-link surfaces with Euler characteristic two, and coherent orientation were checked independently.

The doubled puncture is a connected sum of two certified PL spheres along an induced icosahedral boundary. Opposite summand orientations make the boundary map reversing, so the result is S3.

For the self-handle, A1 supplies the full simplex-fiber check. There are exactly the prescribed 12 vertex, 30 edge, and 20 triangle identifications and no other collisions. The two puncture boundaries are induced and disjoint, and their union is the whole boundary of the complement. The given linear symmetry is an involutive full simplicial automorphism. The independent oriented-chain calculation verifies reversal on all 20 boundary triangles, not merely orientability of the final output.

Removing two disjoint open PL balls from a PL S3 gives S2 × I. Identifying the ends with a map reversing their induced boundary orientations gives the orientable S2 bundle over S1, hence S2 × S1. The standard PL sphere-bundle classification, equivalently isotopy of orientation-preserving PL self-homeomorphisms of S2 to the identity, is an explicit mathematical input. Mod-2 homology is only a corroborating check. As a negative control, gluing by the antipodal map gives a nonorientable quotient, which the author analyzer rejects.

## Independent exact computations

The audit code regenerates coordinates in Z[sqrt(5)] scaled by two from the author's Z[phi] coordinates, uses its own clique enumeration, determinant computation, support checks, link analysis, orientation propagation, quotient-fiber enumeration, and mod-2 boundary-matrix reduction. It imports author routines only for direct comparison and rejection controls. This is a separately implemented check of the same mathematical construction, not a proof assistant or independent discovery of the 600-cell.

- Geometry: 120 vertices, 600 facets; 72,000 exact support comparisons, 69,600 strict comparisons, 2,400 equalities; all 600 facet determinants nonzero.
- Classical 600-cell: f = (120,720,1200,600); 720 degree-five edges; mod-2 Betti vector (1,0,0,1); no TCP violations.
- Doubled puncture: f = (226,1386,2320,1160); 1,356 degree-five and 30 degree-six edges; mod-2 Betti vector (1,0,0,1); exactly the 20 seam triangles violate TCP.
- Self-handle: f = (106,666,1120,560); 636 degree-five and 30 degree-six edges; mod-2 Betti vector (1,1,1,1); exactly the 20 seam triangles violate TCP.
- Exact field-sign tests: 40,401 coefficient pairs checked against a certified rational enclosure of sqrt(5), and the author's phi sign routine compared through the change of basis.
- Independent negative controls reject deleted, repeated, and collapsed tetrahedra; the wrong-orientation self-handle is detected.

## Replay, mutation resistance, and boundaries of assurance

The original verifier passes normal Python, `-O`, and external-manifest-pinned runs. Both original test-driver modes pass relocated execution, 16 semantic mutations and four anchored integrity mutations per driver, with restored-clean checks. The independent checker passes normal, optimized, and relocated paths containing spaces, with identical JSON output. The separate patched verifier produces exactly the original mathematical result in normal and optimized modes; it correctly fails the old author manifest pin.

`audit_replay.py` reruns these checks from the exact author ZIP, applies the correction only to a temporary copy, and exercises four quotient-guard negative controls. Normal and optimized audit harness results are included. A hash manifest needs an external trust anchor; an attacker allowed to replace both code and that anchor is outside this assurance model. Code testing and finite examples cannot establish universal existence.

## Acceptance conditions and remaining gap

Keep A1 with the frozen note whenever claiming the self-handle is fully certified, or incorporate its text and code into a newly versioned author package. Retain all explicit scope, novelty, and review limitations. Leave the universal source problem UNSOLVED, with four of at most five substantive approaches used. The missing global construction or counterexample remains exactly as described by the author. This audit correction is a certification repair within the fourth approach, not a fifth substantive approach.
