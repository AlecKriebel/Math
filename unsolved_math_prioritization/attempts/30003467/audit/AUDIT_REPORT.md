# Independent acceptance audit: OWR-15427-009

Date: 8 October 2026 UTC. Problem 30003467, queue rank 998.

## Verdict

**ACCEPT the frozen packet as a credited prior negative resolution, `already_solved`, with 0/5 author approaches. No mandatory mathematical or scope correction is needed.**

The accepted author-manifest SHA-256 is:

`1f2b1644d763a9c3b87bb391ab135e2501b86458fa36e9d050da544b0e111dbf`

This acceptance means that the cited established theorem applies to the actual historical problem, its hypotheses and quantifiers have been matched, and the packet accurately limits its computational claims. It does not mean that a new disk configuration was constructed, coordinates were independently certified, a formal proof was checked, or a human referee reviewed this work.

## 1. Historical target and decisive source

The [official OWR report](https://publications.mfo.de/bitstream/handle/mfo/3583/OWR_2017_19.pdf?isAllowed=y&sequence=1), printed p.1173, Conjecture 2, concerns points colored with three labels in a given pseudo-disk arrangement, with a non-monochromatic trace required whenever its size is at least four. The page was independently read and rendered. The arrangement is fixed before choosing the coloring. The statement is primal; it does not color regions. The neighboring threshold-three remark is not the target.

The [publisher record](https://link.springer.com/article/10.1007/s00493-021-4846-5) independently confirms Damásdi and Pálvölgyi, *Realizing an m-Uniform Four-Chromatic Hypergraph with Disks*, Combinatorica 42 (Suppl 1), 1027–1048, publication and version-of-record date 21 September 2022. Its abstract states the finite, exactly-m, three-color obstruction. Thus the supplied catalog's later “open” label cannot determine the mathematical status.

The proof inspected was the complete relevant portion of the [authors' arXiv v1 PDF](https://arxiv.org/pdf/2011.12187v1): the definitions and Theorem 1, then Observation 8, Lemma 9, the rooted-tree construction, Theorem 12, Claim 14, and Lemma 16 through the end of Section 3, printed pp.1–12. The first three sections suffice; later results on unit disks and other shapes are not inputs to this deduction. The arXiv title page identifies v1, 24 November 2020. Construction pages 11–12 were also independently rendered and inspected.

Published metadata and the journal abstract were verified. The accessible proof is a preprint proof. The author's failed journal-PDF retrieval is recorded as HTML, and this audit does not upgrade that to full journal-proof access or assert byte identity between the preprint and version of record.

## 2. Construction audit

The following is an independently checked account of the needed logic, not a copied source proof or an executable geometric certificate.

### 2.1 The finite combinatorial obstruction

For a rooted tree, use child sets and root-to-leaf paths as edges. A two-coloring either makes a child set monochromatic or permits following the root's color down the tree to a monochromatic path. A complete m-ary tree with **m vertex levels** makes both edge types have size m. This level convention resolves the otherwise ambiguous word “depth.” For m=4 it has 85 vertices, 21 child-set edges and 64 path edges. Everything is finite.

The extension operation removes an edge F, attaches a fresh vertex to each replacement copy of F, and places a non-two-colorable hypergraph on those new vertices. If a three-coloring avoids monochromatic retained edges, F must be monochromatic in the old coloring; each replacement edge then forces its new vertex to avoid F's color. The fresh hypergraph would consequently be properly two-colored, a contradiction.

Starting with one singleton edge and applying this operation to the edges containing its distinguished vertex increases those edge sizes by one per round, while every inserted tree edge has size m. After m−1 rounds all edges have size m, and non-three-colorability is preserved. Only finitely many vertices, edges and extensions are used. The m=2 case is K4 and independently checks the interpretation of the operation. Neither this extension argument nor the tree obstruction alone proves disk realizability.

### 2.2 The geometric part is actually present

Theorem 12 is the needed local realization result, stronger than mere abstract non-two-colorability. It places a tree's vertices arbitrarily close to prescribed distinct points of a circle and its realizing disks arbitrarily close to that circle.

The sibling-first order is consistent: put children consecutively, then their descendant blocks in reverse child order, recursively within each block. Circularly consecutive sibling blocks can be selected by nearby circles. Their incidences have positive margins. The descendant construction then maintains fixed interior path vertices and unfixed descendant blocks on exposed boundary arcs. The local circle perturbation moves the chosen block outward, while previously fixed incidences are protected by shrinking the perturbation parameter. Each child is eventually moved strictly into its own new path disk and fixed. There are finitely many operations; the movement budget can be chosen below any prescribed tolerance. The final leaf-path and sibling disks realize precisely the desired hypergraph.

The parameter choices must preserve the circular order and the exposed arcs as well as the listed point incidences. This is possible: all blocks are finite and distinct, their separating open arcs can be chosen first, and all subsequent changes are arbitrarily small. The proof's iterative choices provide those margins. Boundary points during the construction are temporary; they are excluded from open disks until their intended insertion. They are not silently counted as interior points.

Lemma 16 then realizes the extension itself. A disk corresponding to an extendable edge has an exposed boundary arc. At a point of that arc, place a sufficiently small externally tangent auxiliary circle away from the old points and other disks. Slightly rotated copies of the old disk remain incidence-equivalent on the old points and have distinct tangency locations on the auxiliary circle. After sufficiently small enlargements, each has a separate cap for one new point. Theorem 12 inserts the desired tree hypergraph near those prescribed cap points, with its own disks close to the auxiliary circle. Choosing its tolerance smaller than the finite existing gaps ensures that each replacement disk gets exactly its designated new vertex and the small disks get no old vertices.

Crucially, each replacement disk can keep an exposed boundary point outside the auxiliary circle and outside the other copies. Those points can be selected before the final local realization, whose disks are then kept close enough to the auxiliary circle not to cover them. Exposed points of the retained extendable disks also survive sufficiently small local changes. This is the invariant needed for every later extension. Only distinguished-edge disks need that invariant; the inserted tree disks need not have it. The initial singleton has an immediate disk realization with an exposed boundary, so induction starts.

As usual in this notation, an edge named F is identified with its realizing disk when selecting an extension. The retired F disk is replaced; references to preservation apply to retained extendable disks and the replacement copies. This interpretive detail causes no gap in the applied induction.

If incidence stability is invoked at an intermediate representation with an unwanted boundary incidence, finitely many open disks can first be shrunk without changing their traces. An exposed boundary arc persists under a sufficiently small shrink, so the stability hypothesis is available. The theorem's finite construction therefore yields an actual geometric realization, rather than merely an abstract hypergraph or a limit requiring infinitely many points.

## 3. Exact transfer to the OWR statement

The definition at the beginning of the preprint makes the vertices the points, and the edges their intersections with disks. This rules out a primal/dual substitution. Apply Theorem 1 at m=4.

The theorem's construction already supplies a finite realizing family. Independently, the packet's witness-collection argument is valid even if one starts only from the point-set formulation: there are finitely many three-label assignments, so choose a witnessing disk for each and then take their union. That one family is fixed before testing any coloring. Removing duplicate disks or keeping one representative of each trace does not lose an obstruction.

Exactly four monochromatic points violate the requirement for every trace of at least four points. No shrinking to a four-element subset of a larger monochromatic trace is being assumed; exact uniformity is supplied by the source theorem itself.

For a selected open disk of radius r and nonempty trace E, put a = max of the distances of its included points from the center. Finiteness and openness give a < r. Any radius s with a < s < r defines a closed disk with the same trace: included distances are below s, excluded distances are at least r and therefore above s. This specifically handles excluded points that lay on the old open boundary. It produces strict incidence margins for every point and every disk.

Distinct Euclidean disks are admissible pseudo-disks: distinct concentric circles are disjoint, while two circles with different centers have common points on their radical-axis line and consequently at most two common boundary points. Duplicates can be removed. The connected-boundary-arc convention used by the related 2019 paper is also satisfied, allowing the ordinary empty and full-circle cases. Consequently neither convention rescues the conjecture.

General position is not required by the target or by this final transfer. If a stricter convention is imposed, the finite strict incidence margins give an open neighborhood of the realization. Within it one may avoid point collinearities, point cocircularities, coincident circles, tangencies and triple boundary intersections by generic arbitrarily small perturbations. There are only finitely many relevant degeneracy conditions, each with empty interior in the independent point and circle parameters. Incidences and non-three-colorability remain unchanged. This is an existence argument, not an explicit rational coordinate certificate.

The same reasoning applies to any prescribed positive threshold. It makes no claim that a fixed-radius family, a commonly stabbed family, or the dual region-coloring problem has the same obstruction.

## 4. Independent checks and their limits

The author packet contains 13 files, including its manifest, with 12 manifest-bound members. All bytes match the independently supplied manifest pin. The separate source-byte stage validates eight complete external files and the selected corpus-record digest; it does not establish the truth of the source contents.

Results in `INDEPENDENT_RESULTS.json` were produced by the new `independent_controls.py`, without importing the author's mathematical control module:

- Three relocated positive verifier runs: normal Python, `-O`, `-OO`.
- Three full source-byte and selected-record replay runs in those modes.
- Three enforced read-only relocated runs. Directory writability was explicitly checked under a non-root account, and file hashes remained unchanged.
- Twenty-seven independently specified adverse cases per mode, 81 rejections. Cases include malformed or duplicate JSON, nonfinite constants, Boolean integers, duplicate and unsafe names, missing members, an extra directory, symlinks, a wrong pin, false scope/threshold/answer claims, and an incorrect numerical receipt. Semantic mutations honestly rebind the disposable manifest while retaining the verifier and claim guards.
- 375 new exact-rational open-to-closed fixtures and 63,375 point-incidence comparisons. Every fixture includes points excluded on the old boundary. The independently written shrink formula differs from the author's formula.
- Exhaustive two-color checks of the tree hypergraphs for m=1,2,3: respectively 2, 8 and 8,192 assignments. At m=4, only the 85-vertex/85-edge uniformity structure is checked, not its exponentially many colorings.
- All 81 three-label assignments of the K4 base example.
- An abstract witness-collection control on 10 vertices: a fixed family of 210 four-element edges defeats all 59,049 three-label assignments. This example is explicitly **not** asserted to be a disk realization.

The author's own adverse-case suite was separately rerun and returned its advertised six positive/read-only runs and 63 rejected cases. No change was made to the original public packet. The new audit harness also runs identically under normal, optimized and doubly optimized Python, with no assertions used as guards.

These controls test integrity, scope, elementary transfer, and small combinatorial cases. They do not numerically reproduce the large geometric theorem, certify the published proof mechanically, or turn a source-byte match into mathematical proof. Manifest verification assumes that the external pin and verifier code are trusted. Rebound negative controls are not a claim of security against an adversary who can replace that trust anchor and all verifier code.

## 5. Disposition and publication boundary

The exact problem is already negatively resolved by prior published work. The author ledger records discovery before any substantive new proof approach, so the requested 0/5 count is consistent. No additional attempt should be manufactured for this literature resolution or its audit.

The audit did not independently repeat every historical repository duplicate search. The packet appropriately describes that gate as bounded observable searches, not exhaustive inspection of every branch or all literature. This limitation does not affect the mathematical negative resolution.

No correction patch is required. Preserve the frozen original and retain the explicit distinction between published status, inspected preprint proof, and unperformed geometric coordinate replay. This report and its audit controls contain authored analysis and public verification metadata, not copied source documents, corpus contents, private personal data or coordination material. No remote changes or author outreach were performed as part of this audit.
