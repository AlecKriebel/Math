# Independent mathematical, source, and artifact audit

Problem 5500072 / AMR-054-0072, queue rank 929: Polyhedron with Regular Pentagon Faces.

## Decision

**Accept the original frozen packet unchanged as a bounded partial investigation.** Proposed disposition remains `stalled_partial`, equivalent to an unresolved/unsolved queue entry, with 3 of 5 approaches used. No proof or counterexample to the original global question has been supplied. No novelty claim is accepted or requested. No mathematical correction to the author packet is necessary. A provenance-only correction to this audit is documented in `PROVENANCE_CORRECTION.md` and its actual patch. The independent acceptance in this packet supersedes the original packet's historical “audit pending” label without editing any original byte.

The accepted local theorem is correct: in the stated flat-face, edge-to-edge model, a four-valent vertex cannot have two cyclically adjacent incident edges whose other endpoints are trivalent. Its stated graph corollary, incidence identities, trivalent rigidity calculation, and flexible local-star construction also pass review. These findings do not establish a dodecahedral decomposition.

## Review provenance

This is an independent AI mathematical, source, and artifact review, supplemented by separately authored executable checks. It is not human peer review or formal verification. Earlier audit metadata incorrectly called this human review; that label has been corrected without changing the mathematical findings or any author artifact.

## 1. Exact target and provenance

The accepted author ZIP is 14,851 bytes, SHA-256 `da58c09682631f3455d7ef0047ff20b137f2c8b14640752f9886bb4dfc4bfb62`. Its external manifest is 1,680 bytes, SHA-256 `88771594f5b6c2aabe33513345ca2b70786984448cfa17d5ed7bbc5ffe122f95`. The original bootstrap is 3,419 bytes, SHA-256 `590cf2095337c31144dc04bff20baf9fede8a6d8ea96fdf4fc92aea3205c9841`.

All eight original members were independently checked against the manifest and read in full: README, proof note, research report, status, diagnostics, source metadata, recorded validation, and replay record. The ZIP inventory is exact, unique, flat, and CRC-valid. The original files remain unchanged. All executable source was inspected before execution.

The complete catalog, problem, and report corpora were independently hashed and parsed, not replaced with selected-record extracts. Their sizes are respectively 21,735,099; 68,931,837; and 80,334,822 bytes, with 15,458; 15,458; and 6,701 records. Their hashes match the author's supplied pins; full details are in `audit_replay_results.json`. Unique target records agree on rank, ID, problem number, and title.

The two-element whole problem/report list, serialized with `json.dumps(..., sort_keys=True)` and otherwise default options, is 3,943 bytes and hashes to `8b339393cebf5ccaee4df9fcd5290875ff54c34aa811cee58f9041e9d54df4c5`. The statement hash and whole inherited-report hash also match independently. A change to a nonstatement record field changes the pair digest. The inherited report was independently read in full by an AI reviewer: it contains literature/status triage, not a substantive proof attempt. Its unsubstantiated aside about an “icosahedron-type” classification is not adopted as a theorem or used in this audit.

This audit does not refresh GitHub repository search or certify a later queue state. The queue blob and searches in the author packet remain historical observations. No repository, queue, or external document was modified.

## 2. Source reconciliation

Fresh direct retrieval independently reproduced the exact bytes of all five pinned public sources, including the three PDFs. Retrieval times, sizes, hashes, URLs, and inspection scope are recorded in `source_verification.json`. The three decisive pages were freshly rendered and visually read as well as textually inspected. No source PDF, page image, extracted source text, or corpus content is distributed here.

- [Oberwolfach Report 12/2006, Discrete Differential Geometry](https://oa.tib.eu/renate/server/api/core/bitstreams/5e8dec33-aefd-438d-8e6d-7517a9a00a61/content), Problem 4, printed p.693, PDF page 41: the original question concerns a spherical polyhedral surface realized by equal regular pentagonal faces. It permits intersections between different sheets and rules out coincident distinct faces. It expressly leaves the meaning of the dodecahedral union to be specified appropriately. Thus an argument for a conventional embedded boundary cannot silently replace this immersed problem.
- [Günter Rote, Open Problems in Discrete Differential Geometry](https://page.mi.fu-berlin.de/rote/Kram/OWR-DDG09-problems.pdf), Problem 2 and Ulrich Brehm's note, p.1: the restatement preserves the preceding distinction. Brehm explains that the great dodecahedron has genus four and fails immersion at vertices because of its self-crossing pentagram links. The note separately discusses relaxing local embedding at vertices. This directly supports the author's source correction.
- [TOPP Problem 72](https://topp.openproblem.net/p72): the fresh maintained page still labels the problem open and also calls the embedded variant open. Its assertion that the great dodecahedron is immersed conflicts with Brehm's explanation under the standard locally embedded interpretation. The genus obstruction already prevents that object from answering the spherical question.
- [Arseneva, Langerman, and Zolotov, A Complete List of All Convex Polyhedra Made by Gluing Regular Pentagons](https://arxiv.org/abs/2007.01753), arXiv v1, p.1; [published version](https://doi.org/10.2197/ipsjjip.28.791): the abstract and introduction permit interior folding of the polygon pieces. This convex metric-gluing classification does not settle the present immersed flat-face question. The audit checks this scope distinction, not the complete classification proof.

The UnsolvedMath live page was not independently re-opened in this audit; the author's disclosed HTTP 403 remains an access limitation. Fresh searches using Kenyon/pentagons/dodecahedra, immersed regular-pentagon surfaces, and four-valent regular pentagons found no established global resolution within their bounded scope. Neither the search nor TOPP's status is an exhaustive proof about all literature.

## 3. Scope of the model

The proof explicitly assumes a finite closed edge-to-edge polygonal cellulation of an abstract sphere, an isometric realization of every face as a convex planar regular pentagon, and local embedding at every abstract point. Global image intersections remain allowed. No two distinct faces may have the same image.

These assumptions are a natural precise flat-face interpretation of “polyhedral surface” in the original sources. However, those short source statements do not explicitly supply every combinatorial convention, particularly full-edge incidence. The audit therefore accepts the theorem conditional on the stated model; it does not assert an equivalence with every possible broader reading. Non-edge-to-edge tilings, folded pentagonal pieces, branching, and the weaker vertex-crossing variant are outside the accepted scope. The restriction to valences three and four applies only to the final graph corollary, not to the local four-valent obstruction.

Local immersion is essential to interpreting vertices and incidences correctly. An accidental crossing of two image sheets is not an additional abstract vertex. Reversing normals or crossing another sheet does not change the two planes of the two abstract faces incident to a given edge.

## 4. Independent mathematical verification

### 4.1 Incidence and low valence

A unit straight edge cannot form a loop. In the regular polygonal cellulation, a closed surface has at least two incident sectors at a vertex. With precisely two sectors, both are convex 108-degree sectors on the same two incident rays. The rays determine their plane and the same smaller angular sector. Consequently the two regular pentagons coincide near the vertex, already violating local embedding; in fact their unit corner edges determine the same complete regular pentagon. Thus every vertex has valence at least three.

For counts n_d, full-edge incidence gives 5F=2E and sum d n_d=2E. Combining these with V-E+F=2 yields sum (10-3d)n_d=20, hence

- n_3 = 20 + sum over d>=4 of (3d-10)n_d;
- F = 12 + 2 sum over d>=4 of (d-3)n_d.

The angular defect is 2pi-d(3pi/5)=(10-3d)pi/5, consistent with total defect 4pi. In particular n_3>=20. A face that is not entirely trivalent contributes at least one incidence with a higher-valence vertex, so the number N_0 of all-trivalent faces satisfies N_0 >= F-sum d n_d over d>=4. Substitution gives the author's 12+sum(d-6)n_d bound. It may be nonpositive and cannot guarantee a removable cap. Algebraic incidence fixtures are not realizability certificates.

### 4.2 Trivalent rigidity and propagation

Put q=(sqrt(5)-1)/4, the positive root of 4q^2+2q-1=0. It lies strictly between 0 and 1/3. At a trivalent vertex, every pair of outgoing unit edge rays bounds one pentagon corner, so each pair has dot product -q. The Gram eigenvalues are 1+q, 1+q, and 1-2q. All are positive, so the rays have rank three and are unique up to an orthogonal transformation. Each ordered pair of rays fixes the convex regular pentagon corner in their span. This establishes local rigidity only.

For adjacent face normals formed as cross products of two rays, the cross-product identity gives an absolute normal dot product of (q+q^2)/(1-q^2)=q/(1-q)=1/sqrt(5). Opposite sign choices for either normal merely change the sign before taking absolute values. Because the two incident faces are individually planar, their planes and this invariant are constant along the whole straight edge. It is therefore inherited at the edge's other endpoint whenever one endpoint is trivalent. No transport of a consistently oriented normal field is assumed.

### 4.3 Four-valent Gram obstruction

At a four-valent vertex, label rays by the abstract cyclic face order. Consecutive ray dot products are -q. Let a=u_1 dot u_3 and b=u_2 dot u_4. Their symmetric Gram matrix has diagonal 1, cyclic-neighbor entries -q, and opposite entries a,b. The vectors lie in R^3, so its determinant must vanish.

The difference vectors of coordinate positions 1 and 3, and of positions 2 and 4, have eigenvalues 1-a and 1-b. The complementary sum-pair block has matrix with diagonal 1+a,1+b and off-diagonal -2q. Therefore the determinant is

(1-a)(1-b)((1+a)(1+b)-4q^2).

Along u_2 the two normals can be taken proportional to u_1 cross u_2 and u_2 cross u_3. Their scalar product is (q^2-a)/(1-q^2). Along u_1 the analogous expression replaces a by b. The same two expressions recur at opposite edges. A trivalent other endpoint on one selected edge forces the absolute value of the relevant expression to equal q/(1-q), giving precisely a=-q or a=1/2. A cyclically adjacent selected edge gives precisely b=-q or b=1/2.

Both possible values are less than 1. Each is at least -q, so the last determinant factor is at least (1-q)^2-4q^2=q^2>0. All factors are positive, contradicting rank at most three. This proves the proposition.

As an independent numerical-free cross-check, direct elimination in Q[q]/(4q^2+2q-1) gives these determinants in the order (-q,-q), (-q,1/2), (1/2,-q), (1/2,1/2):

- (1+q)/8;
- (5+6q)/16;
- (5+6q)/16;
- (5+8q)/16.

Every one is positive. An independently coded universal polynomial determinant identity was also checked before specializing q. These computations do not import the author's arithmetic or determinant routine.

### 4.4 Reflex, orientation, and degeneracy checks

The absolute plane-normal invariant includes both signed normal possibilities. It therefore does not silently assume convex dihedral angles, globally compatible outward normals, or one choice of reflex versus nonreflex side. Reflection of a star is included in orthogonal congruence. Face planes cannot change along a full edge while remaining planar faces.

The determinant calculation exhausts all four combinations of the two possible opposite dot products. A degenerate rank-two or rank-one star would still have determinant zero, so degeneration cannot avoid the contradiction. The formal factors a=1 and b=1 would identify opposite rays, contradicting the local embedding assumptions; independently, neither belongs to the propagated candidate sets. Crossings of a spherical vertex link do not alter the Gram equations, but such crossings fail the stipulated immersion model and are never used to manufacture a valid example.

### 4.5 Graph corollaries

Among four cyclic incident positions, a subset containing no adjacent pair has size at most two; if it has size two, those positions are opposite. Thus at least two edges from a four-valent vertex end at vertices of valence at least four.

If all valences are three or four, those endpoints are four-valent. The induced four-valent subgraph therefore has degree at least two at every vertex whenever it is nonempty. It is simple: loops would be zero-length straight edges, and two edges with the same abstract endpoints would have identical straight-segment images, violating local injectivity near either endpoint. A finite nonempty simple graph of minimum degree at least two contains a cycle, for example by extending a maximal simple path and closing to an earlier vertex. This has no implication that the cycle bounds a removable dodecahedral piece.

### 4.6 Local flexibility

For q<t<1 put s=q/t, so 0<s<1. The four rays in the author's construction have unit length, consecutive dot products -ts=-q, and opposite dot products 2t^2-1 and 2s^2-1. Their shorter spherical arcs have length 108 degrees.

Each open shorter arc is the normalization of a positive linear combination of its two endpoint rays. Its x,y coordinates lie strictly within the corresponding one of the four successive open coordinate quadrants. The four arc interiors are consequently disjoint, and distinct endpoints meet only as prescribed. Thus the spherical link is embedded and its cone is locally embedded at the center. The sectors extend uniquely to full unit regular pentagons. In particular these examples have no illicit self-crossing link.

The opposite-dot invariant 2t^2-1 is nonconstant on an interval. Passing to finitely many ray relabelings cannot turn the continuum into a single congruence class. The exact t=1/2 and t=3/4 fixtures are valid, but the general geometric construction, rather than two numerical examples alone, proves continuous local freedom. The resulting stars do not solve the face-closing equations for a sphere. No global counterexample follows.

## 5. Replay and adversarial validation

`audit_replay.py` is a new external verifier with immutable pins for the three original author artifacts. `independent_exact_checks.py` uses a different field basis, rational isolating-interval sign tests, Gaussian elimination, and a symbolic polynomial calculation. All checks use explicit exceptions and remain active under optimized Python.

The full audit replay passes 81 named checks. The complete replay itself was run with isolated normal and isolated optimized Python, and its outputs matched exactly. Both runs internally test isolated normal/optimized author diagnostics and relocated author bootstraps from unrelated directories whose names contain spaces. Recorded author full-input output is reproduced byte-for-byte as canonical JSON, SHA-256 `1461fc453df3778565f3a7fc2ed4bd6514a2a8cdb1e65e5616a99577fdc475e2`.

Checks include missing-input honesty; full-source and complete-corpus matching; whole-record mutation; status/ID/turn-limit/novelty escalation rejection; incorrect pentagon-constant rejection; altered corpus/PDF rejection; altered ZIP and bootstrap rejection; changed/missing/extra/duplicate members; parent-relative and absolute archive paths; and coordinated member/manifest rewriting against the immutable outer pins. Deeper archive tests deliberately refresh only the outer ZIP hash so the inventory, path, and member checks are actually reached. The independent program additionally rejects an intentionally false determinant value under both Python modes.

The independent exact suite confirms all four forbidden determinant cases, all 24 relabelings of each, the universal factorization, two exact local-star fixtures, all 16 possible trivalent-edge subsets on a four-cycle, and 125 incidence fixtures. These are supporting algebra and finite combinatorial checks, not a machine proof of every geometric sentence or an exhaustive surface search.

The bootstrap is an integrity/replay mechanism, not a digital signature or an arbitrary-code sandbox. SHA-256 pins require an independently trusted reference. Neither a matching author diagnostic nor a self-consistent rewritten manifest alone establishes mathematical truth. The exact acceptance below fixes the particular reviewed bytes.

## 6. Remaining gap and publication boundary

The work does not constrain all higher-valence stars, solve global face compatibility, remove cycles in the higher-valence induced graph, find a legal cap, or define and prove a suitable immersed dodecahedral decomposition. The embedded and immersed global questions remain unresolved by this work.

This audit introduces no additional solution approach and leaves the count at 3/5. Public-safe contents consist only of authored audit/proof discussion, authored executable checks, public verification metadata, exact acceptance, and unchanged public-safe author artifacts. Third-party source files, source text, datasets, private sources, and coordination material are excluded. There were no GitHub writes or other external mutations.
